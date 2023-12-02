import importlib
import logging
import os
import shutil
import time


# 加载配置需要记录日志
# 加载日志需要加载配置
# 什么鬼啊这
# 所以在这里初始化一个默认Log, 先用着, 后面配置加载好了会覆盖

class LogStart:

    log_file_name = "chatbot.log"

    log_colors_config = {
        'DEBUG': 'green',  # cyan white
        'INFO': 'white',
        'WARNING': 'yellow',
        'ERROR': 'red',
        'CRITICAL': 'cyan',
    }

    logger_handler = None

    @classmethod
    def get_logging_level(cls):
        try:
            return importlib.reload(__import__('config')).logging_level
        except:
            return logging.DEBUG

    @classmethod
    def reset_logging(cls) -> None:
        import colorlog
        logging_level = cls.get_logging_level()

        # 检查logs目录是否存在
        if not os.path.exists("logs"):
            os.mkdir("logs")
        # 检查本目录是否有chatbot.log，若有，移动到logs目录
        if os.path.exists("chatbot.log"):
            shutil.move("chatbot.log", "logs/chatbot.legacy.log")
        cls.log_file_name = f"logs/chatbot-{time.strftime('%Y-%m-%d-%H-%M-%S', time.localtime())}.log" if cls.log_file_name == "chatbot.log" else cls.log_file_name

        if cls.logger_handler is not None:
            logging.getLogger().removeHandler(cls.logger_handler)

        for handler in logging.getLogger().handlers:
            logging.getLogger().removeHandler(handler)

        logging.basicConfig(level=logging_level,  # 设置日志输出格式
                            filename=cls.log_file_name,  # log日志输出的文件位置和文件名
                            format="[%(asctime)s.%(msecs)03d] %(pathname)s (%(lineno)d) - [%(levelname)s] :\n%(message)s",
                            # 日志输出的格式
                            # -8表示占位符，让输出左对齐，输出长度都为8位
                            datefmt="%Y-%m-%d %H:%M:%S",  # 时间输出的格式
                            encoding="utf-8"
                            )
        sh = logging.StreamHandler()
        sh.setLevel(logging_level)
        sh.setFormatter(colorlog.ColoredFormatter(
            fmt="%(log_color)s[%(asctime)s.%(msecs)03d] %(filename)s (%(lineno)d) - [%(levelname)s] : "
                "%(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
            log_colors=cls.log_colors_config
        ))
        logging.getLogger().addHandler(sh)
        cls.logger_handler = sh

    @classmethod
    def on_stop(cls):
        if cls.logger_handler is not None:
            logging.getLogger().removeHandler(cls.logger_handler)

        for handler in logging.getLogger().handlers:
            logging.getLogger().removeHandler(handler)
