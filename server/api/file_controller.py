from email import message
from fastapi import APIRouter

from server.api.result import success_response
from ..scripts.copy_folder_rule import copy_folders
from ..scripts.copy_list import copy_files_with_structure
from pydantic import BaseModel
from server.utils.app_logger import *
import json  # 导入 json 模块
    
class ResponseModel(BaseModel):
    message: str
    code: int
    data: dict

# 创建用户相关的 API 路由
router = APIRouter()
@router.post("/copy_folders")
async def copy_folder(data: dict):
    print(json.dumps(data, indent=4, ensure_ascii=False))  # 格式化输出字典内容
    
    return {"message": "OK"}

@router.post("/copy_list")
async def copy_list(data: dict):
    print(json.dumps(data, indent=4, ensure_ascii=False))  # 格式化输出字典内容
    
    logger_name="copy_list"
    setup_stream_logger(logger_name)

    # 运行复制文件的函数
    copy_files_with_structure(**data)
    
   # 收集日志
    log_queue = queue_manager.get_queue(logger_name)
    logs = []
    while not log_queue.empty():
        logs.append(await log_queue.get())
    
    # 移除队列
    queue_manager.remove_queue(logger_name)
    
    print(f'==================logs=====================\n{logs}')
    
    # 格式化日志为字符串
    formatted_logs = "\\n".join(logs)
    # .replace("\\", "\\\\").replace("\"", "\\\"")
    print(f'==================================\n{formatted_logs}')

    return success_response(f"{logs}")


""" from pydantic import BaseModel
from typing import List

class CopyListRequest(BaseModel):
    origin_path: str
    copy_path: str
    file_list: List[str]

@router.post("/api/copy_list")
async def copy_list(request: CopyListRequest):
    return copy_files_with_structure(**request.model_dump()) """

@router.get("/users")
async def get_users():
    return [{"id": 1, "name": "Alice"}, {"id": 2, "name": "Bob"}]

@router.get("/users/{user_id}")
async def get_user(user_id: int):
    return {"id": user_id, "name": "Alice"}
