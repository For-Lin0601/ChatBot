

import Events
from Models.Plugins import *
from ..gocqOnQQ.entities.components import At, Plain
from wcferry import Wcf


@register(
    description="查看聊天历史记录[history]",
    version="1.0.0",
    author="For_Lin0601",
    priority=209
)
class HelpCommand(Plugin):

    @on(CmdCmdHelp)
    def help(self, event: EventContext, **kwargs):
        event.return_value.append(
            "!history - 查看聊天历史记录"
        )

    @on(GetQQPersonCommand)
    def wx_cmd_history(self, event: EventContext, **kwargs):
        message: str = kwargs["message"].strip()
        if message != "history":
            return
        event.prevent_postorder()
        launcher_id = kwargs["launcher_id"]
        session_name = f"person_{launcher_id}"
        self._qq_cmd_history(session_name, kwargs["sender_id"], launcher_id)

    @on(GetQQGroupCommand)
    def wx_cmd_history(self, event: EventContext, **kwargs):
        message: str = kwargs["message"].strip()
        if message != "history":
            return
        event.prevent_postorder()
        launcher_id = kwargs["launcher_id"]
        session_name = f"group_{launcher_id}"
        self._qq_cmd_history(session_name, kwargs["sender_id"], launcher_id)

    @on(GetWXCommand)
    def wx_cmd_history(self, event: EventContext, **kwargs):
        message: str = kwargs["command"].strip()
        if message != "history":
            return
        event.prevent_postorder()
        sender = kwargs["roomid"] if kwargs["roomid"] else kwargs["sender"]
        session_name = "wx_{}".format(sender)
        openai = self.emit(Events.GetOpenAi__)
        wcf: Wcf = self.emit(Events.GetWCF__)
        if session_name not in openai.sessions_dict:
            wcf.send_text("[bot] 暂无历史记录", sender)
            return

        config = self.emit(Events.GetConfig__)
        session = openai.sessions_dict[session_name]
        reply = ["[bot] 当前历史记录:"]
        for _session in session.sessions:
            if _session["role"] == "user":
                reply.append(f"user:\n{_session['content']}")
            else:
                reply.append(f"assistant:\n{_session['content']}")

        reply[1] = "user:\n" + config.command_reset_name_message + \
            "{}".format(session.role_name)

        logging.debug(f"微信[{sender}]查看历史记录: {reply}")
        wcf.send_text("\n\n".join(reply), sender)

    def _qq_cmd_history(self, session_name, sender_id, group_id=None):
        openai = self.emit(Events.GetOpenAi__)
        cqhttp = self.emit(Events.GetCQHTTP__)
        if session_name not in openai.sessions_dict:
            if session_name.startswith("person_"):
                cqhttp.sendPersonMessage(
                    sender_id, "[bot] 暂无历史记录",
                    group_id=sender_id if sender_id != group_id else None,
                    auto_escape=True
                )
            else:
                cqhttp.sendGroupMessage(group_id, [
                    At(qq=sender_id), Plain(text="[bot] 暂无历史记录")
                ])
            return

        config = self.emit(Events.GetConfig__)
        session = openai.sessions_dict[session_name]
        bot_qq = config.qq
        qq_list = []
        name_list = []
        message_list = []
        for _session in session.sessions:
            if _session["role"] == "user":
                qq_list.append(sender_id)
                name_list.append("user")
            else:
                qq_list.append(bot_qq)
                name_list.append("bot")
            message_list.append(_session["content"])

        message_list[0] = config.command_reset_name_message + \
            "{}".format(session.role_name)

        reply = self.emit(
            ForwardMessage__,
            message=message_list, qq=qq_list, name=name_list)

        logging.debug(f"查看历史记录: {reply}")
        logging.debug(f"{sender_id=} {group_id=}")

        if session_name.startswith("person_"):
            cqhttp.sendPersonForwardMessage(sender_id, reply)
        else:
            cqhttp.sendGroupForwardMessage(group_id, reply)
