import os
import time
import logging
import shutil

from Models.Plugins import *


class config:
    logging_level = logging.DEBUG


@register(
    description="log日志",
    version="1.0.0",
    author="For_Lin0601",
    priority=-1,
    is_instance=False,
)
class LogPlugin(Plugin):

    log_file_name = "chatbot.log"

    log_colors_config = {
        'DEBUG': 'green',  # cyan white
        'INFO': 'white',
        'WARNING': 'yellow',
        'ERROR': 'red',
        'CRITICAL': 'cyan',
    }

    logger_handler = None

    # 插件加载时触发
    # plugin_list 提供了全部插件列表，详细请查看其源码
    def __init__(self, plugin_list):
        """为此次运行生成日志文件
        格式: chatbot-yyyy-MM-dd-HH-mm-ss.log
        """

        # 检查logs目录是否存在
        if not os.path.exists("logs"):
            os.mkdir("logs")

        # 检查本目录是否有chatbot.log，若有，移动到logs目录
        if os.path.exists("chatbot.log"):
            shutil.move("chatbot.log", "logs/chatbot.legacy.log")

        self.log_file_name = f"logs/chatbot-{time.strftime('%Y-%m-%d-%H-%M-%S', time.localtime())}.log"
        self.reset_logging()

    def reset_logging(self):

        import colorlog

        if self.logger_handler is not None:
            logging.getLogger().removeHandler(self.logger_handler)

        for handler in logging.getLogger().handlers:
            logging.getLogger().removeHandler(handler)

        logging.basicConfig(level=config.logging_level,  # 设置日志输出格式
                            filename=self.log_file_name,  # log日志输出的文件位置和文件名
                            format="[%(asctime)s.%(msecs)03d] %(pathname)s (%(lineno)d) - [%(levelname)s] :\n%(message)s",
                            # 日志输出的格式
                            # -8表示占位符，让输出左对齐，输出长度都为8位
                            datefmt="%Y-%m-%d %H:%M:%S"  # 时间输出的格式
                            )
        sh = logging.StreamHandler()
        sh.setLevel(config.logging_level)
        sh.setFormatter(colorlog.ColoredFormatter(
            fmt="%(log_color)s[%(asctime)s.%(msecs)03d] %(filename)s (%(lineno)d) - [%(levelname)s] : "
                "%(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
            log_colors=self.log_colors_config
        ))
        logging.getLogger().addHandler(sh)
        self.logger_handler = sh
        return sh

    # 插件卸载时触发
    def __del__(self):
        pass
