# 插件管理模块
import logging
import importlib
import os
import pkgutil
import sys
import time
import traceback

from Models.Plugins import Plugin


def walk_plugin_path(module, prefix='', path_prefix=''):
    error_list = []

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

                    importlib.import_module(module.__name__ + '.' + item.name)
                    logging.info(
                        '加载模块: plugins/{} 成功'.format(path_prefix + item.name + '.py'))
                except:
                    error_list.append(module.__name__ + '.' + item.name)
                    logging.warning(
                        '加载模块: plugins/{} 失败: {}'.format(path_prefix + item.name + '.py', sys.exc_info()))
                    traceback.print_exc()

    _walk_plugin_path(module, prefix, path_prefix)
    if error_list:
        from plugins.__config.save_files import save_files
        save_files(Plugin, "Events.py")
        importlib.reload(__import__("Events"))
        logging.warning("开始尝试重新加载模块")
        for _ in range(3):
            logging.warning(f"第{_+1}次尝试重新加载模块")
            for i, error in enumerate(error_list):
                try:
                    importlib.reload(__import__(error, fromlist=['']))
                    logging.info('重新加载模块: {} 成功'.format(error))
                    error_list.pop(i)
                except:
                    logging.error('重新加载模块: {} 失败: {}'.format(
                        error, sys.exc_info()))
                    traceback.print_exc()
            if not error_list:
                break


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
