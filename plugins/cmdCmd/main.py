

import Events
from .Events import *
from Models.Plugins import *


@register(
    description="显示指令列表[cmd]",
    version="1.0.0",
    author="For_Lin0601",
    priority=201
)
class CmdCommand(Plugin):

    @on(CmdCmdHelp)
    def help(self, event: EventContext, **kwargs):
        event.return_value = ["!cmd - 显示指令列表"]

    @on(GetQQPersonCommand)
    def cmd_cmd(self, event: EventContext, **kwargs):
        message: str = kwargs["message"].strip()
        if message != "cmd":
            return
        event.prevent_postorder()
        reply = "[bot] 当前所有指令:\n\n"
        reply += "\n".join(self.emit(CmdCmdHelp))
        self.emit(Events.GetCQHTTP__).sendPersonMessage(
            user_id=kwargs["sender_id"],
            message=reply
        )

    @on(GetQQGroupCommand)
    def cmd_cmd(self, event: EventContext, **kwargs):
        message: str = kwargs["message"].strip()
        if message != "cmd":
            return
        event.prevent_postorder()
        reply = "[bot] 当前所有指令:\n\n"
        reply += "\n".join(self.emit(CmdCmdHelp))
        self.emit(Events.GetCQHTTP__).sendGroupMessage(
            group_id=kwargs["launcher_id"],
            message=reply
        )

    @on(GetWXCommand)
    def cmd_cmd(self, event: EventContext, **kwargs):
        message: str = kwargs["command"].strip()
        if message != "cmd":
            return
        event.prevent_postorder()
        reply = "[bot] 当前所有指令:\n\n"
        reply += "\n".join(self.emit(CmdCmdHelp))
        self.emit(Events.GetWCF__).send_text(
            msg=reply,
            receiver=kwargs["roomid"] if kwargs["roomid"] else kwargs["sender"]
        )
