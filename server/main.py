import sys, os, asyncio
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse, FileResponse
from fastapi import FastAPI, WebSocket, BackgroundTasks, Depends
from server.utils.app_logger import (
    setup_logger,
    setup_stream_logger,
    get_new_log_queue,
)
from server.api import script_routes
from server.config import config


app = FastAPI(root_path="/api")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 允许所有源，或指定允许的源
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 将 client/dist 目录挂载为 /api 根目录
app.mount("/static", StaticFiles(directory=config.web_path, html=True), name="static")

# 注册不同的路由模块，没有变化
app.include_router(script_routes.router, prefix="/run_script")


# Vue 前端路由处理，调整路径, web_path是client/dist目录
@app.get("/{full_path:path}")
async def serve_frontend(full_path: str):
    return FileResponse(os.path.join(config.web_path, "index.html"))
# 静态重定向路由，调整路径
@app.get("/index")
async def index():
    return FileResponse(os.path.join(config.web_path, "index.html"))

# ws实时通信
@app.websocket("/ws/{client_id}")
async def websocket_endpoint(
    websocket: WebSocket, log_queue: asyncio.Queue = Depends(get_new_log_queue)
):
    await websocket.accept()
    logger = setup_stream_logger(log_queue)
    try:
        while True:
            log_entry = await log_queue.get()
            await websocket.send_text(log_entry)
    except Exception as e:
        await websocket.close()


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8000)
