from fastapi import Request
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
from server.componnet.app_logger import setup_logger  # 假设你有一个单独的日志配置模块

# 初始化日志记录器
logger = setup_logger()

class LogMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        logger.info(f"收到请求: {request.method} {request.url}")
        try:
            response = await call_next(request)
        except Exception as e:
            logger.error(f"处理请求时出错: {str(e)}")
            return JSONResponse(status_code=500, content={"message": "服务器错误"})
        
        logger.info(f"返回响应: {response.status_code}")
        return response
