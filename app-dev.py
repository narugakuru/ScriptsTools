import webview
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import os
import sys
import time
import subprocess

# 获取当前目录
if getattr(sys, "frozen", False):
    base_path = sys._MEIPASS  # PyInstaller 打包后的临时路径
else:
    base_path = os.path.dirname(os.path.abspath(__file__))  # 当前目录

class ChangeHandler(FileSystemEventHandler):
    def __init__(self, restart_function):
        self.restart_function = restart_function

    def on_modified(self, event):
        if event.src_path.endswith(".py"):
            print(f"{event.src_path} has been modified, restarting FastAPI server...")
            self.restart_function()
            print("Restart complete.")  # 输出重启完成

def restart_fastapi():
    global fastapi_process
    if fastapi_process and fastapi_process.poll() is None:
        fastapi_process.terminate()  # 终止进程
        fastapi_process.wait()  # 等待进程终止
    fastapi_process = subprocess.Popen([sys.executable, "server.py"])

if __name__ == "__main__":
    fastapi_process = None
    restart_fastapi()  # 启动 FastAPI 服务器

    # 设置文件监控
    event_handler = ChangeHandler(restart_fastapi)
    observer = Observer()
    monitor_directory = f'{base_path}/server'
    observer.schedule(event_handler, path=monitor_directory, recursive=True)
    observer.start()

    # # PyWebView启动桌面应用窗口，嵌入FastAPI前端
    # webview.create_window("WebViewTools", "http://127.0.0.1:8000/index.html", frameless=False, easy_drag=True)
    # logo = "E:\CodeAchieve\MyFluent\itTools-fastapi\logo.png"
    # webview.start(icon=logo, debug=False)

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
    if fastapi_process:
        fastapi_process.terminate()
        fastapi_process.wait()
