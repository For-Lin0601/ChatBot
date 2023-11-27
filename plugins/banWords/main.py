from Models.Plugins import *

# 注册插件


@register(
    description="敏感词屏蔽",
    version="0.1",
    author="For_Lin0601.002",
    priority=1,
)
class banWordsPlugin(Plugin):

    # 插件加载时触发
    # plugin_host (pkg.plugin.host.PluginHost) 提供了与主程序交互的一些方法，详细请查看其源码
    def __init__(self, plugin_host):
        print("插件 TimedReminder 已加载")

    @on("timed_reminder")
    def _1(self, event):
        print("测试敏感词timereminder")

    @on("PersonMessage")
    def _2(self, event):
        print("[敏感词]好友消息")

    # 插件卸载时触发
    def __del__(self):
        pass
