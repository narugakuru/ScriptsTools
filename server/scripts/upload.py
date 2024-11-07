import os
import paramiko
from scp import SCPClient
import logging

# from  server.utils.app_logger import *
from server.utils.printer_wrapper import format_and_print_params
import asyncio
from server.scripts.env import hostname, username, password


global logger
# 获取当前文件的名词
current_file_name = __name__.split(".")[-1]
logger = logging.getLogger(current_file_name)

logger_info = {
    "name": logger.name,
    "level": logger.level,
    "handlers": [handler.__class__.__name__ for handler in logger.handlers],
    "propagate": logger.propagate,
}
print(f"{current_file_name}文件的Logger 信息: {logger_info}")

def create_ssh_client(server, user, password):

    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        client.connect(server, username=user, password=password, timeout=5)
        logger.info("SSH 连接成功")
    except paramiko.SSHException as e:
        logging.error(f"SSH 连接失败: {e}")
        raise
    return client


async def upload_directory(local_folder, remote_base, ssh_client):
    try:
        logger_info = {
            "name": logger.name,
            "level": logger.level,
            "handlers": [handler.__class__.__name__ for handler in logger.handlers],
            "propagate": logger.propagate,
        }
        print(f"upload_directory函数的Logger 信息: {logger_info}")
        # 统计本地文件夹的文件总数
        file_count = sum([len(files) for _, _, files in os.walk(local_folder)])
        logger.info(f"本地文件夹 {local_folder} 中的文件总数: {file_count}")

        # 打印出整个文件列表
        for root, dirs, files in os.walk(local_folder):
            for file in files:
                logger.info(f"文件列表: {os.path.join(root, file)}")
            await asyncio.sleep(0.01)

        with SCPClient(ssh_client.get_transport()) as scp:
            # =============================================================================================
            scp.put(local_folder, remote_path=remote_base, recursive=True)
            logger.info(f"{local_folder} 上传到 {remote_base} 成功")

    except Exception as e:
        logging.error(f"上传失败: {e}")
        raise


@format_and_print_params
async def upload(local_base, remote_base, target_folder):

    local_folder = os.path.join(local_base, target_folder)
    ssh_client = None
    try:
        # 连接到服务器
        ssh_client = create_ssh_client(hostname, username, password)
        await asyncio.sleep(0.01)
        # 上传本地目录
        await upload_directory(local_folder, remote_base, ssh_client)

        return True

    except Exception as e:
        logging.error(f"上传失败: {e}")
        return False
    finally:
        if ssh_client:
            ssh_client.close()
            logger.info("SSH 连接已关闭")


# 函数功能：运行复制操作的主函数
# 参数列表：
# script_name (str): 脚本名称，用于日志记录
# params (dict): 包含复制操作所需参数的字典，键应与copy_files_with_structure函数的参数匹配
# 返回值：布尔值，指示运行是否成功，若失败则返回错误信息
# local_base, remote_base, target_folder
async def run(script_name, params):
    try:
        # global logger
        # logger = logging.getLogger(script_name)
        logger.info(f"========== run! ： {script_name} ===========")

        # 创建一个新的事件循环来处理文件操作
        result = await upload(**params)

        return result

    except Exception as e:
        logger.error(f"Error in run: {str(e)}")
        return str(e)


if __name__ == "__main__":

    local_base = "E:/WorkSpace/WebKaisyu/"
    remote_base = "/home/ubuntu/kaikei/"
    target_folder = "html_1104_11"

    upload(local_base, remote_base, target_folder)
