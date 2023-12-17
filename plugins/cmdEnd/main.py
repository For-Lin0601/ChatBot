

import Events
from Models.Plugins import *


@register(
    description="结尾指令, 若到大啊此处则表明无命令响应",
    version="1.0.0",
    author="For_Lin0601",
    priority=10000
)
class EndCommand(Plugin):

    @on(GetQQPersonCommand)
    def cmd_end(self, event: EventContext, **kwargs):
        message: str = kwargs["message"]
        event.prevent_postorder()
        self.emit(Events.GetCQHTTP__).sendPersonMessage(
            user_id=kwargs["sender_id"],
            message=f"[bot]err: 无命令响应: !{message}"
        )

    @on(GetQQGroupCommand)
    def cmd_end(self, event: EventContext, **kwargs):
        message: str = kwargs["message"]
        event.prevent_postorder()
        self.emit(Events.GetCQHTTP__).sendGroupMessage(
            group_id=kwargs["launcher_id"], message=f"[bot]err: 无命令响应: !{message}"
        )

    @on(GetWXCommand)
    def cmd_end(self, event: EventContext, **kwargs):
        message: str = kwargs["command"]
        event.prevent_postorder()
        self.emit(Events.GetWCF__).send_text(
            msg=f"[bot]err: 无命令响应: !{message}",
            receiver=kwargs["roomid"] if kwargs["roomid"] else kwargs["sender"]
        )
