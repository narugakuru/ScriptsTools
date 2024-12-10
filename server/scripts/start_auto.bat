@echo off
REM 激活 conda 环境
call E:\Environment\anaconda3\Scripts\activate.bat fast

REM 启动 Python 脚本
E:\Environment\anaconda3\envs\fast\python.exe E:\CodeAchieve\MyFluent\itTools-fastapi\server\scripts\auto_michecker.py

REM 可选：在脚本执行完毕后，停留在命令行窗口
pause