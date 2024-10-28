from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from typing import Any, Optional

def create_standard_response(code: int, message: str, data: Optional[Any] = None):
    standard_response = {
        "code": code,
        "message": message,
        "data": data
    }
    return JSONResponse(content=jsonable_encoder(standard_response))

def success_response(data: Optional[Any] = None):
    return create_standard_response(200, "Success", data)
