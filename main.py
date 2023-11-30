# 插件管理模块
import logging
import importlib
import pkgutil
import sys
import traceback
from Events import PluginsLoadingFinished

from Models.Plugins import Plugin


def walk_plugin_path(module, prefix='', path_prefix=''):

    for item in pkgutil.iter_modules(module.__path__):
        if item.ispkg:
            logging.debug(
                "扫描插件包: plugins/{}".format(path_prefix + item.name))
            walk_plugin_path(__import__(module.__name__ + '.' + item.name, fromlist=['']),
                             prefix + item.name + '.', path_prefix + item.name + '/')
        else:
            try:
                logging.debug(
                    "扫描插件模块: plugins/{}".format(path_prefix + item.name + '.py'))

                importlib.import_module(module.__name__ + '.' + item.name)
                logging.info(
                    '加载模块: plugins/{} 成功'.format(path_prefix + item.name + '.py'))
            except:
                logging.error(
                    '加载模块: plugins/{} 失败: {}'.format(path_prefix + item.name + '.py', sys.exc_info()))
                traceback.print_exc()


def load_plugins():
    """加载插件"""
    try:
        import log_start
        log_start.LogStart.reset_logging()
    except:
        print("日志加载失败")
    logging.info("加载插件")

    walk_plugin_path(__import__('plugins'))

    def logging_debug():
        res = f"{Plugin.plugin_list}"
        for plugin in Plugin.plugin_list:
            res += f"{plugin.hooks, plugin.path, plugin.priority}"
        res += f"{Plugin.hooks_dict}"
        return res

    Plugin._initialize_plugins()
    logging.debug(logging_debug())

    Plugin.emit(PluginsLoadingFinished, plugins=Plugin.plugin_list)
    import Models.reload as reload
    while 1:
        reload.reload()
        logging.debug(logging_debug())
        1


if __name__ == '__main__':
    load_plugins()
