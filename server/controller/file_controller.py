from email import message
from fastapi import APIRouter

from server.controller.result import success_response
from ..utils.copy_folder_rule import copy_folders
from ..utils.copy_list import copy_files_with_structure
from pydantic import BaseModel
import json  # 导入 json 模块
    
class ResponseModel(BaseModel):
    message: str
    code: int
    data: dict

# 创建用户相关的 API 路由
router = APIRouter()

@router.get("/users")
async def get_users():
    return [{"id": 1, "name": "Alice"}, {"id": 2, "name": "Bob"}]

@router.get("/users/{user_id}")
async def get_user(user_id: int):
    return {"id": user_id, "name": "Alice"}

@router.post("/copy_folders")
async def copy_folder(data: dict):
    print(json.dumps(data, indent=4, ensure_ascii=False))  # 格式化输出字典内容
    
    return {"message": "OK"}

@router.post("/copy_list")
async def copy_list(data: dict):
    print(json.dumps(data, indent=4, ensure_ascii=False))  # 格式化输出字典内容
    # copy_files_with_structure(**data)
    return success_response("api is success !!")


""" from pydantic import BaseModel
from typing import List

class CopyListRequest(BaseModel):
    origin_path: str
    copy_path: str
    file_list: List[str]

@router.post("/api/copy_list")
async def copy_list(request: CopyListRequest):
    return copy_files_with_structure(**request.model_dump()) """
