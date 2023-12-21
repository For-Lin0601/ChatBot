
from datetime import datetime, timedelta
import logging


class Session:
    """运行时记忆链(暂时没做外部存储)"""

    def __init__(self, session_name: str, role_name: str, content: str, out_time: datetime):
        logging.info(f"创建会话[{session_name}]: {role_name=}, {out_time=}")
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

        self.params_name = None
        """和gpt接口交互时的参数, 默认为`config.completion_api_params`中的值"""

        self.is_plus = False
        """是否是plus api"""

        self.prefix = ""
        """gpt回复前缀(使用4.0模型建议打开)"""

        self._out_time = out_time
        """缓存过期时间, 通过装饰器更新"""

        self._plus_once = False
        """plus api 只调用一次"""

    def update_out_time(func):
        """过期时间更新装饰器"""

        def wrapper(self: 'Session', *args, **kwargs):
            self.time_out = datetime.now() + timedelta(seconds=self._out_time)
            return func(self, *args, **kwargs)
        return wrapper

    @update_out_time
    def add_user(self, content: str):
        self.sessions.append({"role": "user", "content": content})

    def add_assistant(self, content: str):
        self.sessions.append({"role": "assistant", "content": content})
        # 检查`self._plus_once`
        if self._plus_once:
            self._plus_once = False
            self.set_params()

    @property
    def last_user_content(self):
        """最后一次用户输入的内容"""
        if not self.sessions:
            return ""
        if self.sessions[-1]["role"] == "user":
            return self.sessions[-1]["content"]
        return self.sessions[-2]["content"] if len(self.sessions) > 1 else ""

    @property
    def last_assistant_content(self):
        """最后一次机器人回复的内容"""
        if not self.sessions:
            return ""
        if self.sessions[-1]["role"] == "assistant":
            return self.sessions[-1]["content"]
        return self.sessions[-2]["content"] if len(self.sessions) > 1 else ""

    @update_out_time
    def set_params(self, name=None):
        """设置gpt接口交互时的参数

        name为`config.completion_api_params`中的key

        若不存在则继续使用api对应默认配置
        """
        self.is_plus = False
        self.prefix = f"[{name}] " if name else ""
        self.params_name = name

    @update_out_time
    def set_plus_params(self, name):
        """切换到4.0模型

        name为`config.completion_api_params`中的key

        若不存在则继续使用api对应默认配置, 默认应该有个`gpt4`是合法值
        """
        logging.info(f"[{self.session_name}] 切换到4.0: {name}")
        self.is_plus = True
        self.prefix = f"[{name}] "
        self.params_name = name

    @update_out_time
    def set_plus_params_for_once(self, name):
        """切换到4.0模型(在一轮对话后销毁)

        name为`config.completion_api_params`中的key

        若不存在则继续使用api对应默认配置, 默认应该有个`gpt4`是合法值
        """
        logging.info(f"[{self.session_name}] 临时切换到4.0: {name}")
        self._plus_once = True
        self.is_plus = True
        self.prefix = f"[{name}](剩余0次) "
        self.params_name = name
