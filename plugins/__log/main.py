import importlib
import os
import time
import logging
import shutil

from Models.Plugins import *
from plugins.__log.Events import *


@register(
    description="log日志",
    version="1.0.0",
    author="For_Lin0601",
    priority=-100,
)
class Log(Plugin):

    log_file_name = "chatbot.log"

    log_colors_config = {
        'DEBUG': 'green',  # cyan white
        'INFO': 'white',
        'WARNING': 'yellow',
        'ERROR': 'red',
        'CRITICAL': 'cyan',
    }

    logger_handler = None

    logging_level = None

    # 插件加载时触发
    # plugin_list 提供了全部插件列表，详细请查看其源码
    def __init__(self):
        """为此次运行生成日志文件
        格式: chatbot-yyyy-MM-dd-HH-mm-ss.log
        """
        if self.__first_init__:
            try:
                import log_start
                self.log_file_name = log_start.LogStart.log_file_name
                log_start.LogStart.__del__()
            except:
                # 检查logs目录是否存在
                if not os.path.exists("logs"):
                    os.mkdir("logs")
                # 检查本目录是否有chatbot.log，若有，移动到logs目录
                if os.path.exists("chatbot.log"):
                    shutil.move("chatbot.log", "logs/chatbot.legacy.log")
                self.log_file_name = f"logs/chatbot-{time.strftime('%Y-%m-%d-%H-%M-%S', time.localtime())}.log"
        else:
            self.log_file_name = self.get_reload_config("log_file_name")

        try:
            self.logger_handler = self.get_reload_config("logger_handler")
            if self.logger_handler is not None:
                logging.getLogger().removeHandler(self.logger_handler)

            for handler in logging.getLogger().handlers:
                logging.getLogger().removeHandler(handler)
        except:
            pass
        self.reset_logging(None)

    def get_logging_level(self):
        try:
            self.logging_level = importlib.reload(
                __import__('config')).logging_level
        except:
            self.logging_level = logging.DEBUG  # TODO
            raise Exception("请先配置logging_level")

    @on(SetLogs__)
    def reset_logging(self, event: EventContext,  **kwargs):
        import colorlog
        self.get_logging_level()

        if self.logger_handler is not None:
            logging.getLogger().removeHandler(self.logger_handler)

        for handler in logging.getLogger().handlers:
            logging.getLogger().removeHandler(handler)

        logging.basicConfig(level=self.logging_level,  # 设置日志输出格式
                            filename=self.log_file_name,  # log日志输出的文件位置和文件名
                            format="[%(asctime)s.%(msecs)03d] %(pathname)s (%(lineno)d) - [%(levelname)s] :\n%(message)s",
                            # 日志输出的格式
                            # -8表示占位符，让输出左对齐，输出长度都为8位
                            datefmt="%Y-%m-%d %H:%M:%S",  # 时间输出的格式
                            encoding="utf-8"
                            )
        sh = logging.StreamHandler()
        sh.setLevel(self.logging_level)
        sh.setFormatter(colorlog.ColoredFormatter(
            fmt="%(log_color)s[%(asctime)s.%(msecs)03d] %(filename)s (%(lineno)d) - [%(levelname)s] : "
                "%(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
            log_colors=self.log_colors_config
        ))
        logging.getLogger().addHandler(sh)
        self.logger_handler = sh

    # 插件卸载时触发
    def __del__(self):
        self.set_reload_config("logger_handler", self.logger_handler)
        self.set_reload_config("log_file_name", self.log_file_name)
