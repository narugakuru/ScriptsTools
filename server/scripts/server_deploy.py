import paramiko
import os
from pathlib import Path
from scp import SCPClient
from server.scripts.env import hostname, username, password


class ServerDeployer:
    def __init__(self, hostname, username, password, port=22):
        """
        初始化服务器部署类
        :param hostname: 服务器IP地址
        :param username: 用户名
        :param password: 密码
        :param port: SSH端口号（默认22）
        """
        self.hostname = hostname
        self.username = username
        self.password = password
        self.port = port
        self.ssh = None
        self.sftp = None

    def connect(self):
        """建立SSH连接"""
        try:
            self.ssh = paramiko.SSHClient()
            self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            self.ssh.connect(
                hostname=self.hostname,
                username=self.username,
                password=self.password,
                port=self.port,
            )
            self.sftp = self.ssh.open_sftp()
            return True
        except Exception as e:
            print(f"连接失败: {str(e)}")
            return False

    def execute_command(self, command):
        """执行SSH命令"""
        try:
            stdin, stdout, stderr = self.ssh.exec_command(command)
            return stdout.read().decode(), stderr.read().decode()
        except Exception as e:
            print(f"命令执行失败: {str(e)}")
            return None, str(e)

    def upload_folder(self, local_folder, remote_folder):
        pass

    def upload_directory(self, local_folder, remote_folder, ssh_client):
        """
        上传文件夹到服务器
        :param local_folder: 本地文件夹路径
        :param remote_folder: 远程文件夹路径
        """
        with SCPClient(ssh_client.get_transport()) as scp:
            scp.put(local_folder, remote_path=remote_folder, recursive=True)
            print(f"{local_folder} 上传到 {remote_folder} 成功")

    def deploy_html(self, local_folder, remote_folder):
        """
        部署HTML文件到服务器
        :param local_folder: 本地HTML文件夹路径
        :return: 布尔值表示是否成功
        """
        try:
            # 1. 连接服务器
            if not self.connect():
                return False

            # 2. 切换到root用户
            self.execute_command(f"echo {self.password} | sudo -S su")

            # 3. 上传文件到/home/ubuntu/html_1101

            if not self.upload_folder(local_folder, remote_folder):
                return False

            # 4. 复制文件到/var/www/html/
            _, error = self.execute_command(
                f"echo {self.password} | sudo -S cp -r {remote_folder}/* /var/www/html/"
            )
            if error:
                print(f"复制文件失败: {error}")
                return False

            return True

        except Exception as e:
            print(f"部署过程出错: {str(e)}")
            return False

        finally:
            if self.sftp:
                self.sftp.close()
            if self.ssh:
                self.ssh.close()


def deploy_to_server(local_folder, remote_folder):
    """
    便捷的部署接口
    :param local_folder: 本地HTML文件夹路径
    :return: 布尔值表示是否成功
    """
    deployer = ServerDeployer(hostname, username, password)
    return deployer.deploy_html(local_folder, remote_folder)


# 使用示例
if __name__ == "__main__":
    local_folder = "E:/WorkSpace/WebKaisyu/html_1104"
    remote_folder = "/home/ubuntu/kaikei/html_11011"
    success = deploy_to_server(local_folder, remote_folder)
    if success:
        print("部署成功！")
    else:
        print("部署失败！")
