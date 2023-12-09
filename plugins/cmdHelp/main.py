

import Events
from Models.Plugins import *


@register(
    description="热重载[re, reload]",
    version="1.0.0",
    author="For_Lin0601",
    priority=202,
)
class HelpPlugin(Plugin):

    def __init__(self):
        pass

    def on_reload(self):
        pass

    def on_stop(self):
        pass

    @on(CmdCmdHelp)
    def help(self, event: EventContext, **kwargs):
        event.return_value.append(
            "!help - 显示自定义的帮助信息"
        )

    @on(GetQQPersonCommand)
    @on(GetQQGroupCommand)
    def cmd_reload(self, event: EventContext, **kwargs):
        message: str = kwargs["message"]
        if message != "help":
            return
        event.prevent_postorder()
        self.emit(Events.GetCQHTTP__).sendFriendMessage(
            user_id=kwargs["sender_id"],
            message=self.emit(Events.GetConfig__).help_message
        )
