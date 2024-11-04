import os
import paramiko
from scp import SCPClient
import logging
import getpass

# 配置日志
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)

# 启用 Paramiko 调试日志
paramiko.util.log_to_file("paramiko.log", level="INFO")


# 定义服务器信息
hostname = "153.120.83.98"
username = "ubuntu"
password = "STIDTI2024"


def create_ssh_client(server, user, password):
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        # 增加超时时间
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

    except paramiko.SSHException as ssh_e:
        logging.error(f"SSH 连接错误: {ssh_e}")
        raise
    except FileNotFoundError as fnf_e:
        logging.error(f"文件未找到: {fnf_e}")
        raise
    except scp.SCPException as scp_e:
        logging.error(f"SCP 错误: {scp_e}")
        raise
    except Exception as e:
        logging.error(f"上传失败: {e}")
        raise


def execute_command(ssh_client, command):
    try:
        stdin, stdout, stderr = ssh_client.exec_command(command)
        logging.info(f"执行命令: {command}")
        if stdout:
            logging.info("输出:\n" + stdout.read().decode())
        if stderr:
            logging.error("错误:\n" + stderr.read().decode())
    except Exception as e:
        logging.error(f"命令执行失败: {e}")
        raise


def execute_command_as_root(ssh_client, command, root_password):
    try:
        # 使用 sudo 执行命令并输入 root 密码
        full_command = f"echo {root_password} | sudo -S {command}"
        # full_command = f"{command}"
        logging.info(f"即将执行{full_command}")
        key = input("请输入yes确认: ")
        if key == "yes":
            stdin, stdout, stderr = ssh_client.exec_command(full_command)

            logging.info(f"以 root 用户执行命令: {command}")

            stdout_content = stdout.read().decode()
            stderr_content = stderr.read().decode()

            if stdout_content:
                logging.info("输出:\n" + stdout_content)
            if stderr_content:
                logging.error("错误信息:\n" + stderr_content)
        else:
            logging.info("取消执行命令")
    except Exception as e:
        logging.error(f"命令执行失败: {e}")
        raise


def deploy(local_base, remote_base, target_folder, deploy_path):
    local_folder = os.path.join(local_base, target_folder)
    remote_folder = os.path.join(remote_base, target_folder)
    print("remote_folder:" + remote_folder)
    ssh_client = None
    try:
        # 连接到服务器
        ssh_client = create_ssh_client(hostname, username, password)

        # 上传本地目录
        upload_directory(local_folder, remote_base, ssh_client)

        # execute_command_as_root(
        #     ssh_client, f"cp -r {remote_folder}/* {deploy_path}", password
        # )

    finally:
        if ssh_client:
            ssh_client.close()
            logging.info("SSH 连接已关闭")


# 对外接口
def deploy_project():
    local_base = "E:/WorkSpace/WebKaisyu/"
    remote_base = "/home/ubuntu/kaikei/"

    target_folder = "html_1104_10"
    deploy_path = "/var/www/html/"
    deploy(local_base, remote_base, target_folder, deploy_path)


if __name__ == "__main__":
    deploy_project()
