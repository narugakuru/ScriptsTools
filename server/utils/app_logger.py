import logging, os
from logging.handlers import TimedRotatingFileHandler
import asyncio
from typing import Dict
from fastapi import WebSocket


class QueueManager:
    def __init__(self):
        """
        初始化QueueManager类，用于管理多个异步队列
        """
        self.queues: Dict[str, asyncio.Queue] = {}

    def get_queue(self, name: str) -> asyncio.Queue:
        """
        获取指定名称的异步队列，如果该队列不存在，则创建一个新队列并返回。

        参数:
        name (str): 队列的名称

        返回:
        asyncio.Queue: 指定名称的异步队列
        """
        if name not in self.queues:
            self.queues[name] = asyncio.Queue()
        return self.queues[name]

    def remove_queue(self, name: str):
        """
        移除指定名称的异步队列。

        参数:
        name (str): 要移除的队列名称
        """
        if name in self.queues:
            del self.queues[name]


queue_manager = QueueManager()


class QueueHandler(logging.Handler):
    """
    日志处理器，将日志消息放入队列中
    """

    def __init__(self, queue: asyncio.Queue):
        """
        初始化QueueHandler实例。

        参数:
        queue (asyncio.Queue): 用于存放日志消息的异步队列
        """
        super().__init__()
        self.queue = queue

    def emit(self, record):
        """
        将日志记录放入指定的队列中，如果队列已满则捕获异常。

        参数:
        record: 日志记录对象
        """
        try:
            self.queue.put_nowait(self.format(record))
        except asyncio.QueueFull:
            pass


# 1. 修改 WebSocketHandler
class WebSocketHandler(logging.Handler):
    """
    WebSocket日志处理器，使日志消息通过WebSocket发送
    """

    def __init__(self, websocket: WebSocket):
        """
        初始化WebSocketHandler实例。

        参数:
        websocket (WebSocket): WebSocket连接对象
        """
        super().__init__()
        self.websocket = websocket
        self.message_queue = asyncio.Queue()  # 添加消息队列
        self.setFormatter(
            logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
        )

    def emit(self, record):
        """
        将日志记录格式化并放入消息队列中，如果发生异常则处理错误。

        参数:
        record: 日志记录对象
        """
        try:
            msg = self.format(record)
            # 将消息放入队列
            asyncio.create_task(self.message_queue.put(msg))
        except Exception as e:
            print(f"Error in emit: {str(e)}")
            self.handleError(record)

    async def _async_send(self, message: str):
        """
        通过WebSocket异步发送消息，并处理可能的异常。

        参数:
        message (str): 要发送的消息字符串
        """
        try:
            # print(f"Attempting to send message via WebSocket: {message[:20]}...")
            await self.websocket.send_text(message)
            print("Message sent successfully")
        except Exception as e:
            print(f"Error sending WebSocket message: {str(e)}")


def setup_logger(logger_name="app"):
    """
    设置全局日志记录器，包括控制台和文件处理器。

    参数:
    logger_name (str): 日志记录器的名称，默认为"app"

    返回:
    logging.Logger: 配置好的日志记录器
    """
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


def setup_stream_logger(logger_name="stream"):
    """
    设置流日志记录器，指定用于控制台输出的日志记录器。

    参数:
    logger_name (str): 日志记录器的名称，默认为"stream"

    返回:
    logging.Logger: 配置好的流日志记录器
    """
    logger = logging.getLogger(logger_name)
    print(f"======== 指定获取脚本logger名称：{logger_name} =========")

    if not logger.hasHandlers():
        # # Add console handler for direct output
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        console_formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )
        console_handler.setFormatter(console_formatter)
        logger.addHandler(console_handler)

        logger.setLevel(logging.INFO)  # 确保日志级别设置为DEBUG以捕获所有日志
        logger.info(f"Setting up stream logger: {logger_name}")
        print(f"====== 初始化日志Handler:  {logger_name} =======")

    return logger


def logger_init_print(file_name, print_info=True):
    """
    初始化并且打印日志信息
    """
    # 获取当前文件的名词
    current_file_name = file_name.split(".")[-1]
    logger = logging.getLogger(current_file_name)

    if print_info:
        logger_info = {
            "name": logger.name,
            "level": logger.level,
            "handlers": [handler.__class__.__name__ for handler in logger.handlers],
            "propagate": logger.propagate,
        }
        print(f"{current_file_name}文件的Logger 信息: {logger_info}")

    return logger
