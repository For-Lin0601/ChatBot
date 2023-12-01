# 插件管理模块
import logging
import importlib
import os
import pkgutil
import sys
import time
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


def logging_test():
    res = "插件列表:"
    for plugin in Plugin.plugin_list:
        res += f"\n\n{plugin=}"
        res += f"\n{plugin.cid=}, {plugin.name=},{plugin.priority=}, {plugin.description=}, {plugin.version=}, {plugin.author=}"
        res += f"\n{plugin.enabled=}, {plugin.path=}"
        res += f"\n{plugin.hooks=}"
    res += "\n\n\nPlugin.hooks_dict: "
    for key in Plugin.hooks_dict:
        res += f"\n{key}: {Plugin.hooks_dict[key]}"
    return res


def load_plugins():
    """加载插件"""
    try:
        import log_start
        log_start.LogStart.reset_logging()
    except:
        print("日志加载失败")
    logging.info("加载插件")

    walk_plugin_path(__import__('plugins'))

    Plugin._initialize_plugins()
    logging.debug(logging_test())  # TODO

    Plugin.emit(PluginsLoadingFinished)

    # 主线程循环
    while True:
        try:
            time.sleep(0xFF)
        except:
            Plugin._stop()
            import platform
            if platform.system() == 'Windows':
                cmd = "taskkill /F /PID {}".format(os.getpid())
            elif platform.system() in ['Linux', 'Darwin']:
                cmd = "kill -9 {}".format(os.getpid())
            os.system(cmd)



if __name__ == '__main__':
    load_plugins()
