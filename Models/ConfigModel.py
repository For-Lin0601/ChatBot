from ctypes import Union
import re


class Config:
    def __init__(self,
                 model_name: Union["bot", "utils", "plugins"],
                 class_name: str,
                 text: str):

        self.model_name = model_name
        """模型名/路径名"""

        self.class_name = class_name
        """配置文件名"""

        self.text = text
        """配置文件原文本"""

        self.class_text = self._update_to_main_config_template()
        """配置文件实例化后的文本"""

        self.configs = None
        """配置文件参数"""

    def _update_to_main_config_template(self):
        """
        - 生成配置文件实例化后的文本

        例：/bot/qqbot/config-template.py

        ---
        ```py
        # qq账号
        qq_account = 12345678

        # qq密码
        qq_password = "abcdefg"

        # qq好友列表
        friend_list = [12345678, 23456789]
        ```
        ---

        - 写入 /config-template.py

        ---
        ```py
        class bot_qqbot(Config):
            # qq账号
            qq_account = 12345678

            # qq密码
            qq_password = "abcdefg"

            # qq好友列表
            friend_list = [12345678, 23456789]
        ```
        """
        content_list = self.text.splitlines()
        for i in range(len(content_list)):
            content_list[i] = f"    {content_list[i]}" if content_list[i] else ""
        content = "\n".join(content_list)
        class_content = f"class {self.model_name}_{self.class_name}(Config):\n{content if content else 'pass'}"

        # 读取主线程的config-template.py内容
        main_config_template_path = "config-template.py"
        with open(main_config_template_path, "r", encoding="utf-8") as file:
            main_config_template_content = file.read()

        # 构造匹配类的正则表达式
        class_pattern = f"class {self.model_name}_{self.class_name}\(Config\):(.*?)(class (.*):|$)"
        match = re.search(
            class_pattern, main_config_template_content, re.DOTALL)

        if match:
            main_config_template_content = main_config_template_content.replace(
                match.group(), class_content)
        else:
            main_config_template_content += f"\n\n{class_content}"

        # 将更新后的内容写回主线程的config-template.py
        with open(main_config_template_path, "w", encoding="utf-8") as file:
            file.write(main_config_template_content)
