

import re

import Events
from Models.Plugins import *
from ..OpenAi.Session import Session
from ..cmdDefault.CheckPermission import check_permission


@register(
    description="和gpt对话[t, talk]",
    version="1.0.0",
    author="For_Lin0601",
    priority=210
)
class TalkCommand(Plugin):

    @on(CmdCmdHelp)
    def help(self, event: EventContext, **kwargs):
        event.return_value["talk"] = {
            "is_admin": False,
            "alias": ["t"],
            "summary": "向gpt发送信息",
            "usage": "!talk <信息>",
            "description": (
                "和私聊判断逻辑一模一样, 只有管理员在指导新人上手的时候会用到。多与`!sent`命令合用, 详情请看`!cmd sent`\n"
                "可携带参数`-<配置名>`, 用于以指定配置发起一次gpt请求。请确保有足够的权限"
            )
        }

    @on(GetQQPersonCommand)
    def cmd_talk(self, event: EventContext, **kwargs):
        message: str = kwargs["message"].strip()
        pattern_alarm = r'^t[^a-zA-Z]+'
        if not (re.search(pattern_alarm, message) or message == "t" or message.startswith("talk")):
            return
        event.prevent_postorder()
        if message.startswith("talk"):
            message = message[4:].strip()
        elif message.startswith("t"):
            message = message[1:].strip()
        sender_id = kwargs["sender_id"]

        if not message:
            reply = "[bot]err: 请输入要发送的信息"
            self.emit(Events.GetCQHTTP__).sendPersonMessage(sender_id, reply)
            return

        message_chain = kwargs["message_chain"]
        message_chain.message[0].text = message
        if not message.startswith("-"):
            self.emit(QQ_private_message, QQevents=message_chain)
            return

        if message == "-":
            reply = "[bot]err: 请输入要发送的信息"
            self.emit(Events.GetCQHTTP__).sendPersonMessage(sender_id, reply)
            return

        if not check_permission(sender_id):
            reply = "[bot]err: 权限不足/意外的`-`出现在了文本开头"
            self.emit(Events.GetCQHTTP__).sendPersonMessage(sender_id, reply)
            return

        config = self.emit(Events.GetConfig__)
        text = message[1:].split()[0]
        if text not in config.completion_api_params:
            reply = "[bot]err: 无效的配置名/意外的`-`出现在了文本开头"
            self.emit(Events.GetCQHTTP__).sendPersonMessage(sender_id, reply)
            return

        open_ai = self.emit(Events.GetOpenAi__)
        message_chain.message[0].text = message[len(text) + 1:]
        session_name = f"person_{sender_id}"
        if session_name not in open_ai.sessions_dict:
            open_ai.sessions_dict[session_name] = Session(
                session_name, "default", config.default_prompt["default"], config.session_expire_time)
        open_ai.sessions_dict[session_name].set_plus_params_for_once(text)
        self.emit(QQ_private_message, QQevents=message_chain)
        return

    @on(GetQQGroupCommand)
    def group_send(self, event: EventContext, **kwargs):
        message: str = kwargs["message"].strip()
        pattern_alarm = r'^t[^a-zA-Z]+'
        if not (re.search(pattern_alarm, message) or message == "t" or message.startswith("talk")):
            return
        event.prevent_postorder()
        if message.startswith("talk"):
            message = message[4:].strip()
        elif message.startswith("t"):
            message = message[1:].strip()
        group_id = kwargs["group_id"]

        if not message:
            reply = "[bot]err: 请输入要发送的信息"
            self.emit(Events.GetCQHTTP__).sendGroupMessage(group_id, reply)
            return

        if message.startswith("-"):
            reply = "[bot]err: 群聊暂不支持切换配置/意外的`-`出现在了文本开头"
            self.emit(Events.GetCQHTTP__).sendGroupMessage(group_id, reply)
            return

        message_chain = kwargs["message_chain"]
        message_chain.message[0].text = message
        self.emit(QQ_group_message, QQevents=message_chain)
        return

    @on(GetWXCommand)
    def wx_send(self, event: EventContext, **kwargs):
        message: str = kwargs["command"].strip()
        pattern_alarm = r'^t[^a-zA-Z]+'
        if not (re.search(pattern_alarm, message) or message == "t" or message.startswith("talk")):
            return
        event.prevent_postorder()
        if message.startswith("talk"):
            message = message[4:].strip()
        elif message.startswith("t"):
            message = message[1:].strip()
        sender = kwargs["roomid"] if kwargs["roomid"] else kwargs["sender"]

        if not message:
            reply = "[bot]err: 请输入要发送的信息"
            self.emit(Events.GetWCF__).send_text(reply, sender)
            return

        wx_msg = kwargs["message"]
        wx_msg.content = message
        if not message.startswith("-"):
            self.emit(Wx_msg, Wx_msg=wx_msg, is_admin=kwargs["is_admin"])
            return

        if message == "-":
            reply = "[bot]err: 请输入要发送的信息"
            self.emit(Events.GetWCF__).send_text(reply, sender)
            return

        if not check_permission(sender):
            reply = "[bot]err: 权限不足/意外的`-`出现在了文本开头"
            self.emit(Events.GetWCF__).send_text(reply, sender)
            return

        text = message[1:].split()[0]
        config = self.emit(Events.GetConfig__)
        if text not in config.completion_api_params:
            reply = "[bot]err: 无效的配置名/意外的`-`出现在了文本开头"
            self.emit(Events.GetWCF__).send_text(reply, sender)
            return

        wx_msg.content = message[len(text) + 1:]
        open_ai = self.emit(Events.GetOpenAi__)
        session_name = f"wx_{sender}"
        if session_name not in open_ai.sessions_dict:
            open_ai.sessions_dict[session_name] = Session(
                session_name, "default", config.default_prompt["default"], config.session_expire_time)
        open_ai.sessions_dict[session_name].set_plus_params_for_once(text)
        self.emit(Wx_msg, Wx_msg=wx_msg, is_admin=kwargs["is_admin"])
        return
