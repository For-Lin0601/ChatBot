
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

        self._out_time = out_time
        """缓存过期时间, 通过装饰器更新"""

        self.prefix = ""
        """gpt回复前缀(使用4.0模型建议打开)"""

        self.params_name = None
        """和gpt接口交互时的参数, 默认为`config.completion_api_params`中的值"""

        self._is_plus = False
        """是否是plus api"""

        self._once = False
        """api 只调用一次"""

        self._prefix = ""
        """只调用一次时临时存储"""

        self._params_name = None
        """只调用一次时临时存储"""

        self._plus_once = False
        """plus api 只调用一次"""

        self.user_length = 0
        """api 总发送的对话长度

        注意每次对话会把历史记录也发过去, 所以此处增长很快
        """

        self.assistant_length = 0
        """api 总接收的对话长度

        此处只记录返回值
        """

        self.count_rounds = 0
        """api 总对话轮数"""

        self.plus_user_length = 0
        """plus api 总发送的对话长度

        注意每次对话会把历史记录也发过去, 所以此处增长很快
        """

        self.plus_assistant_length = 0
        """plus api 总接收的对话长度

        此处只记录返回值
        """

        self.plus_count_rounds = 0
        """plus api 总对话轮数"""

    @property
    def is_plus(self):
        """是否是plus api"""
        return (self._is_plus or self._plus_once) and not self._once

    @is_plus.setter
    def is_plus(self, value):
        self._is_plus = value

    def update_out_time(func):
        """过期时间更新装饰器"""

        def wrapper(self: 'Session', *args, **kwargs):
            self.time_out = datetime.now() + timedelta(seconds=self._out_time)
            return func(self, *args, **kwargs)
        return wrapper

    def get_content_length(self):
        """获取历史对话长度"""
        return sum(len(session["content"]) for session in self.sessions)

    @update_out_time
    def add_user(self, content: str):
        """用户输入"""
        self.sessions.append({"role": "user", "content": content})

    def add_assistant(self, content: str):
        """机器人回复"""
        if self.is_plus:
            self.plus_user_length += self.get_content_length()
            self.plus_assistant_length += len(content)
            self.plus_count_rounds += 1
        else:
            self.user_length += self.get_content_length()
            self.assistant_length += len(content)
            self.count_rounds += 1
        self.sessions.append({"role": "assistant", "content": content})
        # 检查`self._plus_once`
        if self._once or self._plus_once:
            self._once = self._plus_once = False
            self.prefix = self._prefix
            self.params_name = self._params_name

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

        若不存在则继续使用api对应默认配置, 默认应该有个`name=gpt4`是合法值
        """
        logging.info(f"[{self.session_name}] 切换到4.0: {name}")
        self.is_plus = True
        self.prefix = f"[{name}] "
        self.params_name = name

    @update_out_time
    def set_params_for_once(self, name):
        """切换到3.5模型(在一轮对话后销毁)

        name为`config.completion_api_params`中的key

        若不存在则继续使用api对应默认配置, 默认应该有个`name=default`是合法值
        """
        if self._once or self._plus_once:
            self._plus_once = False
        else:
            self._prefix = self.prefix
            self._params_name = self.params_name
        self._once = True
        self.prefix = f"[{name}](剩余0次) "
        self.params_name = name

    @update_out_time
    def set_plus_params_for_once(self, name):
        """切换到4.0模型(在一轮对话后销毁)

        name为`config.completion_api_params`中的key

        若不存在则继续使用api对应默认配置, 默认应该有个`name=gpt4`是合法值
        """
        logging.info(f"[{self.session_name}] 临时切换到4.0: {name}")
        if self._once or self._plus_once:
            self._once = False
        else:
            self._prefix = self.prefix
            self._params_name = self.params_name
        self._plus_once = True
        self.prefix = f"[{name}](剩余0次) "
        self.params_name = name

    def try_get_nickname(self) -> str:
        """尝试获取昵称, 格式`[xx] `, 失败返回空字符串"""
        try:
            if self.session_name.startswith("person_"):
                from Models.Plugins import Plugin
                from Events import GetCQHTTP__
                cqhttp = Plugin.emit(GetCQHTTP__)
                return "[" + cqhttp.getStrangerInfo(
                    int(self.session_name.replace("person_", ""))
                ).nickname + "] "
            elif self.session_name.startswith("group_"):
                from Models.Plugins import Plugin
                from Events import GetCQHTTP__
                cqhttp = Plugin.emit(GetCQHTTP__)
                return "[" + cqhttp.getGroupInfo(
                    int(self.session_name.replace("group_", ""))
                ).group_name + "] "
            elif self.session_name.startswith("wx_") and \
                    not self.session_name.endswith("@chatroom"):
                from Models.Plugins import Plugin
                from Events import GetWCF__
                wcf = Plugin.emit(GetWCF__)
                return "[" + wcf.get_info_by_wxid(
                    self.session_name.replace("wx_", "")
                )["name"] + "] "
        except:
            pass
        return ""

    def statistical_usage(self) -> str:
        """统计api调用次数"""
        reply = f"{self.try_get_nickname()}{self.session_name}:\n"
        reply += f"  场景预设: {self.role_name}\n"
        if self._is_plus:
            reply += f"  启用GPT4: 是\n"
        else:
            reply += f"  启用GPT4: 否\n"
        if self.params_name:
            reply += f"  当前模型: {self.params_name}\n"
        else:
            reply += f"  当前模型: default\n"
        if self.count_rounds > 0:
            reply += f"  [GPT3.5用量]:\n"
            reply += f"  - 对话次数: {self.count_rounds}次\n"
            reply += f"  - 发送字数: {self.user_length}字\n"
            reply += f"  - 回复字数: {self.assistant_length}字\n"
        else:
            reply += "  [GPT3.5用量]: 无\n"
        if self.plus_count_rounds > 0:
            reply += f"  [GPT4用量]:\n"
            reply += f"  - 对话次数: {self.plus_count_rounds}次\n"
            reply += f"  - 发送字数: {self.plus_user_length}字\n"
            reply += f"  - 回复字数: {self.plus_assistant_length}字"
        else:
            reply += "  [GPT4用量]: 无"
        return reply

    def __del__(self):
        """只是简单的通知, 如果不喜欢直接删了这个函数就行"""
        reply = self.statistical_usage()
        logging.info(f"检测到对话销毁:\n{reply}")
        if self.plus_user_length > 0 or self.user_length > 10000:
            try:
                from Models.Plugins import Plugin
                from Events import GetCQHTTP__
                cqhttp = Plugin.emit(GetCQHTTP__)
                cqhttp.NotifyAdmin(f"[bot] 检测到对话销毁:\n" + reply)
            except Exception as e:
                logging.error(f"对话销毁通知管理员失败:\n{e}")
