import os
import shutil
import logging
from datetime import datetime
from server.utils.printer_wrapper import format_and_print_params
from tqdm.asyncio import tqdm as async_tqdm
import asyncio

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


# 通用文件复制逻辑
async def copy_files(
    origin_path,
    copy_path,
    exclude_exts,
    exclude_dirs,
    include_dirs,
    all_copy,
    filter_func,
):
    """
    遍历原始路径中的文件，为每个文件进行复制。
    依赖 filter_func 来决定哪些文件夹应该被包含或排除。

    参数:
    origin_path: str，原始文件夹路径。
    copy_path: str，目标文件夹路径。
    exclude_exts: list，文件扩展名列表，复制时将被排除的。
    exclude_dirs: list，文件夹名称列表，复制时将被排除的。
    include_dirs: list，文件夹名称列表，复制时只包含这些文件夹的内容。
    all_copy: bool，是否强制复制所有文件（即使它们已经存在）。
    filter_func: function，用于过滤文件夹的自定义函数。
    """
    logger = logging.getLogger(__name__)
    # 使用 async_tqdm 代替 tqdm
    traversal_pbar = async_tqdm(desc="Traversing Files", unit="files", position=0)
    processing_pbar = async_tqdm(desc="Processing Files", unit="files", position=1)

    for root, dirs, files in os.walk(origin_path):
        # 过滤文件夹，使用 await 调用异步函数
        dirs[:] = await filter_func(dirs, exclude_dirs, include_dirs)

        # 构建目标路径
        relative_path = os.path.relpath(root, origin_path)
        target_dir = os.path.join(copy_path, relative_path)

        # 创建目标目录
        if not os.path.exists(target_dir):
            os.makedirs(target_dir)

        # 复制文件，排除指定扩展名的文件
        for file in files:
            traversal_pbar.update(1)  # 每处理一个文件更新一次进度条
            if not any(file.lower().endswith(ext) for ext in exclude_exts):
                source_file = os.path.join(root, file)
                target_file = os.path.join(target_dir, file)

                if await should_copy(source_file, target_file) or all_copy:
                    # all_copy=True 直接执行更新
                    shutil.copy2(source_file, target_file)

                    processing_pbar.update(1)
                    logger.info(f"Copied: {source_file} to {target_file}")  # 记录日志

        await asyncio.sleep(0.01)

        # 获取最终结果并输出
        traversed_files = traversal_pbar.format_dict["n"]
        processed_files = processing_pbar.format_dict["n"]
        logger.info(
            f"{dirs}: Total files processed: {traversed_files}, Files copied: {processed_files}"
        )


# 复制所有文件，排除指定的目录
async def copy_folders_with_exclusion(
    origin_path,
    copy_path,
    exclude_exts,
    exclude_dirs,
    all_copy,
):
    """
    复制原始路径中的文件，排除指定的目录和扩展名。

    参数:
    origin_path: str，原始文件夹路径。
    copy_path: str，目标文件夹路径。
    exclude_exts: list，文件扩展名列表，复制时将被排除的。
    exclude_dirs: list，文件夹名称列表，复制时将被排除的。
    all_copy: bool，是否强制复制所有文件（即使它们已经存在）。
    """

    async def filter_func(dirs, exclude_dirs, include_dirs):
        # 过滤掉要排除的目录
        return [d for d in dirs if d not in exclude_dirs]

    await copy_files(
        origin_path, copy_path, exclude_exts, exclude_dirs, None, all_copy, filter_func
    )


# 仅复制包含在 include_dirs 中的目录的文件
async def copy_folders_with_inclusion(
    origin_path,
    copy_path,
    exclude_exts,
    include_dirs,
    all_copy,
):
    """
    仅复制原始路径中包含的文件夹内的文件。

    参数:
    origin_path: str，原始文件夹路径。
    copy_path: str，目标文件夹路径。
    exclude_exts: list，文件扩展名列表，复制时将被排除的。
    include_dirs: list，文件夹名称列表，复制时只包含这些文件夹的内容。
    all_copy: bool，是否强制复制所有文件（即使它们已经存在）。
    """

    async def filter_func(dirs, exclude_dirs, include_dirs):
        # 仅保留 include_dirs 中的文件夹
        return [d for d in dirs if d in include_dirs]

    await copy_files(
        origin_path, copy_path, exclude_exts, None, include_dirs, all_copy, filter_func
    )


async def should_copy(source_file, target_file):
    """
    判断是否需要复制源文件到目标文件。

    参数:
    source_file: str，源文件的完整路径。
    target_file: str，目标文件的完整路径。

    返回:
    bool，若应复制则返回 True，否返回 False。
    """

    # 如果目标文件不存在，直接复制
    if not os.path.exists(target_file):
        return True

    # 获取文件的修改时间
    source_mtime = os.path.getmtime(source_file)
    target_mtime = os.path.getmtime(target_file)

    # 如果源文件的修改时间比目标文件新，则复制
    return source_mtime > target_mtime


@format_and_print_params
async def copy_folders(
    origin_path,  # 原始文件路径
    copy_path,  # 目标复制路径
    exclude_exts,  # 要排除的文件扩展名列表
    exclude_dirs,  # 要排除的目录列表
    include_dirs,  # 要包含的目录列表
    all_copy,  # 是否强制复制所有文件
):
    """
    处理复制过程，设置日志管理和调用具体的复制函数。

    参数:
    origin_path: str，原始文件夹路径。
    copy_path: str，目标文件夹路径。
    exclude_exts: list，文件扩展名列表，复制时将被排除的。
    exclude_dirs: list，文件夹名称列表，复制时将被排除的。
    include_dirs: list，文件夹名称列表，复制时仅包含这些文件夹。
    all_copy: bool，是否强制复制所有文件（即使它们已经存在）。
    """

    try:
        logger = logging.getLogger(__name__)
        # 设置日志输出到文件和控制台，并实时刷新日志文件
        current_time = datetime.now().strftime("%Y%m%d_%H%M%S")  # 获取当前日期时间
        log_file_path = (
            f"{copy_path}/copy_folder_{current_time}.log"  # 更新日志文件路径
        )
        fileHandler = logging.FileHandler(log_file_path, mode="a", encoding="utf-8")
        logger.addHandler(fileHandler)

        # 启动异步任务定期更新日志文件
        async def update_log_file():
            while True:
                await asyncio.sleep(10)  # 每10秒更新一次
                current_time = datetime.now().strftime("%Y%m%d_%H%M%S")
                log_file_path = f"{copy_path}/copy_folder_{current_time}.log"
                fileHandler = logging.FileHandler(
                    log_file_path, mode="a", encoding="utf-8"
                )
                logger.addHandler(fileHandler)
                logger.info("日志文件已更新")

        asyncio.create_task(update_log_file())  # 创建异步任务

        if exclude_dirs:  # exclude_dirs 是空列表，也会进入 else 分支
            # 使用排除目录方式
            logger.info("使用排除目录方式复制文件")
            await copy_folders_with_exclusion(
                origin_path, copy_path, exclude_exts, exclude_dirs, all_copy
            )
        elif include_dirs:
            # 使用包含目录方式
            logger.info("使用包含目录方式复制文件")
            await copy_folders_with_inclusion(
                origin_path, copy_path, exclude_exts, include_dirs, all_copy
            )
        else:
            logger.error("没有指定目录过滤方式！")
    except:
        logger.error("参数错误！")
    finally:
        logger.removeHandler(fileHandler)


async def run(script_name, params):
    """
    脚本入口函数
    参数通过关键字参数传入

    参数:
    script_name: str，脚本名称。
    params: dict，包含所有要传递给 copy_folders 函数的参数。

    返回:
    bool，执行成功返回 True，失败返回错误信息字符串。
    """

    try:
        # 处理参数，将字符串转换为列表
        if isinstance(params.get("exclude_exts"), str):
            params["exclude_exts"] = params["exclude_exts"].split(",")
        if isinstance(params.get("exclude_dirs"), str):
            params["exclude_dirs"] = params["exclude_dirs"].split(",")
        if isinstance(params.get("include_dirs"), str):
            params["include_dirs"] = params["include_dirs"].split(",")

        # 设置全局变量 logger
        global logger
        logger = logging.getLogger(script_name)
        await copy_folders(**params)
        return True
    except Exception as e:
        return str(e)
