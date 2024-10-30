# 批量复制文件列表，包括文件夹结构
import os
import shutil
import time
import tqdm
import logging
# from  server.utils.app_logger import *
from server.utils.printer_wrapper import format_and_print_params

origin_path = r"E:\WorkSpace\WebKaisyu\ssl-htdocs-local"
copy_path = r"E:\WorkSpace\WebKaisyu\html_1024"

# String of file paths (could be from a file or input)
file_list = r"""
common\css\common.css
jbaudit\target\02.html
jbaudit\target\04.html
jbaudit\target\05.html
jbaudit\target\06.html
effort\flow.html
effort\operation\index.html
/pr/kensa/activity/demand_r04_02.html
common2\css\english.css
english\index.html
english\template\footer.php
common\template\footer.php
common2\tmp\footer.php
common2\css\basic.css
"""


# Function to normalize paths
async def normalize_paths(raw_paths):
    normalized_paths = []

    # Split the raw string by lines and process each line
    for path in raw_paths.strip().splitlines():
        # Strip whitespace, replace backslashes with forward slashes, and ensure it starts with a forward slash
        path = path.strip().replace("\\", "/")
        if not path.startswith("/"):
            path = "/" + path
        normalized_paths.append(path)

    return normalized_paths


# Function to copy files and recreate folder structure
async def copy_files_with_structure(origin_path, copy_path, file_list):

    # script_name = os.path.basename(__file__).split('.')[0]
    # logger = logger_init(script_name)
    logger.info("====== copy_files_with_structure =======")

    if not isinstance(file_list, list):
        logger.info("====== file_list is normalizing! ======")
        file_list = normalize_paths(file_list)

    print(f'copy folder from {origin_path} to {copy_path}')

    os.makedirs(os.path.dirname(copy_path), exist_ok=True)

    for file in tqdm.tqdm(file_list):
        # Remove leading '/' to avoid issues with os.path.join
        file = file.lstrip('/')

        # Get full path of the source file
        source = os.path.join(origin_path, file)

        # Check if the source is a file and exists
        if os.path.isfile(source):
            # Create the target file path
            target = os.path.join(copy_path, file)

            # Create directories in the target path if they don't exist
            os.makedirs(os.path.dirname(target), exist_ok=True)

            # Copy the file to the target location
            shutil.copy2(source, target)
            logger.info(f"\nCopied: {source} -> {target}")
            print("==== copy_list logging 打印一次日志 =====")

        else:
            logger.info(f"\nSkipped: {source} (Not a file)")


if __name__ == "__main__":
    # Run the function to copy files
    copy_files_with_structure(origin_path, copy_path, file_list)


# @format_and_print_params
async def run(script_name,params):
    """
    脚本入口函数
    参数通过关键字参数传入
    """
    try:
        # 设置全局变量 logger
        global logger
        logger = logging.getLogger(script_name)
        print(f"========== run! ： {script_name} ===========")
        await copy_files_with_structure(**params)
        return True
    except Exception as e:
        return str(e)
