from datetime import datetime, timedelta
import logging

import openai

import Events
from .Events import *
from Models.Plugins import *


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

    session: dict[str, list]
    """QQ以`person_xxx`或`group_xxx`保存

    微信以`wx_person_xxx`或`wx_group_xxx`保存
    """

    time_out: dict[str, datetime]
    """过期时间, 单位秒"""

    def __init__(self):
        self.api_key_index = 0

    @on(PluginsLoadingFinished)
    def init(self, events: EventContext, **kwargs):
        self.openai_api_keys = self.emit(Events.GetConfig__).openai_api_keys
        self.session = {}
        self.time_out = {}

    @on(PluginsReloadFinished)
    def get_config(self, events: EventContext, **kwargs):
        self.openai_api_keys = self.emit(Events.GetConfig__).openai_api_keys
        self.session = self.get_reload_config("session")
        self.time_out = self.get_reload_config("time_out")

    def on_reload(self):
        self.set_reload_config("session", self.session)
        self.set_reload_config("time_out", self.time_out)

    @on(GetOpenAi__)
    def get_openai(self, events: EventContext, **kwargs):
        events.prevent_postorder()
        events.return_value = self

    def request_completion(self, session_name: str, message: str, tmp_api_key_index=None):
        """请求补全接口回复, 屏蔽敏感词"""
        config = self.emit(Events.GetConfig__)

        # 删除过期的对话
        for name, last_updated_time in self.time_out.items():
            expiration_time = last_updated_time + \
                timedelta(seconds=config.session_expire_time)
            if datetime.now() > expiration_time:
                del self.session[name]
                del self.time_out[name]
            else:
                # 会话未过期, 检查长度
                conversation = self.session[name]
                total_length = sum(len(msg["content"]) for msg in conversation)

                if total_length > config.prompt_submit_length:
                    # 长度超过限制, 从头开始暴力删除, 每次删除两个记录
                    while total_length > config.prompt_submit_length:
                        # 删除最前面的两个记录
                        if conversation:
                            del conversation[0]
                            total_length -= len(conversation[0]["content"])
                        if conversation:
                            del conversation[0]
                            total_length -= len(conversation[0]["content"])

        if session_name not in self.session:
            self.session[session_name] = [
                {"role": "user",
                 "content": config.default_prompt["default"]},
                {"role": "assistant",
                 "content": "ok, I'll follow your commands."}
            ]
        self.session[session_name].append({"role": "user", "content": message})
        self.time_out[session_name] = datetime.now()

        # 如果没有可用的 API Key, 通知管理员
        if not config.openai_api_keys or self.api_key_index >= len(config.openai_api_keys):
            logging.error("无可用的 OpenAi API Key")
            self.emit(Events.GetCQHTTP__).NotifyAdmin(
                f"[bot]err: [{session_name}]无可用的 OpenAi API Key")
            return "[bot]err: 无可用的 OpenAi API Key, 等待管理员处理"

        try:
            # 使用当前下标对应的 API Key
            if tmp_api_key_index is not None:
                openai.api_key = config.openai_api_keys[tmp_api_key_index]
            else:
                openai.api_key = config.openai_api_keys[self.api_key_index]

            gpt_response = openai.ChatCompletion.create(
                messages=self.session[session_name],
                **config.completion_api_params
            )

            gpt_response_text = gpt_response['choices'][0]['message']['content']
            if len(gpt_response_text) > 3500:
                gpt_response_text = gpt_response_text[:3500] + \
                    "   ...[消息过长, 已截断]"

            gpt_response = self.emit(
                Events.BanWordProcess__, message=gpt_response_text)

            # 如果成功, 添加助手的回复到会话中
            self.session[session_name].append(
                {"role": "assistant", "content": gpt_response_text})
            return gpt_response_text
        except openai.OpenAIError as e:
            # 如果是 OpenAIError, 尝试使用下一个 API Key
            if self.session[session_name][-1]["role"] == "user":
                self.session[session_name].pop()
            str_e = str(e)
            if "Rate limit reached" in str_e:
                # "[bot]err: 触发限速策略, 请20秒后重试"
                return self.request_completion(session_name, message, self.api_key_index + 1)
            elif "maximum context length" in str_e:
                return f"[bot]err: [{session_name}]会话历史记录过长, 请用'!reset'重置会话"

            logging.warning(f"OpenAi API error: {str_e}")
            self.api_key_index += 1
            # 递归调用, 使用下一个 API Key
            self.emit(Events.GetCQHTTP__).NotifyAdmin(
                f"[bot]err: [{session_name}]调用 API 失败!\n切换第 {self.api_key_index + 1} 个 OpenAi API Key\n{str_e}")
            return self.request_completion(session_name, message)
        except Exception as e:
            logging.error(f"Error: {str_e}")
            self.emit(Events.GetCQHTTP__).NotifyAdmin(
                f"[bot]err: [{session_name}]会话调用API 错误, 错误信息: \n{str_e}"
            )
            return f"[bot]err: {str_e}"
