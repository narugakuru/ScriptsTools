from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from . import *
from server.api.result import *
from server.utils.printer_wrapper import format_and_print_params
from server.config import *
from server.utils.app_logger import *
from typing import Dict, Set


router = APIRouter()


@router.get("/list_scripts")
async def list_available_scripts():
    """获取可用脚本列表"""
    scripts = get_available_scripts()
    return success_response(scripts)

@format_and_print_params
@router.post("/{script_name}")
async def run_script(script_name: str, params: dict):
    """执行脚本并返回结果"""
    try:
        # 获取logger
        logger = setup_stream_logger(script_name)

        logger.info(f"Starting script: {script_name}")
        # 执行脚本
        result: bool = await execute_script(script_name, params)
        logger.info(f"Script completed: {script_name}")
        logger.info(f"Result: {result}")
        
        # logs = collect_log(script_name)

        # 通知所有相关的WebSocket连接脚本执行完成
        if script_name in active_connections:
            for connection in active_connections[script_name]:
                await connection.send_text("Script execution completed")
        
        return success_response(f"run_script OK")
        # return {"success": True, "data": result}
    except Exception as e:
        logger.error(f"Script failed: {str(e)}")
        return {"success": False, "error": str(e)}


# 存储活跃的WebSocket连接
active_connections: Dict[str, Set[WebSocket]] = {}

# WebSocket接口
@router.websocket("/ws/{script_name}")
async def websocket_endpoint(websocket: WebSocket, script_name: str):
    await websocket.accept()
    
    # 将WebSocket连接添加到对应脚本的连接集合中
    if script_name not in active_connections:
        active_connections[script_name] = set()
    active_connections[script_name].add(websocket)
    
    try:
        # 获取该脚本的日志队列
        log_queue = queue_manager.get_queue(script_name)
        
        # 持续监听队列并发送日志
        while True:
            try:
                # 非阻塞方式获取日志
                while not log_queue.empty():
                    log_record = log_queue.get_nowait()
                    if isinstance(log_record, logging.LogRecord):
                        # 格式化日志消息
                        formatted_log = f"{log_record.asctime} - {log_record.levelname} - {log_record.getMessage()}"
                        await websocket.send_text(formatted_log)
                
                # 适当的休眠以避免过度CPU使用
                await asyncio.sleep(0.1)
                
            except asyncio.CancelledError:
                break
    finally:
        active_connections[script_name].remove(websocket)
        if not active_connections[script_name]:
            del active_connections[script_name]
        
        

async def collect_log(script_name):
    # 收集日志
    log_queue = queue_manager.get_queue(script_name)
    logs = []
    while not log_queue.empty():
        logs.append(await log_queue.get())

    print(f"==================logs=====================\n{logs}")
    # 格式化日志为字符串
    formatted_logs = "\\n".join(logs)
    # .replace("\\", "\\\\").replace("\"", "\\\"")
    print(f"==================================\n{formatted_logs}")
    
    # 移除队列
    queue_manager.remove_queue(script_name)
    return formatted_logs