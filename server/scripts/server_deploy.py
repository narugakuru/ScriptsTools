import paramiko
import os
from pathlib import Path
from scp import SCPClient
from server.scripts.env import hostname, username, password


def deploy_to_server(local_folder, remote_folder):
    """
    便捷的部署接口
    :param local_folder: 本地HTML文件夹路径
    :return: 布尔值表示是否成功
    """
    pass

# 使用示例
if __name__ == "__main__":
    local_base = "E:/WorkSpace/WebKaisyu/"
    remote_base = "/home/ubuntu/kaikei/"
    target_folder = "html_1112"
    success = deploy_to_server(local_base, remote_base)
    if success:
        print("部署成功！")
    else:
        print("部署失败！")
