from Models.Plugins import *

# 注册插件


@Plugin.register(
    description="和ChatGPT聊天",
    version="1.0",
    author="For_Lin0601_001",
    priority=100
)
class ChatPlugin(Plugin):

    # 插件加载时触发
    # plugin_host (pkg.plugin.host.PluginHost) 提供了与主程序交互的一些方法，详细请查看其源码
    def __init__(self, plugin_host):
        print("插件 Chat 已加载")


    @on("PersonMessage")
    def _3(self, event):
        print("GPT好友消息")

    # 插件卸载时触发
    def __del__(self):
        pass
