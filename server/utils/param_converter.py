from pydantic import BaseModel
from typing import Dict, Any, Optional
# backend/utils/param_converter.py
class ParamConverter:
    """参数转换器"""
    @staticmethod
    def convert_params(script_name: str, params: Dict[str, Any]) -> tuple:
        """
        将字典参数转换为位置参数和关键字参数
        返回 (args, kwargs)
        """
        # 可以通过配置文件或装饰器来定义参数映射
        param_mappings = {
            "copy_list": {
                "position_args": ["origin_path", "copy_path", "file_list"],
                "keyword_args": []
            }
            # 其他脚本的参数映射...
        }
        
        mapping = param_mappings.get(script_name, {})
        args = [params.get(arg) for arg in mapping.get("position_args", [])]
        kwargs = {k: v for k, v in params.items() 
                 if k in mapping.get("keyword_args", [])}
        
        return args, kwargs