import os
import re
from tqdm import tqdm


def get_all_files(directory):
    # 获取目录及其子目录下的所有文件
    all_files = []
    for root, _, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)
            all_files.append(file_path)
    print(f"Total files: {len(all_files)}")
    return all_files


def filter_html_files(all_files):
    # 从所有文件中过滤出 HTML 文件
    return [file for file in all_files if file.endswith(".html")]


def scan_html_files(html_files):
    files_without_template_count = 0
    files_without_template = []
    pattern = re.compile(r"template/favicon\.php")
    encodings = [
        "utf-8",
        "latin-1",
        "iso-8859-1",
        "cp1252",
        "GBK",
        "shift_jis",
        "euc_jp",
        "iso2022_jp",
        "utf_8",
        "utf_16",
        "iso2022_jp_2",
    ]  # 常见编码格式列表

    # 使用 tqdm 显示进度条
    for file_path in tqdm(html_files, desc="Scanning HTML files"):
        content = None
        for encoding in encodings:
            try:
                with open(file_path, "r", encoding=encoding) as f:
                    content = f.read()
                break  # 成功读取文件后跳出循环
            except Exception as e:
                # print(
                #     f"Error processing file {file_path} with encoding {encoding}: {e}"
                # )
                print(e)

        if content is None:
            print(f"Failed to process file {file_path} with all encodings.")
            continue

        if not pattern.search(content):
            files_without_template_count += 1
            files_without_template.append(file_path)
            print(f"File without: {file_path}")

    # 输出结果
    print(f"Total HTML files scanned: {len(html_files)}")
    print(f"Files without 'template/favicon.php': {files_without_template_count}")

    if files_without_template:
        with open("scan_log.txt", "w", encoding="utf-8") as log_file:
            log_file.write("Files without 'template/favicon.php':\n")
            for file_path in files_without_template:
                log_file.write(f"{file_path}\n")


# 使用示例，指定需要扫描的目录路径
directory = r"E:\WorkSpace\WebKaisyu\ssl-htdocs-local"
all_files = get_all_files(directory)
html_files = filter_html_files(all_files)
scan_html_files(html_files)
