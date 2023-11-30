import importlib
import logging
import pkgutil
from Events import PluginsReloadFinished

from Models.Plugins import Plugin


def walk(module, prefix='', path_prefix=''):
    """遍历并重载所有模块"""
    for item in pkgutil.iter_modules(module.__path__):
        logging.debug("fuck")
        if item.ispkg:

            walk(__import__(module.__name__ + '.' + item.name,
                 fromlist=['']), prefix + item.name + '.', path_prefix + item.name + '/')
        else:
            logging.info('reload module: {}, path: {}'.format(
                prefix + item.name, path_prefix + item.name + '.py'))
            importlib.reload(__import__(module.__name__ +
                             '.' + item.name, fromlist=['']))


def reload():
    """热重载"""
    Plugin._reload()
    logging.info("重载插件")
    walk(__import__('plugins'))
    Plugin._initialize_plugins()
    Plugin.__reload_config__ = {}
    Plugin.emit(PluginsReloadFinished)
