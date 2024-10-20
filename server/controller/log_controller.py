from fastapi import APIRouter,Depends
from fastapi.responses import StreamingResponse
from server.controller.app_logger import setup_stream_logger
import asyncio

router = APIRouter()

# 初始化日志记录器
logger = setup_stream_logger(Depends(asyncio.Queue()))

""" # SSE 端点，用于流式传输日志
@router.get("/stream")
async def stream_logs():
    async def log_generator():
        while True:
            log = await log_queue.get()  # 从队列中获取日志消息
            yield f"data: {log}\n\n"  # 格式化为 SSE 的格式
            await asyncio.sleep(0.1)  # 避免过快传输
            
    return StreamingResponse(log_generator(), media_type="text/event-stream")
 """
@router.get("/hello")
async def root():
    logger.info("收到根目录请求")
    return {"message": "Hello World!"}
