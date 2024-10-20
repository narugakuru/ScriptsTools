# logger_setup.py
import logging


# 自定义日志处理器
class ListHandler(logging.Handler):
    def __init__(self):
        super().__init__()
        self.log_messages = []

    def emit(self, record):
        msg = self.format(record)
        self.log_messages.append(msg)

    def clear_logs(self):
        self.log_messages.clear()

    def get_logs(self):
        return self.log_messages


# 设置全局 logger
logger = logging.getLogger("GlobalLogger")
logger.setLevel(logging.DEBUG)

# Pyside界面
list_handler = ListHandler()
formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
list_handler.setFormatter(formatter)
logger.addHandler(list_handler)

# 控制台
console_handler = logging.StreamHandler()
console_handler.setFormatter(formatter)
logger.addHandler(console_handler)


# 提供获取日志的函数
def get_logs():

    return "\n".join(list_handler.get_logs())


def clear_logs():
    list_handler.clear_logs()


def get_clear_logs():
    msg = get_logs()
    print(msg)
    clear_logs()
    return msg
