import logging
import os


def on(event: str):
    """注册事件监听器
    :param
        event: str 事件名称
    """
    return Plugin.on(event)


def register(description: str,
             version: str,
             author: str,
             priority: int = 100,
             enabled: bool = True,
             **kwargs
             ):
    """注册插件, 此函数作为装饰器使用

    Args:
        description (str): 插件描述
        version (str): 插件版本
        author (str): 插件作者
        priority (int): 插件优先级
        enabled (bool): 插件是否启用(只影响`Plugin.emit`的调用, 即插件会被实例化)
        kwargs: 剩余参数 所有键值对保存为字典存储在`kwargs`字段中

    Returns:
        None
    """
    return Plugin.register(description, version, author, priority, enabled, **kwargs)


class Plugin:
    """插件基类"""

    plugin_list: list['Plugin'] = []
    """插件列表

    按插件优先级排序

    先读取, 然后按顺序初始化
    """

    hooks_dict: dict[str, list[list[int, callable]]] = {}
    """事件处理器列表

    调用请用`Plugin.emit(str)`

    例如: {
        "group_normal_message_received": [              # 事件名
            [0, <function check_message at 0x000001>],  # 第一项为类的`cid`标识, 第二项为函数
            [1, <function reply_group at 0x000002>],    # 注意`cid`标识不等同于`priority`优先级, 故此处日志较为奇怪
        ],
        "person_normal_message_received": [
            [0, <function check_message at 0x000003>],
            [1, <function reply_person at 0x000004>],
        ]
    }
    """

    cid = 0
    """类id标识, 自动获取, 用作抽象函数寻找对应类实例的标识"""
    name: str
    """插件名称(自动获取类名)"""
    description: str
    """插件描述"""
    version: str
    """插件版本"""
    author: str
    """插件作者"""
    priority: int
    """插件优先级, 强烈建议不要使用默认值"""
    hooks: set
    """注册的事件"""
    enabled: bool
    """插件是否启用(初始化必执行, 启用请看函数 TODO )"""
    path: str
    """插件路径(class Y extends Plugin 所在的文件夹)"""
    kwargs: dict = {}
    """插件参数"""

    __is_first_init__ = True
    """是否为首次加载(热重载判断)

    调用: `self.is_first_init()` -> bool
    """
    __reload_config__: dict = {}
    """热重载结束后重置此字典(`PluginsReloadFinished`触发前)

    用 set_reload_config(), get_reload_config() 调用

    内部形如:
    ```py
    {
        f"{plugin.name} {plugin.path}" = {           # 针对每个插件维护一个字典
            "set_reload_config": set_reload_config,  # 插件保留值
        }
    }
    ```
    """

    __plugin_hooks__ = set()
    """临时变量"""
    __plugin_priority__: int
    """临时变量, on()在注册的时候不会保存父类class的实例, 故在此临时保存"""

    @classmethod
    def on(cls, event: str):
        """事件处理器装饰器

        :param
            event: 事件类型
        :return:
            None
        """
        def wrapper(func):
            """事件处理器"""

            if event not in cls.hooks_dict:
                cls.hooks_dict[event] = []
            # 根据优先级加入cls.plugin_hooks[event]
            for index, hook in enumerate(cls.hooks_dict[event]):
                tmp_cls = cls.get_plugin_by_cid(hook[0])
                if tmp_cls and tmp_cls.priority > cls.__plugin_priority__:
                    cls.hooks_dict[event].insert(index, [cls.cid, func])
                    break
            else:
                cls.hooks_dict[event].append([cls.cid, func])

            cls.__plugin_hooks__.add(func)

            return func

        return wrapper

    @classmethod
    def register(cls,
                 description: str,
                 version: str,
                 author: str,
                 priority: int = 100,
                 enabled: bool = True,
                 **kwargs
                 ):
        """注册插件, 此函数作为装饰器使用

        Args:
            description (str): 插件描述
            version (str): 插件版本
            author (str): 插件作者
            priority (int): 插件优先级
            enabled (bool): 插件是否启用(只影响`Plugin.emit`的调用, 即插件会被实例化)
            kwargs: 剩余参数 所有键值对保存为字典存储在`kwargs`字段中

        Returns:
            None
        """
        cls.__plugin_priority__ = priority

        def wrapper(plugin_cls: Plugin):
            plugin_cls.cid = cls.cid
            plugin_cls.name = plugin_cls.__qualname__.split(".")[0]
            plugin_cls.description = description
            plugin_cls.version = version
            plugin_cls.author = author
            plugin_cls.priority = priority
            plugin_cls.hooks = cls.__plugin_hooks__
            plugin_cls.enabled = enabled
            plugin_cls.path = os.path.join(
                os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                plugin_cls.__module__.replace(
                    '.', os.path.sep).rsplit(os.path.sep, 1)[0]
            ).capitalize()
            plugin_cls.kwargs = kwargs

            cls.cid += 1
            cls.__plugin_hooks__ = set()
            # 根据优先级加入 plugin_list
            for index, plugin in enumerate(cls.plugin_list):
                if plugin.priority > priority:
                    cls.plugin_list.insert(
                        index,
                        plugin_cls
                    )
                    if index > 0 and cls.plugin_list[index - 1].priority == priority:
                        logging.warning(
                            f"插件优先级重复, 插件{plugin_cls.name}插入到插件{cls.plugin_list[index - 1].name}之后"
                        )
                    break
            else:
                cls.plugin_list.append(plugin_cls)

            logging.info(
                f"插件注册完成: {plugin_cls.name=}, {description=}, {version=}, {author=}, {priority=}, ({plugin_cls})"
            )

            return plugin_cls

        return wrapper

    @classmethod
    def emit(cls, event_name, **kwargs) -> 'EventContext.return_value':
        """触发事件

        允许自定义事件(可以用`self.emit()`, 但希望用`Plugin.emit()`)
        """
        event_context = EventContext(event_name)
        if event_name in cls.hooks_dict:
            for hook in cls.hooks_dict[event_name]:
                tmp_cls = cls.get_plugin_by_cid(hook[0])
                try:
                    if tmp_cls.enabled:
                        hook[1](tmp_cls, event_context, **kwargs)
                except Exception as e:
                    logging.error(
                        f"插件 {tmp_cls.name} 触发事件 {event_name} 时发生错误: {e}")
                if not event_context.is_prevented_postorder():
                    logging.debug(
                        f"事件 {event_name} ({event_context.eid}) 被插件 {tmp_cls.name} 阻止")
                    break
        else:
            logging.debug(f"事件'{event_name}'无人应答")
        logging.debug(
            f"事件 {event_name} ({event_context.eid}) 处理完毕, 返回值: {event_context.return_value}")

        return event_context.return_value

    @classmethod
    def get_plugin_by_cid(cls, cid) -> 'Plugin':
        """根据插件类标识获取插件类(实例)"""
        for plugin in cls.plugin_list:
            if plugin.cid == cid:
                return plugin
        return None

    @classmethod
    def get_plugin_by_name(cls, name: str) -> 'Plugin':
        """根据插件名获取插件类(实例) [不安全函数!]

        请自行确认插件名不冲突, 否则返回第一个符合条件的值

        找不到则返回 None
        """
        for plugin in cls.plugin_list:
            if plugin.name == name:
                return plugin
        return None

    def is_first_init(self) -> bool:
        """是否为首次加载"""
        return self.__is_first_init__

    def is_enabled(self) -> bool:
        """是否启用"""
        return self.enabled

    def set_enabled(self, enabled: bool):
        """是否启用"""
        self.enabled = enabled

    def set_reload_config(self, key, value):
        """每个插件拥有自己的 kwargs 字典"""
        tmp_cls_name = f"{self.name=} {self.path=}"
        if tmp_cls_name in Plugin.__reload_config__:
            Plugin.__reload_config__[tmp_cls_name][key] = value
        else:
            Plugin.__reload_config__[tmp_cls_name] = {key: value}

    def get_reload_config(self, key=None):
        """每个插件拥有自己的 kwargs 字典, 有key返回值, 无key返回整个字典"""
        tmp_cls_name = f"{self.name=} {self.path=}"
        if tmp_cls_name not in Plugin.__reload_config__:
            return None
        if key:
            if key not in Plugin.__reload_config__[tmp_cls_name]:
                return None
            return Plugin.__reload_config__[tmp_cls_name][key]
        return Plugin.__reload_config__[tmp_cls_name]

    def __init__(self):
        """Plugin不初始化, 子类自行实现该方法"""
        pass

    def __del__(self):
        """热重载时触发, 配置可保留到`Plugin.__reload_config__`中, 详情请查看源码, 子类自行实现该方法"""
        pass

    def __stop__(self):
        """程序异常退出时尝试触发, 子类自行实现该方法"""
        pass

    @classmethod
    def _initialize_plugins(cls):
        """初始化插件"""
        for index, plugin in enumerate(cls.plugin_list):
            try:
                cls.plugin_list[index] = plugin()
            except Exception as e:
                if plugin.is_first_init():
                    logging.error(f"插件{plugin.name}初始化时发生错误: {e}")
                else:
                    logging.error(f"插件{plugin.name}热重载时发生错误: {e}")

    @classmethod
    def _reload(cls):
        cls.__is_first_init__ = False
        cls.cid = 0
        cls.plugin_list = []
        cls.hooks_dict = {}
        cls.__plugin_hooks__ = set()

    @classmethod
    def _stop(cls):
        for plugin in cls.plugin_list:
            try:
                plugin.__stop__(plugin)
            except:
                logging.warning(f"插件 {plugin.name} 停止时发生错误")


class EventContext:
    """事件上下文"""
    eid = 0
    """事件编号"""

    name = ""
    """事件名( Events.py 中存放的字段)"""

    __prevent_postorder__ = False
    """是否阻止后续插件的执行"""

    return_value = None
    """返回值参考 Event.py"""

    def prevent_postorder(self):
        """阻止后续插件执行"""
        self.__prevent_postorder__ = True

    def is_prevented_postorder(self):
        """是否阻止后序插件执行"""
        return self.__prevent_postorder__

    def __init__(self, name: str):
        self.name = name
        self.eid = EventContext.eid
        self.__prevent_postorder__ = False
        self.return_value = None
        EventContext.eid += 1
