from Models.Plugins import *

# 注册插件


@register(
    description="GBT链接类",
    version="1.0.0",
    author="For_Lin0601",
    priority=10,
)
class GPTBot(Plugin):

    # 插件加载时触发
    # plugin_list 提供了全部插件列表，详细请查看其源码
    def __init__(self):
        print("插件 GBT 已加载")

    # 插件热重载时触发
    def on_reload(self):
        pass
