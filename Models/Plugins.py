import logging
import sys


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
             can_reload: bool = True,
             **kwargs
             ):
    """注册插件, 此函数作为装饰器使用

    Args:
        description (str): 插件描述
        version (str): 插件版本
        author (str): 插件作者
        priority (int): 插件优先级
        enabled (bool): 插件是否启用
        can_reload (bool): 是否支持热重载
        kwargs: 剩余参数 所有键值对保存为字典存储在kwargs字段中

    Returns:
        None
    """
    return Plugin.register(description, version, author, priority, enabled, can_reload, **kwargs)


class Plugin:
    """插件基类"""

    plugin_list: list['Plugin'] = []
    """插件列表

    按插件优先级排序

    先读取, 然后按顺序初始化
    """

    need_initialize: bool = True
    """是否需要初始化"""

    hooks_dict: dict[str, list[callable]] = {}
    """事件处理器列表"""

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
    can_reload: bool
    """是否支持热重载"""
    path: str
    """插件路径"""
    kwargs: dict = {}
    """插件参数"""

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
                if cls.get_plugin_by_hook(hook).priority > cls.__plugin_priority__:
                    cls.hooks_dict[event].insert(index, func)
                    break
            else:
                cls.hooks_dict[event].append(func)

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
                 can_reload: bool = True,
                 **kwargs
                 ):
        """注册插件, 此函数作为装饰器使用

        Args:
            description (str): 插件描述
            version (str): 插件版本
            author (str): 插件作者
            priority (int): 插件优先级
            enabled (bool): 插件是否启用
            can_reload (bool): 是否支持热重载
            kwargs: 剩余参数 所有键值对保存为字典存储在kwargs字段中

        Returns:
            None
        """

        cls.__plugin_priority__ = priority

        def wrapper(plugin_cls: Plugin):
            plugin_cls.name = plugin_cls.__qualname__.split(".")[0]
            plugin_cls.description = description
            plugin_cls.version = version
            plugin_cls.author = author
            plugin_cls.priority = priority
            plugin_cls.hooks = cls.__plugin_hooks__
            plugin_cls.enabled = enabled
            plugin_cls.can_reload = can_reload
            plugin_cls.path = plugin_cls.__module__
            plugin_cls.kwargs = kwargs
            plugin_cls.enabled = True

            cls.__plugin_hooks__ = set()
            # 根据优先级加入 plugin_list
            for index, plugin in enumerate(cls.plugin_list):
                if plugin.priority > priority:
                    cls.plugin_list.insert(
                        index,
                        plugin_cls
                    )
                    if index > 0 and cls.plugin_list[index - 1].priority == priority:
                        logging.info("[warning] 插件优先级重复, 插件{}插入到插件{}之前".format(
                            plugin_cls.name, cls.plugin_list[index - 1].name
                        ))
                    break
            else:
                cls.plugin_list.append(plugin_cls)

            logging.info(
                f"插件注册完成: {plugin_cls.name=}, {description=}, {version=}, {author=}, {priority=}, ({plugin_cls})"
            )

            return plugin_cls

        return wrapper

    @classmethod
    def get_plugin_by_hook(cls, hook: callable) -> 'Plugin':
        """根据插件事件函数获取插件类(实例)"""
        return hook.__globals__[hook.__qualname__.split(".")[0]]

    @classmethod
    def emit(cls, event, **kwargs):
        """触发事件

        允许自定义事件
        """
        if event in cls.hooks_dict:
            for hook in cls.hooks_dict[event]:
                tmp_cls = cls.get_plugin_by_hook(hook)
                if tmp_cls.enabled:
                    hook(tmp_cls, event, **kwargs)
        else:
            logging.error(f"未注册事件: {event}")

    @classmethod
    def _initialize_plugins(cls):
        """初始化插件"""
        for index, plugin in enumerate(cls.plugin_list):
            if not plugin.need_initialize:
                continue
            try:
                cls.plugin_list[index] = plugin(cls.plugin_list)
            except:
                try:
                    cls.plugin_list[index] = plugin()
                except:
                    logging.error(f"插件{plugin.name}初始化时发生错误: {sys.exc_info()}")

    def __init__(self):
        """Plugin不初始化, 子类自行实现该方法"""
        pass

    def __del__(self):
        """程序异常时尝试释放资源"""
        pass
