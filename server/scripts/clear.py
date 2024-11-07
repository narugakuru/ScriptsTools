import os
from send2trash import send2trash


def clear_nfo_files(directory):
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith(".nfo"):
                file_path = os.path.join(root, file)
                send2trash(file_path)
                print(f"Moved to trash: {file_path}")


if __name__ == "__main__":
    directory_to_clear = "E:\ProgramFilesData\ProgramFiles"  # 替换为你要清理的目录路径
    clear_nfo_files(directory_to_clear)
