

import Events
from .Events import *
from Models.Plugins import *


@register(
    description="显示指令列表[cmd]",
    version="1.0.0",
    author="For_Lin0601",
    priority=201,
)
class CmdPlugin(Plugin):

    def __init__(self):
        pass

    def on_reload(self):
        pass

    def on_stop(self):
        pass

    @on(CmdCmdHelp)
    def help(self, event: EventContext, **kwargs):
        event.return_value = ["!cmd - 显示指令列表"]

    @on(GetQQPersonCommand)
    @on(GetQQGroupCommand)
    def cmd_reload(self, event: EventContext, **kwargs):
        message: str = kwargs["message"]
        if message != "cmd":
            return
        event.prevent_postorder()
        reply = "[bot] 当前所有指令:\n\n"
        reply += "\n".join(self.emit(CmdCmdHelp))
        self.emit(Events.GetCQHTTP__).sendFriendMessage(
            user_id=kwargs["sender_id"],
            message=reply
        )
