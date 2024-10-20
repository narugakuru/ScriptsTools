# server/controller/my_logger.py
import logging
from logging.handlers import TimedRotatingFileHandler
import asyncio
from fastapi import Depends

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
        log_entry = self.format(record)
        try:
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

def setup_stream_logger(log_queue: asyncio.Queue, logger_name="stream"):
    logger = logging.getLogger(logger_name)
  
    # Remove all previous handlers
    for handler in logger.handlers[:]:
        if isinstance(handler, QueueHandler):
            logger.removeHandler(handler)
  
    # Set new queue handler
    queue_handler = QueueHandler(log_queue)
    queue_handler.setFormatter(logging.Formatter("%(asctime)s - %(message)s"))
    logger.addHandler(queue_handler)

    return logger
