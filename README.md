# ChatBot

a fucking ChatBot link QQ, weChat to GPT.

# 1. 主线程流程

启动主程序后

1. 加载 log 和 config
2. 加载所有[插件基类](#2-插件基类编写规范plugin)
3. while True: time.sleep(6000)不返回

   如果意外出错，在这里做配置保存等

# 2. 插件基类编写规范(`Plugin`)

1. 插件基类应当有`__init__`, `__del__`两个基础函数用于注册和注销插件(多为热重载的时候注销)

2. 每个插件基类只会被实例化一次

3. 与实例基类不同的是，插件中的函数应被`Model.on`或者`Plugin.on`注册，否则函数不会被实例直接触发

4. 所有与实例的交互都应该从`Model.ModelList`中获取，所有和插件的交互应该从`Plugin.PluginList`中获取

```python
import Model.ModelList
import Plugin.PluginList  # 可能从插件列表获取事件

class Plugin:
    def emit(self, event_type):
        """根据优先级触发事件"""
        pass

    def register(self, *args, **kwargs):  # TODO 尚未决定需要多少参数
        """注册插件"""


@register(
    name: str = "MyModel",
    description: str = "实例基类编写参考",
    aliases: list[str] = [],  # 别名，或缩写
    version: str = "1.0",  # 版本
    author: str,  # 作者
    priority: int = 0,  # 优先级(0~999) 可重复，但执行顺序不一定
    # 可能还需要一个参数列表之类的？后面再说
)
class MyBotPlugin(Plugin):
    def __init__(self):
        """初始化"""
        self.bot = ModelList.get(MyBotModel)

    # 举例子
    #
    # PersonMessageReceived = "person_message_received"
    # 收到好游戏聊消息
    # kwargs:
    #   send_id: 发送人
    #   message: 发送的消息
    # return:
    #   None
    #
    # event: EventContent
    # 事件上下文，保存了事件编号，事件名字，是否阻止后续插件行为等。调用函数修改，不用返回
    @self.bot.on(PersonMessageReceived)
    def _(self, event: EventContent, **kwargs):
        self.bot.print_message(kwargs['send_id'], f"获取到私聊消息：{kwargs['message']}")

    def __del__(self):
        """热重载"""
        pass
```

-100: **config
-99: **log
