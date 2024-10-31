import os
import shutil
import logging
from datetime import datetime
from tqdm import tqdm

# 通用文件复制逻辑
def copy_files(origin_path, copy_path, exclude_exts, exclude_dirs, include_dirs, all_copy, filter_func):

    # 创建一个进度条用于遍历文件
    traversal_pbar = tqdm(desc="Traversing Files", unit="files", position=0)
    # 创建另一个进度条用于处理文件
    processing_pbar = tqdm(desc="Processing Files", unit="files", position=1)

    for root, dirs, files in os.walk(origin_path):
        # 过滤文件夹
        dirs[:] = filter_func(dirs, exclude_dirs, include_dirs)

        # 构建目标路径
        relative_path = os.path.relpath(root, origin_path)
        target_dir = os.path.join(copy_path, relative_path)

        # 创建目标目录
        if not os.path.exists(target_dir):
            os.makedirs(target_dir)

        # 复制文件，排除指定扩展名的文件
        for file in files:

            traversal_pbar.update(1)  # 每处理一个文件更新一次进度条
            if not any(file.lower().endswith(ext) for ext in exclude_exts):
                source_file = os.path.join(root, file)
                target_file = os.path.join(target_dir, file)

                if should_copy(source_file, target_file) or all_copy:
                    # all_copy=True 直接执行更新
                    shutil.copy2(source_file, target_file)

                    processing_pbar.update(1)
                    logging.info(f'Copied: {source_file} to {target_file}')  # 记录日志

        # 获取最终结果并输出
        traversed_files = traversal_pbar.format_dict['n']
        processed_files = processing_pbar.format_dict['n']
        logging.info(f'{dirs}: Total files processed: {traversed_files}, Files copied: {processed_files}')


# 复制所有文件，排除指定的目录
def copy_folders_with_exclusion(origin_path, copy_path, exclude_exts, exclude_dirs, all_copy):
    def filter_func(dirs, exclude_dirs, include_dirs):
        return [d for d in dirs if d not in exclude_dirs]
    
    copy_files(origin_path, copy_path, exclude_exts, exclude_dirs, None, all_copy, filter_func)

# 仅复制包含在 include_dirs 中的目录的文件
def copy_folders_with_inclusion(origin_path, copy_path, exclude_exts, include_dirs, all_copy):
    def filter_func(dirs, exclude_dirs, include_dirs):
        # 仅保留 include_dirs 中的文件夹
        return [d for d in dirs if d in include_dirs]
    
    copy_files(origin_path, copy_path, exclude_exts, None, include_dirs, all_copy, filter_func)

def should_copy(source_file, target_file):
    # 如果目标文件不存在，直接复制
    if not os.path.exists(target_file):
        return True

    # 获取文件的修改时间
    source_mtime = os.path.getmtime(source_file)
    target_mtime = os.path.getmtime(target_file)

    # 如果源文件的修改时间比目标文件新，则复制
    return source_mtime > target_mtime


def copy_folders(
    origin_path, copy_path, exclude_exts, exclude_dirs, include_dirs, all_copy
):

    try:
        # 设置日志输出到文件和控制台，并实时刷新日志文件
        current_time = datetime.now().strftime("%Y%m%d_%H%M%S")  # 获取当前日期时间
        log_file_path = f"{copy_path}/copy_log_{current_time}.txt"  # 更新日志文件路径
        fileHandler = logging.FileHandler(log_file_path, mode="a", encoding="utf-8")
        logger.addHandler(fileHandler)

        if exclude_dirs:  # exclude_dirs 是空列表，也会进入 else 分支
            # 使用排除目录方式
            copy_folders_with_exclusion(
                origin_path, copy_path, exclude_exts, exclude_dirs, all_copy
            )
        elif include_dirs:
            # 使用包含目录方式
            copy_folders_with_inclusion(
                origin_path, copy_path, exclude_exts, include_dirs, all_copy
            )
        else:
            logger.error("没有指定目录过滤方式！")
    except:
        logger.error("参数错误！")
    finally:
        logger.removeHandler(fileHandler)


async def run(script_name, params):
    """
    脚本入口函数
    参数通过关键字参数传入
    """
    try:
        # 设置全局变量 logger
        global logger
        logger = logging.getLogger(script_name)
        copy_folders(**params)
        return True
    except Exception as e:
        return str(e)
