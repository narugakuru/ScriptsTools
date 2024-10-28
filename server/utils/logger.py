# backend/utils/logger.py
import logging
from typing import Optional
from fastapi import WebSocket

class WebSocketHandler(logging.Handler):
    def __init__(self):
        super().__init__()
        self.websocket: Optional[WebSocket] = None

    async def emit(self, record):
        if self.websocket:
            try:
                log_entry = self.format(record)
                await self.websocket.send_text(log_entry)
            except Exception:
                self.handleError(record)

class ScriptLogger:
    def __init__(self, script_name: str):
        self.logger = logging.getLogger(script_name)
        self.handler = WebSocketHandler()
        self.logger.addHandler(self.handler)
        self.logger.setLevel(logging.INFO)

    def set_websocket(self, websocket: WebSocket):
        self.handler.websocket = websocket

    def remove_websocket(self):
        self.handler.websocket = None