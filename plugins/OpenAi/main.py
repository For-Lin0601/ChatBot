from datetime import datetime, timedelta
import logging

import openai

import Events
from .Events import *
from Models.Plugins import *


class Session:
    """运行时记忆链(暂时没做外部存储)"""

    def __init__(self, session_name: str, role_name: str, content: str, out_time: datetime):
        self.session_name = session_name
        """与用户绑定的会话名字"""

        self.role_name = role_name
        """场景预设名"""

        self.sessions = [
            {"role": "user", "content": content},
            {"role": "assistant", "content": "ok, I'll follow your commands."}
        ]
        """对话内容"""

        self.time_out = datetime.now() + timedelta(seconds=out_time)
        """过期时间"""

    def add_user(self, content: str):
        self.sessions.append({"role": "user", "content": content})

    def add_assistant(self, content: str):
        self.sessions.append({"role": "assistant", "content": content})

    @property
    def last_user_content(self):
        if not self.sessions:
            return ""
        if self.sessions[-1]["role"] == "user":
            return self.sessions[-1]["content"]
        return self.sessions[-2]["content"] if len(self.sessions) > 1 else ""

    @property
    def last_assistant_content(self):
        if not self.sessions:
            return ""
        if self.sessions[-1]["role"] == "assistant":
            return self.sessions[-1]["content"]
        return self.sessions[-2]["content"] if len(self.sessions) > 1 else ""


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

    def __init__(self):
        self.api_key_index = 0
        self.openai_api_keys = self.emit(Events.GetConfig__).openai_api_keys

    @on(PluginsLoadingFinished)
    def init(self, events: EventContext, **kwargs):
        self.sessions_dict = {}

    @on(PluginsReloadFinished)
    def get_config(self, events: EventContext, **kwargs):
        self.sessions_dict = self.get_reload_config("session")

    def on_reload(self):
        self.set_reload_config("session", self.sessions_dict)

    @on(GetOpenAi__)
    def get_openai(self, events: EventContext, **kwargs):
        events.prevent_postorder()
        events.return_value = self

    def request_completion(self, session_name: str, message: str, tmp_api_key_index=None):
        """请求补全接口回复, 屏蔽敏感词"""
        config = self.emit(Events.GetConfig__)

        # 删除过期的对话
        current_time = datetime.now()
        for session in self.sessions_dict.values():
            if session.time_out < current_time:
                logging.info("删除过期的对话: " + session.session_name)
                del self.sessions_dict[session.session_name]
            else:
                # 会话未过期, 检查长度
                conversation = session.sessions
                total_length = sum(len(msg["content"]) for msg in conversation)

                if total_length > config.prompt_submit_length:
                    # 长度超过限制, 从头开始暴力删除, 每次删除两个记录
                    logging.debug("长度超过限制, 从头开始暴力删除: " + session.session_name)
                    while total_length > config.prompt_submit_length:
                        # 删除最前面的两个记录, 不删除第一条人格设置
                        if len(conversation) >= 3:
                            total_length -= len(conversation[2]["content"])
                            del conversation[2]
                        if len(conversation) >= 3:
                            total_length -= len(conversation[2]["content"])
                            del conversation[2]
                        if len(conversation) < 3 and total_length > config.prompt_submit_length:
                            return "[bot]err: 对话长度超过限制, 当前场景预设过长, 请用`!r`重置会话"

        if session_name not in self.sessions_dict:
            self.sessions_dict[session_name] = Session(
                session_name, "default", config.default_prompt["default"], config.session_expire_time)
        self.sessions_dict[session_name].add_user(message)

        # 如果没有可用的 API Key
        if not config.openai_api_keys or \
            self.api_key_index >= len(config.openai_api_keys) or \
                (tmp_api_key_index is not None and tmp_api_key_index >= len(config.openai_api_keys)):
            logging.error("无可用的 OpenAi API Key")
            return "[bot]err: 无可用的 OpenAi API Key, 等待管理员处理"

        try:
            # 使用当前下标对应的 API Key
            if tmp_api_key_index is not None:
                openai.api_key = config.openai_api_keys[tmp_api_key_index]
            else:
                openai.api_key = config.openai_api_keys[self.api_key_index]

            gpt_response = openai.ChatCompletion.create(
                messages=self.sessions_dict[session_name].sessions,
                **config.completion_api_params
            )

            response_content = gpt_response['choices'][0]['message']['content']
            if len(response_content) > 3500:
                response_content = response_content[:3500] + \
                    "   ...[消息过长, 已截断]"

            # 处理敏感词
            response_content = self.emit(
                Events.BanWordProcess__, message=response_content)

            # 如果成功, 添加助手的回复到会话中
            self.sessions_dict[session_name].add_assistant(response_content)
            logging.debug(
                f"{session_name}: {self.sessions_dict[session_name].sessions}")
            return response_content
        except openai.OpenAIError as e:
            # 如果是 OpenAIError, 尝试使用下一个 API Key
            conversation = self.sessions_dict[session_name].sessions
            if conversation[-1]["role"] == "user":
                conversation.pop()
            str_e = str(e)
            if "Rate limit reached" in str_e:
                # "[bot]err: 触发限速策略, 请20秒后重试"
                logging.warning(f"OpenAi API 限速, 临时切换下一个 API Key: {str_e}")
                tmp = tmp_api_key_index if tmp_api_key_index else self.api_key_index
                return self.request_completion(session_name, message, tmp + 1)
            elif "The server had an error while processing your request. Sorry about that!" in str_e:
                # "[bot]err: OpenAi API 内部错误, 请稍后重试"
                logging.warning(f"OpenAi API 内部错误, 临时切换下一个 API Key: {str_e}")
                tmp = tmp_api_key_index if tmp_api_key_index else self.api_key_index
                return self.request_completion(session_name, message, tmp + 1)
            elif "远程主机强迫关闭了一个现有的连接。" in str_e \
                    or "SSLEOFError" in str_e:
                # "[bot]err: OpenAi API 连接超时, 请稍后重试"
                logging.warning(f"OpenAi API 连接超时: {str_e}")
                self.emit(Events.GetCQHTTP__).NotifyAdmin(
                    f"[bot]err: [{session_name}]OpenAi API 连接超时"
                )
                return config.tip_timeout_message
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

            logging.error(f"OpenAi API error: {str_e}")
            self.api_key_index += 1
            # 递归调用, 使用下一个 API Key
            if self.api_key_index < len(config.openai_api_keys):
                self.emit(Events.GetCQHTTP__).NotifyAdmin(
                    f"[bot]err: [{session_name}]调用 API 失败!API Key:{self.openai_api_keys[self.api_key_index-1]}\n" +
                    f"切换至第 {self.api_key_index+1} 个 API Key:{self.openai_api_keys[self.api_key_index]}\n{str_e}")
                return self.request_completion(session_name, message)
            else:
                self.emit(Events.GetCQHTTP__).NotifyAdmin(
                    f"[bot]err: [{session_name}]调用 API 失败!API Key:{self.openai_api_keys[self.api_key_index-1]}\n" +
                    f"无可用的 API Key\n{str_e}")
                return "[bot]err: 无可用的 OpenAi API Key, 等待管理员处理"
        except Exception as e:
            str_e = str(e)
            logging.error(f"Error: {str_e}")
            self.emit(Events.GetCQHTTP__).NotifyAdmin(
                f"[bot]err: [{session_name}]会话调用API 错误, 错误信息: \n{str_e}"
            )
            return f"[bot]err: {str_e}"
