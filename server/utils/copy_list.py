# 批量复制文件列表，包括文件夹结构
import os
import shutil
import tqdm

origin_path = r"Z:\ssl-htdocs"
copy_path = r"E:\WorkSpace\WebKaisyu\html_1016_1"

# String of file paths (could be from a file or input)
file_list = r"""
recruit/msg01.html
recruit/way.html
recruit/carrerPath.html
recruit/training.html
recruit/other.html
common\template\footer.php
common2/tmp/footer.php
"""

# Function to normalize paths
def normalize_paths(raw_paths):
    normalized_paths = []
    
    # Split the raw string by lines and process each line
    for path in raw_paths.strip().splitlines():
        # Strip whitespace, replace backslashes with forward slashes, and ensure it starts with a forward slash
        path = path.strip().replace("\\", "/")
        if not path.startswith("/"):
            path = "/" + path
        normalized_paths.append(path)
    
    return normalized_paths

# Function to copy files and recreate folder structure
def copy_files_with_structure(origin_path, copy_path, file_list):
    
    file_list = normalize_paths(file_list)
    
    print(f'copy folder from {origin_path} to {copy_path}')
    
    os.makedirs(os.path.dirname(copy_path), exist_ok=True)
    
    for file in tqdm.tqdm(file_list):
        # Remove leading '/' to avoid issues with os.path.join
        file = file.lstrip('/')
        
        # Get full path of the source file
        source = os.path.join(origin_path, file)
        
        # Check if the source is a file and exists
        if os.path.isfile(source):
            # Create the target file path
            target = os.path.join(copy_path, file)
            
            # Create directories in the target path if they don't exist
            os.makedirs(os.path.dirname(target), exist_ok=True)
            
            # Copy the file to the target location
            shutil.copy2(source, target)
            print(f"\nCopied: {source} -> {target}")
        else:
            print(f"\nSkipped: {source} (Not a file)")


if __name__ == "__main__":
    # Run the function to copy files
    copy_files_with_structure(origin_path, copy_path, file_list)
