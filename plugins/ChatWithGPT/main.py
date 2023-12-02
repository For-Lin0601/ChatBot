from Models.Plugins import *

# 注册插件


@register(
    description="和ChatGPT聊天",
    version="1.0",
    author="For_Lin0601",
    priority=100
)
class ChatModel(Plugin):

    # 插件加载时触发
    # plugin_list 提供了全部插件列表，详细请查看其源码
    def __init__(self):
        print("插件 Chat 已加载")

    @on("PersonMessage")
    def _3(self, event: EventContext,  **kwargs):
        print("GPT好友消息")

    # 插件热重载时触发
    def on_reload(self):
        pass
