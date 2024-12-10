import pyautogui
import time
import os, sys
import logging
from logging.handlers import TimedRotatingFileHandler

os.system("chcp 65001")


pyautogui.FAILSAFE = True
pyautogui.PAUSE = 0.3
TIME_OUT = 10
CONFIFDENCE = 0.8
image_base_path = r"E:\CodeAchieve\MyFluent\itTools-fastapi\resource\image"
SLEEP = 2
SLEEP_MOER = 3

X = 2560
Y = 1600
right_up = (X / 2, 0, X, Y / 2)
right_down = (X / 2, Y / 2, X, Y)
left_up = (0, 0, X / 2, Y / 2)
left_down = (0, Y / 2, X / 2, Y)


def setup_logger(logger_name="miChecker"):
    """
    设置全局日志记录器，包括控制台和文件处理器。

    参数:
    logger_name (str): 日志记录器的名称，默认为"miChecker"
    返回:
    logging.Logger: 配置好的日志记录器
    """
    logger = logging.getLogger(logger_name)

    if not logger.hasHandlers():
        logger.setLevel(logging.INFO)
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(logging.INFO)

        console_formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )
        console_handler.setFormatter(console_formatter)
        logger.addHandler(console_handler)

        # Global file handler for persistent logs
        file_handler = TimedRotatingFileHandler(
            f"{logger_name}.log",
            when="midnight",
            interval=1,
            backupCount=7,
            encoding="utf-8",
        )
        file_handler.setLevel(logging.INFO)
        file_formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )
        file_handler.setFormatter(file_formatter)
        logger.addHandler(file_handler)
    return logger


def wait_for_image(image_name, timeout=TIME_OUT, confidence=CONFIFDENCE, region=None):
    """
    等待特定图标出现
    :param image_name: 图标的路径
    :param timeout: 超时时间（秒）
    :param confidence: 匹配精度 (0.1 ~ 1.0)
    :param region: 搜索区域 (x, y, width, height)
    :return: 图标的坐标位置，未找到返回 None
    """
    start_time = time.time()
    image_path = os.path.join(image_base_path, image_name)

    while True:
        try:
            time.sleep(0.5)
            location = pyautogui.locateOnScreen(
                image_path, confidence=confidence, region=region
            )
            if location:
                logger.info(f"location: {location}")
                return location
            elif time.time() - start_time > timeout:
                logger.info(f"超时未找到{image_name}图标")
                return None
        except pyautogui.ImageNotFoundException:
            # 捕获异常并忽略，继续循环
            logger.info(f"未找到{image_name}图标，继续寻找")
            if time.time() - start_time > timeout:
                logger.info(f"超时未找到{image_name}图标")
                return None
            continue
            # 增加超时检查
        except Exception as e:
            logger.info(f"加载超时，未找到{image_name}图标")


def click_icon(image_path, timeout=TIME_OUT, confidence=CONFIFDENCE, region=None):
    location = wait_for_image(
        image_path, timeout=timeout, confidence=CONFIFDENCE, region=region
    )
    if location:
        pyautogui.click(location)
        logger.info(f"已点击{image_path}按钮")
    else:
        logger.info(f"未找到{image_path}按钮")
        return


def perform_task_for_link(link):
    """
    对单个网页链接执行指定操作
    :param link: 网页链接
    """
    # 等待软件启动完成
    logger.info("等待软件启动...")
    wait_for_image(
        "michecker.png",
        region=(0, 0, 200, 200),
    )
    logger.info("软件启动完成...")

    time.sleep(SLEEP)

    # 输入链接
    pyautogui.click(x=400, y=175)  # 确认坐标正确
    time.sleep(1)  # 增加延迟，确保输入框被选中
    pyautogui.typewrite(link)

    pyautogui.press("enter")
    pyautogui.press("enter")
    logger.info(f"已输入链接：{link}")

    # 防止弹出iframe
    click_icon("ok.png", timeout=2, region=(500, 400, 2560, 1500))

    time.sleep(SLEEP)
    # 点击視覚化按钮
    click_icon("visual.png", region=(2000, 0, 2560, 300))
    time.sleep(SLEEP)

    # 会計検査院 Board of Audit of Japan
    wait_for_image(
        "search.png",
        timeout=TIME_OUT / 2,
        confidence=0.5,
        # region=(X / 2, 0, X, Y / 2),  # 最右边一小块
    )

    # 等待并点击“保存”按钮
    click_icon("save.png", region=(2000, 0, 2560, 300))

    time.sleep(SLEEP)

    # 等待并点击“保存”按钮
    click_icon("report_flie_save.png", region=(0, 0, 1200, 1000))

    logger.info(f"任务完成：{link}")


def main():
    """
    主程序，循环处理网页链接
    """
    logger.info("\n\n\n开始执行任务...")

    # 定义网页链接列表
    links = read_txt()

    index = 42

    for link in links[index:]:
        index += 1
        logger.info(f"index: {index}")
        logger.info(f"开始处理链接：{link}")
        perform_task_for_link(link)
        time.sleep(2)  # 等待2秒避免过快操作


def read_txt():
    # 定义文件路径
    file_path = r"E:\CodeAchieve\MyFluent\itTools-fastapi\resource\link.txt"

    # 读取文件并转换为拼接后的列表
    with open(file_path, "r", encoding="utf-8") as file:
        # links = ["http://ip" + line for line in file.read().splitlines()]
        links = [line for line in file.read().splitlines()]

    # 打印结果
    logger.info(links)

    return links


logger = setup_logger()

if __name__ == "__main__":
    main()
    # read_txt()
    # E:/Environment/anaconda3/envs/fast/python.exe e:/CodeAchieve/MyFluent/itTools-fastapi/server/scripts/auto_michecker.py
