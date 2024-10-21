import os
import shutil

# 目标文件夹路径
target_dir = r"V:\UserTEMP"
# target_dir = r"V:\UserTMP"

# 需要检查的子文件夹名称列表
check_dirs = ["EBWebView", "gen_py"]

for entry in os.listdir(target_dir):
    # 构建子文件夹的完整路径
    sub_dir = os.path.join(target_dir, entry)

    # 如果是目录,则进入
    if os.path.isdir(sub_dir):
        # 标记是否需要删除该目录
        remove_dir = False

        # 检查是否包含需要检查的子文件夹
        for check_dir in check_dirs:
            check_path = os.path.join(sub_dir, check_dir)
            if os.path.exists(check_path):
                remove_dir = True
                break

        # 如果没有子文件夹,也标记为需要删除
        if not os.listdir(sub_dir):
            remove_dir = True

        # 如果需要删除,则删除整个目标文件夹
        if remove_dir:
            try:
                shutil.rmtree(sub_dir)
                print(f"已删除目录: {sub_dir}")
            except Exception as e:
                print(f"删除目录时出错: {sub_dir}")
                print(e)
