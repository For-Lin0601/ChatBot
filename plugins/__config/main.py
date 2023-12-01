import importlib
import os
import re
import shutil
import sys

from Models.Plugins import *
from plugins.__config.Events import *

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


@register(
    description="敏感词屏蔽",
    version="1.0.0",
    author="For_Lin0601",
    priority=-99,
)
class Config(Plugin):

    def __init__(self):
        self._save_files("config-template.py")
        self._save_files("Events.py")
        self._save_files("requirements.txt")
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
            config = importlib.import_module('config')
        else:
            self.config_template = importlib.reload(
                __import__('config-template'))
            config = importlib.reload(__import__('config'))
        for key in dir(self.config_template):
            if not key.startswith("__") and not hasattr(config, key):
                setattr(config, key, getattr(self.config_template, key))
                logging.warning(f"[{key}]不存在")
                is_integrity = False

        if not is_integrity:
            logging.warning(
                "配置文件不完整, 您可以依据 config-template.py 检查 config.py. 已设为默认值")
        self.config = config

    @on(GetConfig__)
    def get_config(self, event: EventContext,  **kwargs):
        """获取配置列表"""
        event.prevent_postorder()
        event.return_value = self.config

    @on(SetConfig__)
    def check_and_add_to_config(self, event: EventContext,  **kwargs):
        """设置配置(暂存到 __config.config 中，不写入 config.py)"""
        event.prevent_postorder()
        for item in kwargs["config"]:
            if not hasattr(self.config, item):
                setattr(self.config, item, kwargs["config"][item])

    def _save_files(self, main_file_name):
        """设置并写入 main_file_name.py 中

        系元编程
        """
        logging.info(f"设置并写入 {main_file_name}")
        imports = set()

        def update_content(main_file_name, plugin: Plugin):
            file_path = os.path.join(
                plugin.path, main_file_name)
            if not os.path.exists(file_path):
                return

            with open(file_path, "r", encoding="utf-8") as file:
                file_content = file.read()
            with open(main_file_name, "r", encoding="utf-8") as file:
                main_file_content = file.read()

            marker = f"########## {plugin.name=} {plugin.path=} ##########".replace(
                "\\", "/")
            pattern = f"{marker}(.*)(?=(########## plugin.name=(.*) plugin.path=(.*) ##########)|$)"
            match = re.search(pattern, main_file_content, re.DOTALL)
            if match:
                main_file_content = main_file_content.replace(
                    match.group(), marker + "\n" + file_content.rstrip())
            else:
                main_file_content += f"\n\n\n{marker}\n{file_content}"

            with open(main_file_name, "w", encoding="utf-8") as file:
                file.write(main_file_content)

        # 遍历插件列表
        for plugin in self.plugin_list:
            update_content(main_file_name, plugin)

        # 提升 import 语句
        with open(main_file_name, "r", encoding="utf-8") as file:
            content = file.read()
        existing_imports = re.findall(r"^\s*import .*$", content, re.MULTILINE)
        imports = set(existing_imports)
        for existing_import in imports:
            content = content.replace(existing_import+"\n", "")
        updated_content = "\n".join(imports) + "\n" + content
        with open(main_file_name, "w", encoding="utf-8") as file:
            file.write(updated_content.lstrip())

    def __del__(self):
        pass

    def __stop__(self):
        pass
