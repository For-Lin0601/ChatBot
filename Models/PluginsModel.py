import logging


__plugins__ = []

def on(event: str):
    """注册事件监听器
    :param
        event: str 事件名称
    """
    return Plugin.on(event)


__current_registering_plugin__ = ""


class Plugin:
    """插件基类"""

    host: host.PluginHost
    """插件宿主，提供插件的一些基础功能"""

    @classmethod
    def on(cls, event):
        """事件处理器装饰器

        :param
            event: 事件类型
        :return:
            None
        """
        global __current_registering_plugin__

        def wrapper(func):
            plugin_hooks = __plugins__[
                __current_registering_plugin__]["hooks"]

            if event not in plugin_hooks:
                plugin_hooks[event] = []
            plugin_hooks[event].append(func)

            # print("registering hook: p='{}', e='{}', f={}".format(__current_registering_plugin__, event, func))

            __plugins__[
                __current_registering_plugin__]["hooks"] = plugin_hooks

            return func

        return wrapper


def register(name: str, description: str, version: str, author: str):
    """注册插件, 此函数作为装饰器使用

    Args:
        name (str): 插件名称
        description (str): 插件描述
        version (str): 插件版本
        author (str): 插件作者

    Returns:
        None
    """
    global __current_registering_plugin__

    __current_registering_plugin__ = name
    # print("registering plugin: n='{}', d='{}', v={}, a='{}'".format(name, description, version, author))
    __plugins__[name] = {
        "name": name,
        "description": description,
        "version": version,
        "author": author,
        "hooks": {},
        "path": __current_module_path__,
        "enabled": True,
        "instance": None,
    }

    def wrapper(cls: Plugin):
        cls.name = name
        cls.description = description
        cls.version = version
        cls.author = author
        cls.host = pkg.utils.context.get_plugin_host()
        cls.enabled = True
        cls.path = __current_module_path__

        # 存到插件列表
        __plugins__[name]["class"] = cls

        logging.info("插件注册完成: n='{}', d='{}', v={}, a='{}' ({})".format(
            name, description, version, author, cls))

        return cls

    return wrapper
