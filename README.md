# ChatBot

a fucking ChatBot on QQ, weChat and GPT.

# 1. 主线程流程

启动主程序后

1. 加载 config.py
2. 加载所有[实例基类](#2-实例基类编写规范model)
3. 加载所有[插件基类](#3-插件基类编写规范plugin)
4. while True: time.sleep(6000)不返回

   如果意外出错，在这里做配置保存等

# 2. 实例基类编写规范(`Model`)

1. 实例基类应当有`__init__`, `__del__`两个基础函数用于注册和注销实例(多为热重载的时候注销)

2. 应当有`on()`方法用于注册后续插件事件处理

   并在后续代码中用`emit()`方法调用事件处理

3. 每个实例基类只会被实例化一次

4. 此外与插件交互规范应当写在同目录下.md 文件中

```python
class Model:
    def emit(self, event_type):
        """根据优先级触发事件"""
        pass

    def register(self, *args, **kwargs):  # TODO 尚未决定需要多少参数
        """注册实例基类"""


@Model.register(
    name: str = "MyBotModel",
    description: str = "实例基类编写参考",
    version: str = "1.0",  # 版本
    author: str,  # 作者
)
class MyBotModel(Model):
    def __init__(self):
        """初始化"""
        pass

    def on(
        self,
        event_type: Union[Type[Event], str],
        priority: int = 0,
    ) -> Callable:  # TODO 搞不好封装到Model层里面去
        """注册事件处理器。
        Args:
            event_type: 事件类或事件名。
            priority: 优先级，较小者优先。
        """
        pass

    def print_message(self, target, message):
        """示例函数，此处可自行修改实现
        统一接口规范，插件可获取此处的实例，调用函数实现与外界交互
        """
        print(f"向用户{target}发送信息：{message}")

    def __del__(self):
        """热重载"""
        pass
```

# 3. 插件基类编写规范(`Plugin`)

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
        """注册插件基类"""


Plugin.register(
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

### ~~此外也允许插件注册插件事件"`on()`"和触发插件事件"`emit()`"，但还请注意优先级~~
