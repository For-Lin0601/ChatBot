
from datetime import datetime, timedelta


class Session:
    """运行时记忆链(暂时没做外部存储)"""

    def __init__(self, session_name: str, role_name: str, content: str, out_time: datetime):
        self.session_name = session_name
        """与用户绑定的会话名字"""

        self.role_name = role_name
        """场景预设名"""

        self.sessions = [
            {"role": "user", "content": content},
            {"role": "assistant", "content": "ok, I'll follow your commands."}
        ]
        """对话内容"""

        self.time_out = datetime.now() + timedelta(seconds=out_time)
        """过期时间"""

        self.params = None
        """和gpt接口交互时的参数, 默认为`config.completion_api_params`中的值"""

        self.is_plus = False
        """是否是plus api"""

        self.prefix = ""
        """gpt回复前缀(使用4.0模型建议打开)"""

    def add_user(self, content: str):
        self.sessions.append({"role": "user", "content": content})

    def add_assistant(self, content: str):
        self.sessions.append({"role": "assistant", "content": content})

    @property
    def last_user_content(self):
        if not self.sessions:
            return ""
        if self.sessions[-1]["role"] == "user":
            return self.sessions[-1]["content"]
        return self.sessions[-2]["content"] if len(self.sessions) > 1 else ""

    @property
    def last_assistant_content(self):
        if not self.sessions:
            return ""
        if self.sessions[-1]["role"] == "assistant":
            return self.sessions[-1]["content"]
        return self.sessions[-2]["content"] if len(self.sessions) > 1 else ""

    def set_plus(self):
        """切换到4.0模型"""
        self.is_plus = True
        self.prefix = "[gpt4] "
        self.params = {
            "model": "gpt-4-0314",
            "temperature": 0.8,
            "top_p": 1,
            "frequency_penalty": 0.3,
            "presence_penalty": 1.0,
        }
