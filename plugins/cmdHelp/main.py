

import Events
from Models.Plugins import *


@register(
    description="显示自定义的帮助信息[help]",
    version="1.0.0",
    author="For_Lin0601",
    priority=202
)
class HelpCommand(Plugin):

    @on(CmdCmdHelp)
    def help(self, event: EventContext, **kwargs):
        event.return_value["help"] = {
            "is_admin": False,
            "alias": [],
            "summary": "显示自定义的帮助信息",
            "usage": "!help",
            "description": "机器人操作指南, 新手入门手册"
        }

    @on(GetQQPersonCommand)
    @on(GetQQGroupCommand)
    def cmd_help(self, event: EventContext, **kwargs):
        message: str = kwargs["message"].strip()
        if message != "help":
            return
        event.prevent_postorder()
        self.emit(Events.GetCQHTTP__).sendPersonMessage(
            user_id=kwargs["group_id"],
            message=self.emit(Events.GetConfig__).help_message
        )

    @on(GetWXCommand)
    def wx_send(self, event: EventContext, **kwargs):
        message: str = kwargs["command"].strip()
        if message != "help":
            return
        event.prevent_postorder()
        self.emit(Events.GetWCF__).send_text(
            self.emit(Events.GetConfig__).help_message,
            kwargs["roomid"] if kwargs["roomid"] else kwargs["sender"]
        )
