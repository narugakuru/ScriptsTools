import os
import csv
import logging

# from utils.backup import backup_file_or_folder
from server.utils.config_setup import ConfigManager

# 设置日志配置
logger = logging.getLogger("GlobalLogger")


class CSVProcessor:
    def __init__(self, add_value=int(0)):
        config = ConfigManager()
        self.start_values, self.cyclic_values = config.load_start_cyclic_values()
        self.add = config.config_data["add"]

    def generate_data(self, row_index, column_name):
        if column_name in self.start_values:
            return str(int(self.start_values[column_name]) + row_index + self.add)
        elif column_name in self.cyclic_values:
            return str(
                self.cyclic_values[column_name][
                    row_index % len(self.cyclic_values[column_name])
                ]
            )
        else:
            raise KeyError(
                f"Column name {column_name} not in start values or cyclic values"
            )

    def clean_data(self, data):
        """去除空格"""
        cleaned_data = []
        for row in data:
            cleaned_row = [elem.strip() if elem.strip() else " " for elem in row]
            cleaned_data.append(cleaned_row)
        return cleaned_data

    def process_csv_file(self, input_file, output_file):
        logger.info(f"开始处理文件: {input_file}")

        try:
            with open(input_file, "r", encoding="utf-8") as infile:
                reader = csv.reader(infile)
                headers = next(reader, None)
                if headers is None:
                    logger.warning(f"文件 {input_file} 是空的，无法处理。")
                    return

                data_rows = [row for row in reader]
                if not data_rows:
                    logger.warning(f"文件 {input_file} 没有数据行，无法处理。")
                    return

        except FileNotFoundError:
            logger.error(f"文件 {input_file} 不存在。")
            return
        except PermissionError:
            logger.error(f"没有权限访问文件 {input_file}。")
            return
        except Exception as e:
            logger.error(f"处理文件 {input_file} 时发生错误: {e}")
            return

        data_rows = self.clean_data(data_rows)
        new_data = self.replace(headers, data_rows)

        try:
            os.makedirs(os.path.dirname(output_file), exist_ok=True)
            with open(output_file, "w", newline="", encoding="utf-8") as outfile:
                writer = csv.writer(outfile, quoting=csv.QUOTE_ALL)
                writer.writerow(headers)
                writer.writerows(new_data)
            logger.info(f"文件 {input_file} 处理完毕，保存到 {output_file}")
        except PermissionError:
            logger.error(f"没有权限写入文件 {output_file}。")
        except Exception as e:
            logger.error(f"保存文件 {output_file} 时发生错误: {e}")

    def replace(self, headers, data_rows):
        replacements_count = 0
        new_data_rows = []
        for i, row in enumerate(data_rows):
            new_row = []
            for j, field in enumerate(headers):
                if j < len(row):
                    if field in self.start_values or field in self.cyclic_values:
                        try:
                            new_value = self.generate_data(i, field)
                            if new_value != row[j]:
                                replacements_count += 1
                            new_row.append(new_value)
                        except KeyError:
                            new_row.append(row[j])
                    else:
                        new_row.append(row[j])
                else:
                    if field in self.start_values or field in self.cyclic_values:
                        try:
                            new_value = self.generate_data(i, field)
                            new_row.append(new_value)
                            replacements_count += 1
                        except KeyError:
                            new_row.append("")
                    else:
                        new_row.append("")
            new_data_rows.append(new_row)

        logger.info(f"数据处理完成，替换了 {replacements_count} 条数据")
        return new_data_rows

    def process_data(self, data):
        """
        处理返回一个完整的包含csv数据的list数组
        """
        headers = data[0]
        data_rows = data[1:]

        # 处理数据行
        data_rows = self.clean_data(data_rows)
        new_data_rows = self.replace(headers, data_rows)
        # 返回处理过的data
        return [headers] + new_data_rows

    def process_csv_folder(self, input_directory, output_directory):
        try:
            for file in os.listdir(input_directory):
                if file.endswith(".csv"):
                    input_file = os.path.join(input_directory, file)
                    output_file = os.path.join(output_directory, file)
                    self.process_csv_file(input_file, output_file)
        except FileNotFoundError:
            logger.error(f"目录 {input_directory} 不存在。")
        except PermissionError:
            logger.error(f"没有权限访问目录 {input_directory}。")
        except Exception as e:
            logger.error(f"处理目录 {input_directory} 时发生错误: {e}")

    def process_csv(self, input, output=None):
        # 备份原始文件
        # backup_file_or_folder(input)
        if output is None:
            # 默认在输入路径下新建replace文件夹
            output = get_folder_path(input)
            output = os.path.join(output, "replace")

        if os.path.isdir(input):
            # output是一个文件夹
            self.process_csv_folder(input, output)
        elif os.path.isfile(input):
            # output是一个文件
            output_name = os.path.basename(input)
            output = os.path.join(output, output_name)
            self.process_csv_file(input, output)
        else:
            raise ValueError("输入路径必须是一个文件或文件夹")

        return output


def get_folder_path(path):
    # 如果路径以.csv结尾，则返回其文件夹路径
    if path.endswith(".csv"):
        return os.path.dirname(path)
    # 否则，假设路径是文件夹路径，直接返回
    return path


# 示例使用
if __name__ == "__main__":
    # rule_file_path = r"D:\WorkSpace\app\id.txt"
    input_directory = r"D:\WorkSpace\NADJ20007"
    output_directory = input_directory

    processor = CSVProcessor()
    processor.process_csv(input_directory)
