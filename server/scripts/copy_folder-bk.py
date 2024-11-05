import os
import shutil
import logging
import sys
from datetime import datetime
from tqdm import tqdm

# 设置日志配置
def setup_logging(log_file_path):
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    # FileHandler 用于将日志写入文件
    file_handler = logging.FileHandler(log_file_path, mode='a', encoding='utf-8')
    file_handler.setLevel(logging.INFO)

    # StreamHandler 用于将日志输出到控制台
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)

    # 日志格式
    formatter = logging.Formatter('%(asctime)s - %(message)s')
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)

    # 添加处理器
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    # 确保日志文件实时写入
    file_handler.flush = file_handler.stream.flush

def print_progress(total_files, copied_files):
    # 动态更新控制台显示，不换行，用 \r 使得光标返回行首并覆盖前面的内容
    sys.stdout.write(f'\rTotal files processed: {total_files}, Files copied: {copied_files}')
    sys.stdout.flush()

def copy_folders_with_exclusion_and_time_check(origin_path, copy_path, exclude_exts, exclude_dirs, all_copy):
    total_files = 0  # 遍历的文件总数
    copied_files = 0  # 实际复制的文件数
    log_interval = 500  # 每 500 次进行一次日志记录
    # 创建一个进度条用于遍历文件
    traversal_pbar = tqdm(desc="Traversing Files", unit="files", position=0)
    # 创建另一个进度条用于处理文件
    processing_pbar = tqdm(desc="Processing Files", unit="files", position=1)
    

    for root, dirs, files in os.walk(origin_path):
        # 忽略指定的文件夹 (在遍历子目录之前从 dirs 列表中移除)
        dirs[:] = [d for d in dirs if d not in exclude_dirs]

        # 构建目标路径
        relative_path = os.path.relpath(root, origin_path)
        target_dir = os.path.join(copy_path, relative_path)

        # 创建目标目录
        if not os.path.exists(target_dir):
            os.makedirs(target_dir)

        # 复制文件，排除指定扩展名的文件
        for file in files:
            total_files += 1  # 统计遍历的文件总数
            traversal_pbar.update(1)  # 每处理一个文件更新一次进度条
            if not any(file.lower().endswith(ext) for ext in exclude_exts):
                source_file = os.path.join(root, file)
                target_file = os.path.join(target_dir, file)

                if should_copy(source_file, target_file) or all_copy:
                    # all_copy=True 直接执行更新
                    shutil.copy2(source_file, target_file)
                    copied_files += 1  # 统计实际复制的文件数
                    processing_pbar.update(1)
                    logging.info(f'Copied: {source_file} to {target_file}')  # 记录日志

            # 实时更新控制台的文件计数
            # print_progress(total_files, copied_files)
            
            # 如果到达500个文件的整数倍，输出日志
            if total_files % log_interval == 0:
                logging.info(f'Total files processed: {total_files}, Files copied: {copied_files}')

    # 最后输出一次日志
    logging.info(f'Final file count: Total files processed: {total_files}, Files copied: {copied_files}')
    # 清除进度条行，避免最后遗留多余信息
    print("\nDone.")

def should_copy(source_file, target_file):
    # 如果目标文件不存在，直接复制
    if not os.path.exists(target_file):
        return True

    # 获取文件的修改时间
    source_mtime = os.path.getmtime(source_file)
    target_mtime = os.path.getmtime(target_file)

    # 如果源文件的修改时间比目标文件新，则复制
    return source_mtime > target_mtime


if __name__ == "__main__":
    origin_path = r"Z:\ssl-htdocs"  # 源文件夹路径
    copy_path = r"E:\WorkSpace\WebKaisyu\ssl-htdocs-local"  # 目标文件夹路径
    all_copy = False  # 设置是否强制更新所有文件

    # 设置日志输出到文件和控制台，并实时刷新日志文件
    current_time = datetime.now().strftime("%Y%m%d_%H%M%S")  # 获取当前日期时间
    log_file_path = f'{copy_path}/copy_log_{current_time}.txt'  # 更新日志文件路径
    setup_logging(log_file_path)

    exclude_exts = ['.pdf', '.PDF']  # 排除的文件扩展名
    exclude_dirs = ['.git', 'pdf']  # 排除的文件夹

    copy_folders_with_exclusion_and_time_check(origin_path, copy_path, exclude_exts, exclude_dirs, all_copy)
