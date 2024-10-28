# server/controller/my_logger.py
import logging, os
from logging.handlers import TimedRotatingFileHandler
import asyncio
from typing import Dict


class QueueManager:
    def __init__(self):
        self.queues: Dict[str, asyncio.Queue] = {}

    def get_queue(self, name: str) -> asyncio.Queue:
        if name not in self.queues:
            self.queues[name] = asyncio.Queue()
        return self.queues[name]

    def remove_queue(self, name: str):
        if name in self.queues:
            del self.queues[name]


queue_manager = QueueManager()


# 不再是全局队列，而是动态创建
def get_new_log_queue():
    return asyncio.Queue()


class QueueHandler(logging.Handler):
    """
    日志处理器，将日志消息放入队列中
    """

    def __init__(self, queue):
        super().__init__()
        self.queue = queue

    def emit(self, record):
        try:
            log_entry = self.format(record)  # 确保日志记录被正确格式化
            self.queue.put_nowait(log_entry)
        except asyncio.QueueFull:
            pass


def setup_logger(logger_name="app"):
    logger = logging.getLogger(logger_name)
    if not logger.hasHandlers():
        logger.setLevel(logging.INFO)
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.DEBUG)
        console_formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )
        console_handler.setFormatter(console_formatter)
        logger.addHandler(console_handler)

        # Global file handler for persistent logs
        file_handler = TimedRotatingFileHandler(
            "my_log_file.log", when="midnight", interval=1, backupCount=7
        )
        file_handler.setLevel(logging.DEBUG)
        file_formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )
        file_handler.setFormatter(file_formatter)
        logger.addHandler(file_handler)
    return logger

# logger_name="stream"
def setup_stream_logger(logger_name):
    if logger_name is None:
        logger_name = os.path.basename(__file__).split(".")[0]
        print(f'自动获取脚本logger名称：======== {logger_name} =========')

    logger = logging.getLogger(logger_name)

    if not logger.hasHandlers():
        # Get or create queue from QueueManager
        log_queue = queue_manager.get_queue(logger_name)
        # Set new queue handler
        queue_handler = QueueHandler(log_queue)
        queue_handler.setFormatter(logging.Formatter("%(asctime)s - %(message)s"))
        logger.addHandler(queue_handler)

        # Add console handler for direct output
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.DEBUG)
        console_formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )
        console_handler.setFormatter(console_formatter)
        logger.addHandler(console_handler)

        logger.setLevel(logging.INFO)  # 确保日志级别设置为DEBUG以捕获所有日志
        logger.info("Setting up stream logger")

    return logger


def inject_logger(func):
    def wrapper(*args, **kwargs):
        script_name = os.path.basename(__file__).split('.')[0]
        logger = setup_stream_logger(script_name)
        kwargs['logger'] = logger
        return func(*args, **kwargs)
    return wrapper