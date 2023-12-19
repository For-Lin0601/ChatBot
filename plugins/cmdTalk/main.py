

import re

import Events
from Models.Plugins import *
from ..gocqOnQQ.CQHTTP_Protocol.CQHTTP_Protocol import CQHTTP_Protocol


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
                "和私聊判断逻辑一模一样, 只有管理员在指导新人上手的时候会用到。多与`!sent`命令合用, 详情请看`!cmd sent`"
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
        cqhttp: CQHTTP_Protocol = self.emit(Events.GetCQHTTP__)
        sender_id = kwargs["sender_id"]
        if not message:
            reply = "[bot]err: 请输入要发送的信息"
        else:
            reply = self.emit(Events.GetOpenAi__).request_completion(
                f"person_{sender_id}", message)

        cqhttp.sendPersonMessage(sender_id, reply)
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
        cqhttp: CQHTTP_Protocol = self.emit(Events.GetCQHTTP__)
        group_id = kwargs["group_id"]
        if not message:
            reply = "[bot]err: 请输入要发送的信息"
        else:
            reply = self.emit(Events.GetOpenAi__).request_completion(
                f"group_{group_id}", message)
        cqhttp.sendGroupMessage(group_id, reply)

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
        wcf = self.emit(Events.GetWCF__)
        sender = kwargs["roomid"] if kwargs["roomid"] else kwargs["sender"]
        if not message:
            reply = "[bot]err: 请输入要发送的信息"
        else:
            reply = self.emit(Events.GetOpenAi__).request_completion(
                f"wx_{sender}", message)
        wcf.send_text(reply, sender)
