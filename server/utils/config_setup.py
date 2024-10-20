import os
import sys
import logging
import yaml
import sqlite3
import json

# from backup import sqliteManager

logger = logging.getLogger("GlobalLogger")


class ConfigManager:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(ConfigManager, cls).__new__(cls, *args, **kwargs)
            cls._instance._initialize(*args, **kwargs)
        return cls._instance

    def _initialize(self, cfg_file="cfg.yaml", db_file="rule.db"):
        # self.ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
        RESOURCE = "resource"
        if getattr(sys, "frozen", False):

            self.ROOT_DIR = os.path.dirname(sys.executable)
            print("exe模型！:" + self.ROOT_DIR)
        else:

            self.ROOT_DIR = os.path.abspath(
                os.path.join(os.path.dirname(__file__), "..")
            )
            print("py模式" + self.ROOT_DIR)
        self.ROOT_DIR = os.path.realpath(self.ROOT_DIR)
        print("当前real路径：" + self.ROOT_DIR)
        self.CONFIG_DIR = os.path.dirname(os.path.abspath(__file__))

        self.CONFIG_FILE_PATH = os.path.join(self.ROOT_DIR, "resource", cfg_file)
        self.SQLITE_DB_PATH = os.path.join(self.ROOT_DIR, "resource", db_file)

        self._load_config()
        self._load_database()

    def _load_config(self):
        with open(self.CONFIG_FILE_PATH, "r", encoding="utf-8") as file:
            self.config_data = yaml.load(file, Loader=yaml.SafeLoader)

    def _load_database(self):
        self.db_conn = sqlite3.connect(self.SQLITE_DB_PATH)
        self.db_cursor = self.db_conn.cursor()
        self.start_values = self._fetch_all("start_values")
        self.cyclic_values = self._fetch_all("cyclic_values")

    def _fetch_all(self, table_name):
        self.db_cursor.execute(f"SELECT * FROM {table_name}")
        return self.db_cursor.fetchall()

    def get_config_value(self, key):
        return self.config_data.get(key)

    def query_db(self, query, params=()):
        self.db_cursor.execute(query, params)
        return self.db_cursor.fetchall()

    def load_start_cyclic_values(self):
        start_values = {item[0]: item[1] for item in self.start_values}
        cyclic_values = {
            item[0]: eval(item[1]) for item in self.cyclic_values
        }  # Convert string to list
        return start_values, cyclic_values

    def update_yaml(self, field, new_value):
        if field in self.config_data:
            self.config_data[field] = new_value
        else:
            print(f"字段 '{field}' 不存在于 YAML 文件中。")
            return

        with open(self.CONFIG_FILE_PATH, "w", encoding="utf-8") as file:
            yaml.dump(
                self.config_data,
                file,
                default_flow_style=False,
                allow_unicode=True,
                sort_keys=False,
            )
        logger.info(f"字段 '{field}' 已更新为 '{new_value}'")
        self._load_config()

    def save_config(self):
        with open(self.CONFIG_FILE_PATH, "w", encoding="utf-8") as file:
            yaml.dump(
                self.config_data,
                file,
                allow_unicode=True,
                sort_keys=False,
                default_flow_style=False,
            )
        self._load_config()

    def load_json_config(self):
        json_str = json.dumps(self.config_data, separators=(",", ":"))
        return self.format_json(json_str)

    def format_json(self, json_str):
        formatted_str = ""
        in_string = False
        indent_level = 0
        last_char = ""

        for char in json_str:
            if char == '"':
                in_string = not in_string

            if char in "{[" and not in_string:
                formatted_str += char + "\n" + " " * (indent_level + 1)
                indent_level += 1
            elif char in "}]" and not in_string:
                indent_level -= 1
                formatted_str += "\n" + " " * indent_level + char
            elif char == "," and not in_string:
                formatted_str += char + "\n" + " " * indent_level
            elif char == " " and last_char in "[]" and not in_string:
                continue
            else:
                formatted_str += char

            last_char = char

        return formatted_str

    def __del__(self):
        if hasattr(self, "db_conn"):
            self.db_conn.close()
