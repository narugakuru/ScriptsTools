import uvicorn

def start_fastapi():
    uvicorn_config = uvicorn.Config("server.main:app", host="127.0.0.1", port=8000, log_level="debug")
    server = uvicorn.Server(uvicorn_config)
    server.run()

if __name__ == "__main__":
    start_fastapi()