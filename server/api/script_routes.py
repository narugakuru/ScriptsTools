from fastapi import APIRouter, WebSocket
from typing import Dict, Any
from ..utils.logger import ScriptLogger
from ..utils.param_converter import ParamConverter
from . import *
from ..schemas.request_models import ScriptRequest

router = APIRouter()
script_loggers: Dict[str, ScriptLogger] = {}

@router.post("/{script_name}")
async def run_script(script_name: str, params: dict):
    """通用脚本执行接口"""
    try:
        # 动态导入并执行脚本
        result = await execute_script(script_name, params)
        return {"success": True, "data": result}
    except Exception as e:
        return {"success": False, "error": str(e)}

@router.get("/list_scripts")
async def list_available_scripts():
    """获取可用脚本列表"""
    scripts = get_available_scripts()
    return {"scripts": scripts}



''' @router.websocket("/ws/{script_name}")
async def websocket_endpoint(websocket: WebSocket, script_name: str):
    await websocket.accept()
    
    # 获取或创建logger
    if script_name not in script_loggers:
        script_loggers[script_name] = ScriptLogger(script_name)
    logger = script_loggers[script_name]
    
    try:
        logger.set_websocket(websocket)
        while True:
            # 保持连接活跃
            data = await websocket.receive_text()
    except Exception:
        logger.remove_websocket()
        await websocket.close()

@router.post("/run_script/{script_name}")
async def run_script(script_name: str, request: ScriptRequest):
    """执行脚本并返回结果"""
    try:
        # 转换参数
        args, kwargs = ParamConverter.convert_params(script_name, request.params)
        
        # 获取logger
        logger = script_loggers.get(script_name)
        if logger:
            logger.logger.info(f"Starting script: {script_name}")
        
        # 执行脚本
        result = await execute_script(script_name, *args, **kwargs)
        
        if logger:
            logger.logger.info(f"Script completed: {script_name}")
        
        return {"success": True, "data": result}
    except Exception as e:
        if logger:
            logger.logger.error(f"Script failed: {str(e)}")
        return {"success": False, "error": str(e)} '''