

from Events import *
from Models.Plugins import *


@register(
    description="定时提醒",
    version="0.1",
    author="For_Lin0601",
    priority=10,
)
class TimeReminderPlugin(Plugin):

    # 插件加载时触发
    # plugin_list 提供了全部插件列表, 详细请查看其源码
    def __init__(self):
        print("插件 TimedReminder 已加载")

    @on("fuck")
    def _1(self, event):
        print("定时提醒")

    @on("PersonMessage")
    def _2(self, event):
        print("好友消息")

    # 插件卸载时触发
    def on_reload(self):
        pass
