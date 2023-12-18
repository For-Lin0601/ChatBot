import importlib
import logging
import os
import pkgutil
import sys
import traceback

from Events import *


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
        enabled (bool): 插件是否启用
        kwargs: 剩余参数 所有键值对保存为字典存储在`kwargs`字段中

    return:
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

    hooks_dict: dict[str: list[list[int, callable]]] = {}
    """事件处理器列表

    调用请用`self.emit(str)`
    ```python
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
    ```"""

    cid = 0
    """类id标识, 自动获取, 用作抽象函数寻找对应类实例的标识"""
    name: str = "Plugin"
    """插件名称(自动获取类名)"""
    description: str = "主线程"
    """插件描述"""
    version: str = "1.0.0"
    """插件版本"""
    author: str = "For_Lin0601"
    """插件作者"""
    priority: int = -float("inf")
    """插件优先级, 强烈建议不要使用默认值"""
    hooks: set = []
    """注册的事件"""
    enabled: bool = True
    """插件是否启用(初始化必执行, 仅判断是否响应`self.emit`)"""
    path: str = ""
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
    ```python
    {
        f"{plugin.name} {plugin.path}" = {  # 针对每个插件维护一个字典
            "set_reload_config": set_reload_config,  # 插件设定的保留值
        }
    }
    ```
    """

    _hooks_dict = {}
    """临时变量"""
    __plugin_hooks__ = set()
    """临时变量"""
    __plugin_priority__: int
    """临时变量, on()在注册的时候不会保存父类class的实例, 故在此临时保存"""

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
            enabled (bool): 插件是否启用
            kwargs: 剩余参数 所有键值对保存为字典存储在`kwargs`字段中

        return:
            None
        """
        cls.__plugin_priority__ = priority

        def wrapper(plugin_cls: Plugin):

            root_directory = os.path.dirname(
                os.path.dirname(os.path.abspath(__file__)))
            module_path = os.path.abspath(
                plugin_cls.__module__.replace('.', os.path.sep))
            plugin_cls.path = module_path.replace(root_directory, "")
            if not enabled:
                cls._hooks_dict = {}
                cls.__plugin_hooks__ = set()
                logging.warning(
                    f"插件{plugin_cls.__qualname__.split('.')[0]}被禁用")
                return
            for tmp_cls in cls.plugin_list:
                if plugin_cls.path == tmp_cls.path:
                    cls._hooks_dict = {}
                    cls.__plugin_hooks__ = set()
                    logging.warning(
                        f"插件重复注册, 插件{plugin_cls.__qualname__.split('.')[0]}已被注册(若为'尝试重新加载'则忽略)")
                    return

            plugin_cls.cid = cls.cid
            cls.cid += 1

            plugin_cls.hooks = cls.__plugin_hooks__
            cls.__plugin_hooks__ = set()

            plugin_cls.name = plugin_cls.__qualname__.split(".")[0]
            plugin_cls.description = description
            plugin_cls.version = version
            plugin_cls.author = author
            plugin_cls.priority = priority
            plugin_cls.enabled = enabled
            plugin_cls.kwargs = kwargs

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

            # 根据优先级加入cls.plugin_hooks[event]
            for event, lst in cls._hooks_dict.items():
                if event not in cls.hooks_dict:
                    cls.hooks_dict[event] = []
                for index, item in enumerate(cls.hooks_dict[event]):
                    tmp_cls = cls.get_plugin_by_cid(item[0])
                    if tmp_cls and tmp_cls.priority > cls.__plugin_priority__:
                        for _lst in lst:
                            cls.hooks_dict[event].insert(index, _lst)
                        break
                else:
                    for _lst in lst:
                        cls.hooks_dict[event].append(_lst)

                cls._hooks_dict = {}
                cls.__plugin_hooks__.add(plugin_cls)

            logging.info(
                f"插件注册完成: {plugin_cls.name=}, {description=}, {version=}, {author=}, {priority=}, ({plugin_cls})"
            )

            return plugin_cls

        return wrapper

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
            item = [cls.cid, func]  # [插件cid, 函数]
            if event not in cls._hooks_dict:
                cls._hooks_dict[event] = []
            cls._hooks_dict[event].append(item)

            return func

        return wrapper

    @classmethod
    def emit(self, event_name, **kwargs) -> 'EventContext.return_value':
        """触发事件

        允许自定义事件(用`self.emit()`调用)
        """
        event_context = EventContext(self, event_name)
        logging.debug(
            f"({event_context.eid})start事件[{event_name}]: 插件[{self.name}]触发事件")
        if event_name in self.hooks_dict:
            for hook in self.hooks_dict[event_name]:
                tmp_cls = self.get_plugin_by_cid(hook[0])
                try:
                    if tmp_cls.enabled:
                        logging.debug(
                            f"({event_context.eid})跟踪事件[{event_name}]: 插件[{tmp_cls.name}]已获取, 继续跟踪。")
                        hook[1](tmp_cls, event_context, **kwargs)
                        logging.debug(
                            f"({event_context.eid})跟踪事件[{event_name}]: 插件[{tmp_cls.name}]已归还, 继续跟踪。当前返回值: {event_context.return_value}")
                    else:
                        logging.debug(
                            f"({event_context.eid})跟踪事件[{event_name}]: 插件[{tmp_cls.name}]已禁用, 继续跟踪。")
                except Exception as e:
                    logging.error(
                        f"({event_context.eid})跟踪事件[{event_name}]: 插件[{tmp_cls.name}]响应事件时发生错误, 继续跟踪: \n{e}")
                if event_context.is_prevented_postorder():
                    logging.debug(
                        f"({event_context.eid})跟踪事件[{event_name}]: 被插件[{tmp_cls.name}]阻止。")
                    break
        else:
            logging.debug(f"({event_context.eid})跟踪事件[{event_name}]: 无人监听")
        logging.debug(
            f"({event_context.eid})跟踪事件[{event_name}]: 处理完毕, 停止跟踪。\n返回值: {event_context.return_value}")

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
        """设置为是否启用"""
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

    def on_reload(self):
        """热重载时触发, 配置可保留到`Plugin.__reload_config__`中, 详情请查看源码, 子类自行实现该方法"""
        pass

    def on_stop(self):
        """程序异常退出时尝试触发, 子类自行实现该方法"""
        pass

    @classmethod
    def _initialize_plugins(cls):
        """初始化插件"""
        for index, plugin in enumerate(cls.plugin_list):
            try:
                cls.plugin_list[index] = plugin()
            except Exception as e:
                if plugin.is_first_init(plugin):
                    logging.error(f"插件{plugin.name}初始化时发生错误: {e}")
                else:
                    logging.error(f"插件{plugin.name}热重载时发生错误: {e}")
        if cls.is_first_init(cls):
            cls.emit(PluginsLoadingFinished)

    @classmethod
    def _reload(cls):
        """热重载"""
        def walk(module, prefix='', path_prefix=''):
            """遍历并重载所有模块"""
            for item in pkgutil.iter_modules(module.__path__):
                if item.ispkg:
                    logging.debug(
                        "扫描插件包: plugins/{}".format(path_prefix + item.name))
                    walk(__import__(module.__name__ + '.' + item.name,
                         fromlist=['']), prefix + item.name + '.', path_prefix + item.name + '/')
                else:
                    try:
                        logging.debug('扫描插件模块: {}, 路径: {}'.format(
                            prefix + item.name, path_prefix + item.name + '.py'))
                        importlib.reload(__import__(
                            module.__name__ + '.' + item.name, fromlist=['']))
                        logging.info('热重载模块: {} 成功'.format(prefix + item.name))
                    except:
                        logging.error(
                            '热重载模块: {} 失败: {}'.format(prefix + item.name, sys.exc_info()))
                        traceback.print_exc()

        logging.critical("开始重载插件")
        for plugin in cls.plugin_list:
            try:
                plugin.on_reload()
            except Exception as e:
                logging.warning(f"插件 {plugin.name} 热重载时发生错误: {e}")
        cls.cid = 0
        cls.plugin_list = []
        cls.hooks_dict = {}
        cls.__plugin_hooks__ = set()
        cls.__is_first_init__ = False
        walk(__import__('plugins'))
        Plugin._initialize_plugins()
        Plugin.emit(PluginsReloadFinished)
        Plugin.__reload_config__ = {}
        logging.critical("插件热重载完成")

    @classmethod
    def _stop(cls):
        for plugin in cls.plugin_list:
            try:
                plugin.on_stop()
            except:
                logging.warning(f"插件 {plugin.name} 停止时发生错误")


class EventContext:
    """事件上下文"""
    eid = 0
    """事件编号"""

    name = ""
    """事件名( Events.py 中存放的字段)"""

    plugin = None
    """事件所属插件(可能为`Plugin`)"""

    return_value = None
    """返回值参考`Event.py`自行确认"""

    __prevent_postorder__ = False
    """是否阻止后续插件的执行"""

    def prevent_postorder(self):
        """阻止后续插件执行"""
        self.__prevent_postorder__ = True

    def is_prevented_postorder(self):
        """是否阻止后序插件执行"""
        return self.__prevent_postorder__

    def __init__(self, plugin, name: str):
        self.name = name
        self.plugin = plugin
        self.eid = EventContext.eid
        self.__prevent_postorder__ = False
        self.return_value = None
        EventContext.eid += 1
