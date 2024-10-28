# 批量复制文件列表，包括文件夹结构
import os
import shutil
import tqdm
from  server.utils.app_logger import *
from . import *
from  server.api.result import success_response


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

# Function to copy files and recreate folder structure
def copy_files_with_structure(origin_path, copy_path, file_list):
    
    logger = logger_init()
    logger.info("======copy_files_with_structure=======")
    
    if file_list is str:
        logger.info("file_list is normalizing!!!")
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
        else:
            logger.info(f"\nSkipped: {source} (Not a file)")


if __name__ == "__main__":
    # Run the function to copy files
    copy_files_with_structure(origin_path, copy_path, file_list)

async def run(origin_path: str, copy_path: str, file_list):
    """
    脚本入口函数
    参数通过关键字参数传入
    """
    try:
        copy_files_with_structure(origin_path, copy_path, file_list)
        return success_response("Files copied successfully")
        # return {"result": "success", "message": "Files copied successfully"}
    except Exception as e:
        return {"result": "error", "message": str(e)}