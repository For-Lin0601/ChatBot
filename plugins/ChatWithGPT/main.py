
import Events
from Models.Plugins import *
from plugins.gocqOnQQ.QQevents.MessageEvent import PersonMessage


@register(
    description="和ChatGPT聊天",
    version="1.0.0",
    author="For_Lin0601",
    priority=100
)
class ChatModel(Plugin):

    def __init__(self):
        pass

    @on("QQ_private_message")
    def check_admin(self, event: EventContext,  **kwargs):
        person_message: PersonMessage = kwargs["QQevents"]
        if person_message.message == "reload":
            logging.debug("开始插件热重载！！！！！！！！！！！！！")
            self.emit(Events.SubmitSysTask__, fn=Plugin._reload)

    def on_reload(self):
        pass
