# backend/schemas/request_models.py
from pydantic import BaseModel
from typing import Dict, Any, Optional

class ScriptRequest(BaseModel):
    """通用脚本请求模型"""
    params: Dict[str, Any]
