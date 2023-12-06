
from typing import Union
import Events
from Models.Plugins import *
from plugins.gocqOnQQ.CQHTTP_Protocol.CQHTTP_Protocol import CQHTTP_Protocol
from plugins.gocqOnQQ.QQevents.MessageEvent import PersonMessage, GroupMessage


@register(
    description="命令基类",
    version="1.0.0",
    author="For_Lin0601",
    priority=100
)
class CmdModel(Plugin):

    def __init__(self):
        pass

    @on(QQ_private_message)
    def check_cmd(self, event: EventContext,  **kwargs):
        message: Union[PersonMessage, GroupMessage] = kwargs["QQevents"]
        self.CQHTTP: CQHTTP_Protocol = self.emit(GetCQHTTP__)
        if message.message[0].text == "reload":
            logging.critical("开始插件热重载")
            self.emit(Events.SubmitSysTask__, fn=Plugin._reload)
        elif message.message[0].text == "get":
            self.CQHTTP.sendFriendMessage(1636708665, "fuck")

    def on_reload(self):
        pass
