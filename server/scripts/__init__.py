from server.utils.app_logger import *

def logger_init():
    script_name = os.path.basename(__file__).split('.')[0]
    logger = setup_stream_logger(script_name)
    print(f'====== logger_init: {script_name} ======')
    return logger