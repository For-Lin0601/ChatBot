
import logging
import os
import re

from Models.Plugins import Plugin


def save_files(cls: 'Plugin', main_file_name):
    """设置并写入 main_file_name.py 中

    系元编程
    """
    logging.info(f"设置并写入 {main_file_name}")

    def update_content(plugin: 'Plugin'):

        file_path = \
            os.path.dirname(os.path.dirname(os.path.dirname(__file__))) + \
            os.path.join(os.path.dirname(plugin.path), main_file_name)
        if not os.path.exists(file_path):
            return

        with open(file_path, "r", encoding="utf-8") as file:
            file_content = file.read()
        with open(main_file_name, "r", encoding="utf-8") as file:
            main_file_content = file.read()

        marker = f"########## {plugin.name=} {plugin.path=} ##########".replace(
            "\\", "/")
        pattern = f"{marker}(.*?)(?=(########## plugin.name=(.*) plugin.path=(.*) ##########)|$)"
        match = re.search(pattern, main_file_content, re.DOTALL)
        if match:
            main_file_content = main_file_content.replace(
                match.group(), marker + "\n" + file_content.rstrip() + "\n\n\n")
        else:
            main_file_content += f"\n\n\n{marker}\n{file_content}"

        with open(main_file_name, "w", encoding="utf-8") as file:
            file.write(main_file_content)

    # 遍历插件列表
    for plugin in cls.plugin_list:
        update_content(plugin)

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
