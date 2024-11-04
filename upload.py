import os
import paramiko
from scp import SCPClient
import logging

# 配置日志
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)

# 定义服务器信息
hostname = "153.120.83.98"
username = "ubuntu"
password = "STIDTI2024"

def create_ssh_client(server, user, password):
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        client.connect(server, username=user, password=password, timeout=10)
        logging.info("SSH 连接成功")
    except paramiko.SSHException as e:
        logging.error(f"SSH 连接失败: {e}")
        raise
    return client

def upload_directory(local_folder, remote_base, ssh_client):
    try:
        # 统计本地文件夹的文件总数
        file_count = sum([len(files) for _, _, files in os.walk(local_folder)])
        logging.info(f"本地文件夹 {local_folder} 中的文件总数: {file_count}")

        # 打印出整个文件列表
        for root, dirs, files in os.walk(local_folder):
            for file in files:
                logging.info(f"文件列表: {os.path.join(root, file)}")

        with SCPClient(ssh_client.get_transport()) as scp:
            scp.put(local_folder, remote_path=remote_base, recursive=True)
            logging.info(f"{local_folder} 上传到 {remote_base} 成功")

    except Exception as e:
        logging.error(f"上传失败: {e}")
        raise


def upload(local_base, remote_base, target_folder):
    local_folder = os.path.join(local_base, target_folder)
    ssh_client = None
    try:
        # 连接到服务器
        ssh_client = create_ssh_client(hostname, username, password)

        # 上传本地目录
        upload_directory(local_folder, remote_base, ssh_client)
    finally:
        if ssh_client:
            ssh_client.close()
            logging.info("SSH 连接已关闭")


# 对外接口
def deploy_project():
    local_base = "E:/WorkSpace/WebKaisyu/"
    remote_base = "/home/ubuntu/kaikei/"
    target_folder = "html_1104_10"

    upload(local_base, remote_base, target_folder)


if __name__ == "__main__":
    deploy_project()
