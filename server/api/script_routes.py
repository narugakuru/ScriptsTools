import time
from fastapi import APIRouter, WebSocket
from . import *
from server.api.result import *
from server.utils.printer_wrapper import format_and_print_params
from server.config import *
from server.utils.app_logger import *
from typing import Dict, Set
from datetime import datetime, timedelta


router = APIRouter()


@router.websocket("/ws/{script_name}")
async def websocket_endpoint(websocket: WebSocket, script_name: str):
    """
    处理 WebSocket 连接并发送消息。

    参数:
    - websocket: WebSocket 连接对象。
    - script_name: 连接的脚本名称。
    """
    await websocket.accept()  # 接受 WebSocket 连接
    print(f"WebSocket connection established for {script_name}")

    logger = setup_stream_logger(script_name)  # 设置日志记录器
    ws_handler = WebSocketHandler(websocket)  # 创建 WebSocket 处理器
    logger.addHandler(ws_handler)  # 将处理器添加到日志记录器中

    timeout = timedelta(seconds=8)  # 设置超时时间
    last_message_time = datetime.now()  # 记录最后消息时间

    try:
        while True:
            try:
                # 非阻塞方式获取消息
                try:
                    # 尝试从队列获取消息，设置超时时间
                    msg = await asyncio.wait_for(
                        ws_handler.message_queue.get(), timeout=5
                    )
                    logging.debug("=======websocket开始发送消息 =====")
                    await websocket.send_text(msg)  # 发送文本消息
                    last_message_time = datetime.now()  # 更新最后消息时间

                except asyncio.TimeoutError:
                    # 检查是否超过指定时间没有新消息
                    if datetime.now() - last_message_time > timeout:
                        logger.info(
                            "No messages received for 5 seconds, closing connection"
                        )
                        await websocket.close()  # 关闭连接
                        break
                    continue
                except Exception as e:
                    logger.info(f"Error sending message: {e}")
                    break  # 发生错误时直接退出

            except asyncio.CancelledError:
                break  # 在任务被取消时退出循环

            await asyncio.sleep(0.01)  # 小睡眠，避免高频率循环

    except Exception as e:
        logger.info(f"WebSocket error: {e}")
    finally:
        logger.removeHandler(ws_handler)  # 从日志记录器中移除处理器
        try:
            await websocket.close()  # 尝试关闭 WebSocket 连接

        except:
            pass  # 忽略关闭过程中可能出现的异常
        logger.info(
            f"WebSocket handler removed from logger {script_name}"
        )  # 打印处理器移除信息


# @format_and_print_params
@router.post("/{script_name}")
async def run_script(script_name: str, params: dict):
    """
    执行指定的脚本并记录日志。

    参数:
    - script_name: 要执行的脚本名称。
    - params: 执行脚本所需的参数字典。
    """
    try:
        logger = setup_stream_logger(script_name)  # 设置日志记录器

        # 添加文件日志处理器
        log_file = f"E:\WorkSpace\WebKaisyu\{script_name}.log"
        file_handler = logging.FileHandler(log_file)  # 创建文件处理器
        file_formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )
        file_handler.setFormatter(file_formatter)
        logger.addHandler(file_handler)  # 将文件处理器添加到日志记录器中

        logger.info(f"======== run_script : {script_name} ==========")

        # 使用 create_task 来避免阻塞
        task = asyncio.create_task(execute_script(script_name, params))  # 创建异步任务

        # 等待任务完成
        result = await task  # 获取任务结果

        logger.info(f"Script completed: {script_name}")
        logger.info(f"Result: {result} ")
        logger.info("\n\n" + "=" * 60 + "\n\n")

        return success_response("run_script OK")  # 返回成功响应
    except Exception as e:
        logger.error(f"Script failed: {str(e)}")  # 记录错误信息
        return {"success": False, "error": str(e)}  # 返回错误信息
    finally:
        # 移除文件日志处理器
        logger.removeHandler(file_handler)  # 从日志记录器中移除文件处理器
        file_handler.close()  # 关闭文件处理器


@router.get("/list_scripts")
async def list_available_scripts():
    """
    获取可用脚本列表。

    返回：
    - 可用脚本的成功响应。
    """
    scripts = get_available_scripts()  # 获取可用脚本
    return success_response(scripts)  # 返回成功响应


# 存储活动连接的字典
active_connections: Dict[str, WebSocket] = {}  # 初始化活动连接字典
