from datetime import datetime
import logging

import openai

import Events
from .Events import *
from Models.Plugins import *
from .Session import Session
from .OpenAiKeysManager import OpenAiKeysManager


@register(
    description="OpenAi 接口封装",
    version="1.0.0",
    author="For_Lin0601",
    priority=10
)
class OpenAiInteract(Plugin):
    """OpenAi 接口封装

    将文字接口和图片接口封装供调用方使用
    """

    sessions_dict: dict[str, Session]
    """QQ以`person_xxx`或`group_xxx`保存

    微信以`wx_wxid_xxx`保存
    """

    @on(PluginsLoadingFinished)
    @on(PluginsReloadFinished)
    def init(self, events: EventContext, **kwargs):
        if self.is_first_init():
            self.sessions_dict = {}
        else:
            self.sessions_dict = self.get_reload_config("session", default={})
        self.config = self.emit(Events.GetConfig__)
        self.openai_config = self.config.openai_config
        self.completion_api_params = self.config.completion_api_params
        self.keys_manager = OpenAiKeysManager(
            self.openai_config,
            self.completion_api_params["default"]["params"],
        )

    def on_reload(self):
        self.set_reload_config("session", self.sessions_dict)

    @on(GetOpenAi__)
    def get_openai(self, events: EventContext, **kwargs):
        events.prevent_postorder()
        events.return_value = self

    def request_completion(self, session_name: str, message: str, tmp_api_key_index=None):
        """请求补全接口回复, 屏蔽敏感词"""

        # 删除过期的对话
        current_time = datetime.now()
        del_list = []
        for session in self.sessions_dict.values():
            if session.time_out < current_time:
                logging.info("删除过期的对话: " + session.session_name)
                del_list.append(session.session_name)
            else:
                # 会话未过期, 检查长度
                conversation = session.sessions
                total_length = session.get_content_length()

                if total_length > self.config.prompt_submit_length:
                    # 长度超过限制, 从头开始暴力删除, 每次删除两个记录
                    logging.debug("长度超过限制, 从头开始暴力删除: " + session.session_name)
                    while total_length > self.config.prompt_submit_length:
                        # 删除最前面的两个记录, 不删除第一条人格设置
                        if len(conversation) >= 3:
                            total_length -= len(conversation[2]["content"])
                            del conversation[2]
                        if len(conversation) >= 3:
                            total_length -= len(conversation[2]["content"])
                            del conversation[2]
                        if len(conversation) < 3 and total_length > self.config.prompt_submit_length:
                            return "[bot]err: 对话长度超过限制, 当前场景预设过长, 请用`!r`重置会话"

        if del_list:
            for _session_name in del_list:
                del self.sessions_dict[_session_name]
        if session_name not in self.sessions_dict:
            self.sessions_dict[session_name] = Session(
                session_name, "default", self.config.default_prompt["default"], self.config.session_expire_time)
        session = self.sessions_dict[session_name]
        session.add_user(message)

        # 如果没有可用的 API Key
        if not self.keys_manager.has_openai_config(tmp_api_key_index, session.is_plus):
            logging.error("无可用的 OpenAi API Key")
            return "[bot]err: 无可用的 OpenAi API Key, 等待管理员处理"

        try:
            session_config = self.keys_manager\
                .get_openai_config_by_index(tmp_api_key_index, session.is_plus)
            # 配置openai http代理
            if session_config["http_proxy"] is not None:
                openai.proxy = {
                    "http": session_config["http_proxy"],
                    "https": session_config["http_proxy"]
                }
            # 配置openai api_base
            if session_config["reverse_proxy"] is not None:
                openai.api_base = session_config["reverse_proxy"]
            # 配置API Key
            openai.api_key = session_config["api_key"]

            # 如果该session有自己的配置
            if session.params_name and session.params_name in self.completion_api_params:
                params = self.completion_api_params[session.params_name]["params"]
            else:
                params = session_config["params"]
            flag_prefix = not session.params_name or session.params_name in self.completion_api_params

            gpt_response = openai.ChatCompletion.create(
                messages=session.sessions,
                **params,
            )

            response_content = gpt_response['choices'][0]['message']['content']
            if len(response_content) > 3500:
                response_content = response_content[:3500] + \
                    "   ...[消息过长, 已截断]"

            # 处理敏感词
            response_content = self.emit(
                Events.BanWordProcess__, message=response_content)

            # 如果成功, 添加助手的回复到会话中
            logging.debug(f"{session_name}: {session.sessions}")
            reply = (session.prefix if flag_prefix else "") + response_content
            session.add_assistant(response_content)
            return reply
        except openai.OpenAIError as e:
            # 如果是 OpenAIError, 尝试使用下一个 API Key
            session = self.sessions_dict[session_name]
            conversation = session.sessions
            if conversation[-1]["role"] == "user":
                conversation.pop()
            str_e = str(e)
            if "Rate limit reached" in str_e:
                # "[bot]err: 触发限速策略, 请20秒后重试"
                logging.warning(f"OpenAi API 限速, 临时切换下一个 API Key: {str_e}")
                tmp = tmp_api_key_index if tmp_api_key_index else self.keys_manager.get_index(
                    session.is_plus)
                return self.request_completion(session_name, message, tmp + 1)
            elif "The server had an error while processing your request. Sorry about that!" in str_e:
                # "[bot]err: OpenAi API 内部错误, 请稍后重试"
                logging.warning(f"OpenAi API 内部错误, 临时切换下一个 API Key: {str_e}")
                tmp = tmp_api_key_index if tmp_api_key_index else self.keys_manager.get_index(
                    session.is_plus)
                return self.request_completion(session_name, message, tmp + 1)
            elif "远程主机强迫关闭了一个现有的连接。" in str_e \
                    or "SSLEOFError" in str_e:
                # "[bot]err: OpenAi API 连接超时, 请稍后重试"
                logging.warning(f"OpenAi API 连接超时: {str_e}")
                self.emit(Events.GetCQHTTP__).NotifyAdmin(
                    f"[bot]err: [{session_name}]OpenAi API 连接超时\n{str_e}"
                )
                return self.config.reply_timeout_message
            elif "maximum context length" in str_e:
                # "[bot]err: 会话历史记录过长, 请用'!reset'重置会话"
                logging.warning(f"OpenAi API 历史记录过长: {str_e}")
                # 删除最前面的两个记录, 不删除第一条人格设置
                if len(conversation) < 3:
                    # 走到这里得怀疑是不是人格设置太长了, 直接导致token过长(我就是懒得算token)
                    return f"[bot]err: [{session_name}]会话历史记录过长, 请用'!reset'重置会话"
                if len(conversation) >= 3:
                    total_length -= len(conversation[2]["content"])
                    del conversation[2]
                if len(conversation) >= 3:
                    total_length -= len(conversation[2]["content"])
                    del conversation[2]
                return self.request_completion(session_name, message)
            elif "The server is overloaded or not ready yet." in str_e:
                # "[bot]err: OpenAi API 连接超时, 请稍后重试"
                logging.warning(f"OpenAi API 连接超时: {str_e}")
                self.emit(Events.GetCQHTTP__).NotifyAdmin(
                    f"[bot]err: [{session_name}]OpenAi API 连接超时\n{str_e}"
                )
                return self.config.reply_timeout_message
            elif "当前分组上游负载已饱和" in str_e:
                # 当前分组上游负载已饱和，请稍后再试
                logging.warning(f"当前分组上游负载已饱和，请稍后再试：{str_e}")
                self.emit(Events.GetCQHTTP__).NotifyAdmin(
                    f"[bot]err: [{session_name}]负载饱和：\n{str_e}"
                )
                return self.config.reply_timeout_message

            logging.error(f"OpenAi API error: {str_e}")
            tmp_index = tmp_api_key_index if tmp_api_key_index else self.keys_manager.get_index(
                session.is_plus)
            if self.keys_manager.next_api(session.is_plus):
                logging.info(
                    f"切换至第 {self.keys_manager.get_index()+1} 个 API Key:{self.keys_manager.get_openai_config_name_by_index(is_plus=session.is_plus)}")
                self.emit(Events.GetCQHTTP__).NotifyAdmin(
                    f"[bot]err: [{session_name}]调用 API 失败!API Key:{self.keys_manager.get_openai_config_name_by_index(tmp_index, session.is_plus)}\n" +
                    f"切换至第 {self.keys_manager.get_index()+1} 个 API Key:{self.keys_manager.get_openai_config_name_by_index(is_plus=session.is_plus)}\n{str_e}")
                return self.request_completion(session_name, message)
            else:
                self.emit(Events.GetCQHTTP__).NotifyAdmin(
                    f"[bot]err: [{session_name}]调用 API 失败!API Key:{self.keys_manager.get_openai_config_name_by_index(tmp_index, session.is_plus)}\n" +
                    "无可用的 API Key" +
                    ("\n请切换模型重试" if session.is_plus else "") +
                    f"\n{str_e}")
                return "[bot]err: 无可用的 OpenAi API Key, 等待管理员处理"
        except Exception as e:
            str_e = str(e)
            logging.error(f"Error: {str_e}")
            self.emit(Events.GetCQHTTP__).NotifyAdmin(
                f"[bot]err: [{session_name}]会话调用API 错误, 错误信息: \n{str_e}"
            )
            return f"[bot]err: {str_e}"
