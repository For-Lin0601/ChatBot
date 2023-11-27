# 插件管理模块
import logging
import importlib
import os
import pkgutil
import sys
import shutil
import traceback

from Models.Plugins import Plugin


def walk_plugin_path(module, prefix='', path_prefix=''):
    __current_module_path__ = ""
    """遍历插件路径"""

    def _walk_plugin_path(module, prefix='', path_prefix=''):
        for item in pkgutil.iter_modules(module.__path__):
            if item.ispkg:
                logging.debug(
                    "扫描插件包: plugins/{}".format(path_prefix + item.name))
                _walk_plugin_path(__import__(module.__name__ + '.' + item.name, fromlist=['']),
                                  prefix + item.name + '.', path_prefix + item.name + '/')
            else:
                try:
                    logging.debug(
                        "扫描插件模块: plugins/{}".format(path_prefix + item.name + '.py'))
                    __current_module_path__ = "plugins/"+path_prefix + item.name + '.py'

                    importlib.import_module(module.__name__ + '.' + item.name)
                    logging.info(
                        '加载模块: plugins/{} 成功'.format(path_prefix + item.name + '.py'))
                except:
                    logging.error(
                        '加载模块: plugins/{} 失败: {}'.format(path_prefix + item.name + '.py', sys.exc_info()))
                    traceback.print_exc()

    _walk_plugin_path(module, prefix, path_prefix)


def load_plugins():
    """加载插件"""
    logging.basicConfig(level=logging.DEBUG)
    logging.info("加载插件")
    # logging.basicConfig(level=logging.DEBUG)

    walk_plugin_path(__import__('plugins'))

    def logging_debug():
        res = ''

        res += f"{Plugin.plugin_list}"
        for plugin in Plugin.plugin_list:
            res += f"{plugin.hooks, plugin.path, plugin.priority}"
        res += f"{Plugin.hooks_dict}"
        return res
    logging.debug(logging_debug())

    Plugin._initialize_plugins()
    logging.debug(logging_debug())

    Plugin.emit('timed_reminder')


def install_plugin(repo_url: str):
    """安装插件, 从git储存库获取并解决依赖"""
    try:
        import pkg.utils.pkgmgr
        pkg.utils.pkgmgr.ensure_dulwich()
    except:
        pass

    try:
        import dulwich
    except ModuleNotFoundError:
        raise Exception(
            "dulwich模块未安装,请查看 https://github.com/RockChinQ/QChatGPT/issues/77")

    from dulwich import porcelain

    logging.info("克隆插件储存库: {}".format(repo_url))
    repo = porcelain.clone(
        repo_url, "plugins/"+repo_url.split(".git")[0].split("/")[-1]+"/", checkout=True)

    # 检查此目录是否包含requirements.txt
    if os.path.exists("plugins/"+repo_url.split(".git")[0].split("/")[-1]+"/requirements.txt"):
        logging.info("检测到requirements.txt, 正在安装依赖")
        import pkg.utils.pkgmgr
        pkg.utils.pkgmgr.install_requirements(
            "plugins/"+repo_url.split(".git")[0].split("/")[-1]+"/requirements.txt")

        import pkg.utils.log as log
        log.reset_logging()


def uninstall_plugin(plugin_name: str) -> str:
    """卸载插件"""
    if plugin_name not in __plugins__:
        raise Exception("插件不存在")

    # 获取文件夹路径
    plugin_path = __plugins__[plugin_name]['path'].replace("\\", "/")

    # 剪切路径为plugins/插件名
    plugin_path = plugin_path.split("plugins/")[1].split("/")[0]

    # 删除文件夹
    shutil.rmtree("plugins/"+plugin_path)
    return "plugins/"+plugin_path


class EventContext:
    """事件上下文"""
    eid = 0
    """事件编号"""

    name = ""

    __prevent_default__ = False
    """是否阻止默认行为"""

    __prevent_postorder__ = False
    """是否阻止后续插件的执行"""

    __return_value__ = {}
    """ 返回值 
    示例:
    {
        "example": [
            'value1',
            'value2',
            3,
            4,
            {
                'key1': 'value1',
            },
            ['value1', 'value2']
        ]
    }
    """

    def add_return(self, key: str, ret):
        """添加返回值"""
        if key not in self.__return_value__:
            self.__return_value__[key] = []
        self.__return_value__[key].append(ret)

    def get_return(self, key: str):
        """获取key的所有返回值"""
        if key in self.__return_value__:
            return self.__return_value__[key]
        return None

    def get_return_value(self, key: str):
        """获取key的首个返回值"""
        if key in self.__return_value__:
            return self.__return_value__[key][0]
        return None

    def prevent_default(self):
        """阻止默认行为"""
        self.__prevent_default__ = True

    def prevent_postorder(self):
        """阻止后续插件执行"""
        self.__prevent_postorder__ = True

    def is_prevented_default(self):
        """是否阻止默认行为"""
        return self.__prevent_default__

    def is_prevented_postorder(self):
        """是否阻止后序插件执行"""
        return self.__prevent_postorder__

    def __init__(self, name: str):
        self.name = name
        self.eid = EventContext.eid
        self.__prevent_default__ = False
        self.__prevent_postorder__ = False
        self.__return_value__ = {}
        EventContext.eid += 1

class PluginHost:
    """插件宿主"""

    def __init__(self):
        pass

    def emit(self, event_name: str, **kwargs) -> EventContext:
        """触发事件"""
        import json

        event_context = EventContext(event_name)
        logging.debug("触发事件: {} ({})".format(event_name, event_context.eid))
        for plugin in iter_plugins():

            if not plugin['enabled']:
                continue

            # if plugin['instance'] is None:
            #     # 从关闭状态切到开启状态之后, 重新加载插件
            #     try:
            #         plugin['instance'] = plugin["class"](plugin_host=self)
            #         logging.info("插件 {} 已初始化".format(plugin['name']))
            #     except:
            #         logging.error("插件 {} 初始化时发生错误: {}".format(plugin['name'], sys.exc_info()))
            #         continue

            if 'hooks' not in plugin or event_name not in plugin['hooks']:
                continue

            hooks = []
            if event_name in plugin["hooks"]:
                hooks = plugin["hooks"][event_name]
            for hook in hooks:
                try:
                    already_prevented_default = event_context.is_prevented_default()

                    kwargs['event'] = event_context

                    hook(plugin['instance'], **kwargs)

                    if event_context.is_prevented_default() and not already_prevented_default:
                        logging.debug("插件 {} 已要求阻止事件 {} 的默认行为".format(
                            plugin['name'], event_name))

                except Exception as e:
                    logging.error("插件{}触发事件{}时发生错误".format(
                        plugin['name'], event_name))
                    logging.error(traceback.format_exc())

            # print("done:{}".format(plugin['name']))
            if event_context.is_prevented_postorder():
                logging.debug("插件 {} 阻止了后序插件的执行".format(plugin['name']))
                break

        logging.debug("事件 {} ({}) 处理完毕, 返回值: {}".format(event_name, event_context.eid,
                                                        event_context.__return_value__))

        return event_context


if __name__ == '__main__':
    load_plugins()
