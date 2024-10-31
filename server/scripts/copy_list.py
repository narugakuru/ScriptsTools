# 批量复制文件列表，包括文件夹结构
import os
import shutil
import time
import tqdm
import logging
# from  server.utils.app_logger import *
from server.utils.printer_wrapper import format_and_print_params
import asyncio

# 函数功能：标准化文件路径
# 参数列表：
# raw_paths (str): 原始文件路径字符串，可能包含多个路径，每行一个
# 返回值：一个标准化后的路径列表，所有路径都将以斜杠开头，且符合 UNIX 风格
def normalize_paths(raw_paths):
    normalized_paths = []

    # 按行分割原始字符串并处理每一行
    for path in raw_paths.strip().splitlines():
        # 去除多余空格，将反斜杠替换为正斜杠，并确保路径以正斜杠开头
        path = path.strip().replace("\\", "/")
        if not path.startswith("/"):
            path = "/" + path
        normalized_paths.append(path)

    return normalized_paths


# 函数功能：按结构复制文件和文件夹
# 参数列表：
# origin_path (str): 源文件夹的路径
# copy_path (str): 目标文件夹的路径
# file_list (list或str): 要复制的文件列表，可以是字符串列表或单个字符串
# 返回值：无返回值，异步执行文件复制任务
async def copy_files_with_structure(origin_path, copy_path, file_list):
    logger.info("====== copy_files_with_structure =======")

    if not isinstance(file_list, list):
        logger.info("====== file_list is normalizing! ======")
        file_list = await normalize_paths(file_list)

    print(f'copy folder from {origin_path} to {copy_path}')

    # 创建目标文件夹（如果不存在）
    await asyncio.to_thread(os.makedirs, os.path.dirname(copy_path), exist_ok=True)

    for file in file_list:  # 移除tqdm，因为它可能影响异步操作
        file = file.lstrip("/")
        source = os.path.join(origin_path, file)

        # 使用异步方式检查文件是否存在
        if await asyncio.to_thread(os.path.isfile, source):
            target = os.path.join(copy_path, file)

            # 创建目标文件的目录
            await asyncio.to_thread(os.makedirs, os.path.dirname(target), exist_ok=True)

            # 异步复制文件
            await asyncio.to_thread(shutil.copy2, source, target)
            logger.info(f"\nCopied: {source} -> {target}")

            # 让出控制权，使日志有机会被处理
            await asyncio.sleep(0.01)
        else:
            logger.info(f"\nSkipped: {source} (Not a file)")
            await asyncio.sleep(0.01)


# 函数功能：运行复制操作的主函数
# 参数列表：
# script_name (str): 脚本名称，用于日志记录
# params (dict): 包含复制操作所需参数的字典，键应与copy_files_with_structure函数的参数匹配
# 返回值：布尔值，指示运行是否成功，若失败则返回错误信息
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
