# backend/scripts/__init__.py
from typing import Dict, Any
import importlib
import os
from  server.config import config
def get_available_scripts() -> list:
    """获取scripts目录下所有可用的脚本"""
    scripts_dir = config.scripts_path
    scripts = []
    for file in os.listdir(scripts_dir):
        if file.endswith('.py') and not file.startswith('__'):
            scripts.append(file[:-3])
    return scripts

async def execute_script(script_name: str, params: Dict[Any, Any]):
    """动态执行脚本"""
    try:
        print(f"========= execute_script: {script_name}==========")
        module = importlib.import_module(f"server.scripts.{script_name}")
        if hasattr(module, 'run'):
            # 创建一个新的事件循环来处理脚本执行
            result = await module.run(script_name, params)
            return result
        raise Exception(f"Script {script_name} doesn't have run function")
    except Exception as e:
        raise Exception(f"Failed to execute script: {str(e)}")


# async def execute_script(script_name: str, params: Dict[Any, Any]):
#     """动态执行脚本"""
#     try:
#         print(f"========= execute_script: {script_name}==========")
#         module = importlib.import_module(f"server.scripts.{script_name}")
#         if hasattr(module, 'run'):
#             return await module.run(script_name, params)
#         raise Exception(f"Script {script_name} doesn't have run function")
#     except Exception as e:
#         raise Exception(f"Failed to execute script: {str(e)}")
