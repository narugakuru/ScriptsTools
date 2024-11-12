import os
import shutil
import logging


def get_folder_path(path):
    # 如果路径以.csv结尾，则返回其文件夹路径
    if path.endswith(".csv"):
        return os.path.dirname(path)
    # 否则，假设路径是文件夹路径，直接返回
    return path


def backup_file_or_folder(path):
    try:
        # 检查路径是否存在
        if not os.path.exists(path):
            print("路径不存在")
            return False

        # 获取当前文件夹路径
        current_dir = get_folder_path(path)

        # 获取备份目录路径（当前文件夹下的backup文件夹）
        backup_dir = os.path.join(current_dir, "backup")

        # 创建备份目录（如果不存在）
        if not os.path.exists(backup_dir):
            os.makedirs(backup_dir)

        # 获取要备份的目标名称
        item_name = os.path.basename(path)

        # 初始化备份日志
        backup_log = []
        file_count = 0

        # 备份文件或文件夹
        if os.path.isfile(path):
            destination = os.path.join(backup_dir, item_name)
            shutil.copy(path, destination)
            backup_log.append((path, destination))
            file_count += 1
        elif os.path.isdir(path):
            for root, _, files in os.walk(path):
                if root == path:  # 只在顶级文件夹备份文件
                    for file in files:
                        src_file = os.path.join(root, file)
                        dst_file = os.path.join(backup_dir, file)
                        shutil.copy(src_file, dst_file)
                        backup_log.append((src_file, dst_file))
                        file_count += 1
        else:
            print("不支持的路径类型")
            return False

        # 输出日志信息
        logging.basicConfig(level=logging.INFO, format="%(message)s")
        logging.info("备份完成。以下是备份的文件列表：")
        for src, dst in backup_log:
            logging.info(f"备份文件: {src} 到 {dst}")
        logging.info(f"总共备份了 {file_count} 个文件。")

        return True

    except Exception as e:
        print(f"备份失败: {e}")
        return False


async def run(script_name, params):
    """
    脚本入口函数
    参数通过关键字参数传入
    """
    try:
        # 设置全局变量 logger
        global logger
        logger = logging.getLogger(script_name)
        backup_file_or_folder(**params)
        return True
    except Exception as e:
        return str(e)
