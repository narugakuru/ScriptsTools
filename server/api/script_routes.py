from fastapi import APIRouter, WebSocket
from typing import Dict, Any
from . import *
from ..utils.logger import ScriptLogger
from ..utils.app_logger import *
from ..utils.param_converter import ParamConverter
from ..schemas.request_models import ScriptRequest
from server.api.result import *
from server.utils.printer_wrapper import format_and_print_params
from server.config import *



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
        # 转换参数
        # args, kwargs = ParamConverter.convert_params(script_name, request.params)

        # 获取logger
        logger = setup_stream_logger(script_name)

        logger.info(f"Starting script: {script_name}")
        # 执行脚本
        result: bool = await execute_script(script_name, params)
        logger.info(f"Script completed: {script_name}")
        logger.info(f"Result: {result}")

        # 收集日志
        log_queue = queue_manager.get_queue(script_name)
        logs = []
        while not log_queue.empty():
            logs.append(await log_queue.get())

        # 移除队列
        queue_manager.remove_queue(script_name)

        print(f"==================logs=====================\n{logs}")

        # 格式化日志为字符串
        formatted_logs = "\\n".join(logs)
        # .replace("\\", "\\\\").replace("\"", "\\\"")
        print(f"==================================\n{formatted_logs}")

        return success_response(f"{logs}")
        # return {"success": True, "data": result}
    except Exception as e:
        logger.error(f"Script failed: {str(e)}")
        return {"success": False, "error": str(e)}



# @router.websocket("/ws/{script_name}")
# async def websocket_endpoint(websocket: WebSocket, script_name: str):
#     await websocket.accept()

#     # 获取或创建logger
#     if script_name not in script_loggers:
#         script_loggers[script_name] = ScriptLogger(script_name)
#     logger = script_loggers[script_name]

#     try:
#         logger.set_websocket(websocket)
#         while True:
#             # 保持连接活跃
#             data = await websocket.receive_text()
#     except Exception:
#         logger.remove_websocket()
#         await websocket.close()
