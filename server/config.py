import os, sys

class ConfigStatic:
    def __init__(self):
        # 获取当前目录
        if getattr(sys, "frozen", False):
            # 如果应用是通过 PyInstaller 打包的
            self.base_path = sys._MEIPASS  # PyInstaller 打包后的临时路径
        else:
            self.base_path = os.path.dirname(os.path.abspath(__file__))  # 当前目录

        self.root_path = os.path.dirname(self.base_path) # app.py所在路径
        self.scripts_path = os.path.join(self.root_path, "server/scripts")
        self.web_path = os.path.join(self.root_path, "client/dist")

# 创建配置实例
config = ConfigStatic()
