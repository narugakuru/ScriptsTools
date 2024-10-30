# 批量复制文件列表，包括文件夹结构
import os
import shutil
import time
import tqdm
import logging
# from  server.utils.app_logger import *
from server.utils.printer_wrapper import format_and_print_params
import asyncio

# Function to normalize paths
def normalize_paths(raw_paths):
    normalized_paths = []

    # Split the raw string by lines and process each line
    for path in raw_paths.strip().splitlines():
        # Strip whitespace, replace backslashes with forward slashes, and ensure it starts with a forward slash
        path = path.strip().replace("\\", "/")
        if not path.startswith("/"):
            path = "/" + path
        normalized_paths.append(path)

    return normalized_paths


# 在copy_files_with_structure函数中修改
async def copy_files_with_structure(origin_path, copy_path, file_list):
    logger.info("====== copy_files_with_structure =======")

    if not isinstance(file_list, list):
        logger.info("====== file_list is normalizing! ======")
        file_list = await normalize_paths(file_list)

    print(f'copy folder from {origin_path} to {copy_path}')

    await asyncio.to_thread(os.makedirs, os.path.dirname(copy_path), exist_ok=True)

    for file in file_list:  # 移除tqdm，因为它可能影响异步操作
        file = file.lstrip("/")
        source = os.path.join(origin_path, file)

        # 使用异步方式检查文件
        if await asyncio.to_thread(os.path.isfile, source):
            target = os.path.join(copy_path, file)

            # 创建目录
            await asyncio.to_thread(os.makedirs, os.path.dirname(target), exist_ok=True)

            # 异步复制文件
            await asyncio.to_thread(shutil.copy2, source, target)
            logger.info(f"\nCopied: {source} -> {target}")

            # 让出控制权，使日志有机会被处理
            await asyncio.sleep(0.01)
        else:
            logger.info(f"\nSkipped: {source} (Not a file)")
            await asyncio.sleep(0.01)


# 修改run函数
async def run(script_name, params):
    try:
        global logger
        logger = logging.getLogger(script_name)
        print(f"========== run! ： {script_name} ===========")

        # 创建一个新的事件循环来处理文件操作
        result = await copy_files_with_structure(**params)
        return True
    except Exception as e:
        logger.error(f"Error in run: {str(e)}")
        return str(e)
