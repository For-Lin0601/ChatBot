import os
import shutil
import sys

from .Events import *
from Models.Plugins import *
from .save_files import save_files

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


@register(
    description="敏感词屏蔽",
    version="1.0.0",
    author="For_Lin0601",
    priority=-99
)
class Config(Plugin):

    def __init__(self):
        save_files(self, "config-template.py")
        save_files(self, "Events.py")
        save_files(self, "requirements.txt")
        logging.info("检查 config 模块完整性.")

        # 配置文件存在性校验
        if not os.path.exists('config.py'):
            shutil.copy('config-template.py', 'config.py')
            logging.error('请先在config.py中填写配置')
            sys.exit(0)

        is_integrity = True
        if self.is_first_init():
            # 完整性校验
            self.config_template = importlib.import_module('config-template')
            self.config = importlib.import_module('config')
        else:
            self.config_template = importlib.reload(
                __import__('config-template'))
            self.config = importlib.reload(__import__('config'))
        for key in dir(self.config_template):
            if not key.startswith("__") and not hasattr(self.config, key):
                setattr(self.config, key, getattr(self.config_template, key))
                logging.warning(f"[{key}]不存在")
                is_integrity = False
        importlib.reload(__import__('Events'))

        if not is_integrity:
            logging.warning(
                "配置文件不完整, 您可以依据 config-template.py 检查 config.py. 已设为默认值")

    @on(PluginsLoadingFinished)
    @on(PluginsReloadFinished)
    def reset_config(self, event: EventContext, **kwargs):
        """重置配置"""
        importlib.reload(__import__('config-template'))
        importlib.reload(__import__('config'))
        importlib.reload(__import__('Events'))

    @on(GetConfig__)
    def get_config(self, event: EventContext,  **kwargs):
        """获取配置列表"""
        event.prevent_postorder()
        event.return_value = self.config

    @on(SetConfig__)
    def check_and_add_to_config(self, event: EventContext,  **kwargs):
        """设置配置

        暂存到 __config.config 中, 不写入 config.py

        热重载可能丢失, 请谨慎使用
        """
        event.prevent_postorder()
        for item in kwargs["config"]:
            if not hasattr(self.config, item):
                setattr(self.config, item, kwargs["config"][item])

    def on_reload(self):
        pass

    def on_stop(self):
        pass
