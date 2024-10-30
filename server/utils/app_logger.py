import logging, os
from logging.handlers import TimedRotatingFileHandler
import asyncio
from typing import Dict
from fastapi import WebSocket


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


class QueueHandler(logging.Handler):
    """
    日志处理器，将日志消息放入队列中
    """
    def __init__(self, queue: asyncio.Queue):
        super().__init__()
        self.queue = queue

    def emit(self, record):
        try:
            self.queue.put_nowait(self.format(record))
        except asyncio.QueueFull:
            pass


# 1. 修改 WebSocketHandler
class WebSocketHandler(logging.Handler):

    def __init__(self, websocket: WebSocket):
        super().__init__()
        self.websocket = websocket
        self.message_queue = asyncio.Queue()  # 添加消息队列
        self.setFormatter(
            logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
        )

    def emit(self, record):
        try:
            msg = self.format(record)
            # 将消息放入队列
            asyncio.create_task(self.message_queue.put(msg))
        except Exception as e:
            print(f"Error in emit: {str(e)}")

            self.handleError(record)
    # 在WebSocketHandler中添加更多调试信息
    async def _async_send(self, message: str):
        try:
            print(f"Attempting to send message via WebSocket: {message[:20]}...")
            await self.websocket.send_text(message)
            print("Message sent successfully")
        except Exception as e:
            print(f"Error sending WebSocket message: {str(e)}")


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

def setup_stream_logger(logger_name="stream"):
    # logger_name=script_name
    logger = logging.getLogger(logger_name)
    print(f"======== 指定获取脚本logger名称：{logger_name} =========")

    if not logger.hasHandlers():
        # # Get or create queue from QueueManager
        # log_queue = queue_manager.get_queue(logger_name)
        # # Set new queue handler
        # queue_handler = QueueHandler(log_queue)
        # queue_handler.setFormatter(logging.Formatter("%(asctime)s - %(message)s"))
        # logger.addHandler(queue_handler)

        # # Add console handler for direct output
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.DEBUG)
        console_formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )
        console_handler.setFormatter(console_formatter)
        logger.addHandler(console_handler)

        logger.setLevel(logging.INFO)  # 确保日志级别设置为DEBUG以捕获所有日志
        logger.info(f"Setting up stream logger: {logger_name}")
        print(f"====== 初始化日志Handler:  {logger_name} =======")

    return logger
