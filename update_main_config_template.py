import os
import re

from Models.ConfigListModel import ConfigList


def update_main_config_template(config_list: ConfigList):
    main_config_template_path = "config-template.py"  # 主线程的config-template.py路径
    main_config_path = "config.py"  # 主线程的config.py路径

    def update_class_content(main_config_template_path, folder, folder_path):
        # 遍历文件夹内所有文件
        for filename in os.listdir(folder_path):
            file_path = os.path.join(folder_path, filename)

            # 只处理目标的文件夹
            if os.path.isdir(file_path):
                class_name = f"{folder}_{filename}"
                class_content = read_config_template(
                    os.path.join(file_path, "config-template.py"))

                # 更新主线程的config-template.py
                update_main_config_template(main_config_template_path,
                                            class_name, class_content)

    def read_config_template(config_template_path):
        # 读取插件的config-template.py内容
        with open(config_template_path, "r", encoding="utf-8") as file:
            return file.read()

    def update_main_config_template(main_config_template_path, class_name, class_content: str):
        # 读取主线程的config-template.py内容
        with open(main_config_template_path, "r", encoding="utf-8") as file:
            main_config_template_content = file.read()

        # 构造匹配类的正则表达式
        class_pattern = f"class {class_name}\(Config\)(.*?)(class (.*):|$)"
        match = re.search(
            class_pattern, main_config_template_content, re.DOTALL)

        # 在每一行前加上四个空格
        class_content = "\n    ".join(class_content.splitlines())

        # 在最前面加入一行class {plugins/bot/utils}_{dirname}:作为唯一性标识
        class_content = f"class {class_name}(Config):\n    {class_content if class_content else 'pass'}"

        if match:
            # 如果已存在该类，则替换原有内容
            main_config_template_content = main_config_template_content.replace(
                match.group(), class_content)
        else:
            # 如果不存在该类，则添加到文件末尾
            main_config_template_content += f"\n\n{class_content}"

        # 将更新后的内容写回主线程的config-template.py
        with open(main_config_template_path, "w", encoding="utf-8") as file:
            file.write(main_config_template_content)

    # 遍历bot、plugins、utils文件夹
    folders = ["bot", "plugins", "utils"]
    for folder in folders:
        folder_path = os.path.join(os.getcwd(), folder)
        update_class_content(main_config_template_path, folder, folder_path)


if __name__ == "__main__":
    config_list = ConfigList()
    update_main_config_template(config_list)
