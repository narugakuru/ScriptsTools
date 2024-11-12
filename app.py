import uvicorn
import webview
import os, sys, threading

# 获取当前目录
if getattr(sys, "frozen", False):
    base_path = sys._MEIPASS  # PyInstaller 打包后的临时路径
else:
    base_path = os.path.dirname(os.path.abspath(__file__))  # 当前目录


def start_fastapi():
    config = uvicorn.Config(
        "server.main:app", host="127.0.0.1", port=8000, log_level="info", reload=False
    )
    server = uvicorn.Server(config)
    server.run()


if __name__ == "__main__":

    fastapi_thread = threading.Thread(target=start_fastapi)
    fastapi_thread.start()

    # PyWebView启动桌面应用窗口，嵌入FastAPI前端
    webview.create_window(
        "WebViewTools",
        "http://127.0.0.1:8000/index.html",
        frameless=False,
        easy_drag=True,
    )
    logo = "E:\CodeAchieve\MyFluent\itTools-fastapi\logo.png"
    webview.start(icon=logo, debug=False)
