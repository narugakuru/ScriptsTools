from sqlalchemy import true
import webview
import uvicorn
import threading

def start_fastapi():
    # /app/main.pyd的app对象需在uvicorn中启动
    uvicorn.run("server.main:app", host="127.0.0.1", port=8000, log_level="debug")

if __name__ == "__main__":
    # 在独立线程中启动FastAPI服务器
    threading.Thread(target=start_fastapi, daemon=True).start()

    # PyWebView启动桌面应用窗口，嵌入FastAPI前端
    webview.create_window("WebViewTools", "http://127.0.0.1:8000/index.html",frameless=False, easy_drag=True)
    # webview.create_window('Woah dude!', 'index.html')
    logo = "E:\CodeAchieve\MyFluent\itTools-fastapi\logo.png"
    webview.start(icon=logo,debug=True)
    