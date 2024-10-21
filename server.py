import uvicorn

def start_fastapi():
    config = uvicorn.Config("server.main:app", host="127.0.0.1", port=8000, log_level="debug")
    server = uvicorn.Server(config)
    server.run()

if __name__ == "__main__":
    start_fastapi()