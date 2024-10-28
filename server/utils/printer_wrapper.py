import functools
from tabulate import tabulate

def format_and_print_params(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        # 准备表格数据
        table_data = []
        
        # 添加位置参数到表格
        if args:
            for i, arg in enumerate(args):
                table_data.append([f"参数 {i}", arg])
        
        # 添加关键字参数到表格
        if kwargs:
            for key, value in kwargs.items():
                table_data.append([key, value])
        
        # 打印表格
        print(tabulate(table_data, headers=["参数名", "值"], tablefmt="grid"))
        
        # 调用原始函数
        result = func(*args, **kwargs)
        
        return result
    
    return wrapper

# # 示例使用
# @format_and_print_params
# def example_function(a, b, c=1, d=2):
#     return a + b + c + d

# # 调用示例函数
# example_function(10, 20, d=30)