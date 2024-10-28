# backend/scripts/__init__.py
from typing import Dict, Any
import importlib
import os

def get_available_scripts() -> list:
    """获取scripts目录下所有可用的脚本"""
    scripts_dir = os.path.dirname(__file__)
    scripts = []
    for file in os.listdir(scripts_dir):
        if file.endswith('.py') and not file.startswith('__'):
            scripts.append(file[:-3])
    return scripts

async def execute_script(script_name: str, params: Dict[Any, Any]):
    """动态执行脚本"""
    try:
        print(f'=========Executing script: {script_name}==========')
        module = importlib.import_module(f"server.scripts.{script_name}")
        if hasattr(module, 'run'):
            return await module.run(**params)
        raise Exception(f"Script {script_name} doesn't have run function")
    except Exception as e:
        raise Exception(f"Failed to execute script: {str(e)}")
