import os
import csv
import re
import logging
from datetime import datetime
from peewee import PostgresqlDatabase
from utils.all_rule_replace import (
    CSVProcessor,
)  # Ensure this module is available in your environment
from utils.config_setup import (
    ConfigManager,
)  # Ensure this module is available in your environment

# Set up logging configuration
logger = logging.getLogger("GlobalLogger")
logging.basicConfig(level=logging.INFO)


class CSVtoPostgresInserter:
    def __init__(self, id_replace=True):
        self.csv_folder = None
        self.id_replace = id_replace
        self.db = None
        self.connect()
        logger.info("CSVtoPostgresInserter initialized successfully.")

    def connect(self):
        # Define database connection parameters
        db_url = "postgresql+psycopg2://postgres:rootroot@localhost:5432/postgres?options=-csearch_path=takusai_tanntai"

        # Parse database URL
        pattern = re.compile(
            r"postgresql\+psycopg2://(?P<user>[^:]+):(?P<password>[^@]+)@(?P<host>[^:]+):(?P<port>\d+)/(?P<database>[^\?]+)\?options=-csearch_path=(?P<schema>[^\&]+)"
        )
        match = pattern.match(db_url)

        if match:
            self.db_config = match.groupdict()
        else:
            raise ValueError("Invalid database URL")
        try:
            # Create database instance
            self.db = PostgresqlDatabase(
                self.db_config["database"],
                user=self.db_config["user"],
                password=self.db_config["password"],
                host=self.db_config["host"],
                port=int(self.db_config["port"]),
                options=f"-c search_path={self.db_config['schema']}",
            )

            # Connect to the database
            self.db.connect()
            logger.info("Connected to the database.")
        except Exception as e:
            logger.error(f"Failed to connect to the database: {e}")
            raise

    def filter_latest_csv_files(self):
        latest_files = {}
        pattern = re.compile(r"^(.*?)(?:_(\d{8}\d{4}))?\.csv$")

        for filename in os.listdir(self.csv_folder):
            if filename.endswith(".csv"):
                match = pattern.match(filename)
                if match:
                    table_name = match.group(1)
                    date_str = match.group(2)
                    file_date = (
                        datetime.min
                        if not date_str
                        else datetime.strptime(date_str, "%Y%m%d%H%M")
                    )

                    if (
                        table_name not in latest_files
                        or latest_files[table_name][1] < file_date
                    ):
                        latest_files[table_name] = (filename, file_date)

        return [entry[0] for entry in latest_files.values()]

    def insert_csv_to_postgresql_with_transaction(self):
        try:
            csv_list = self.filter_latest_csv_files()
            for filename in csv_list:
                file_path = os.path.join(self.csv_folder, filename)
                with open(file_path, newline="", encoding="utf-8") as csvfile:
                    reader = csv.DictReader(csvfile)
                    columns = reader.fieldnames

                    table_name = re.match(
                        r"^(.*?)(?:_\d{8}\d{4})?\.csv$", filename
                    ).group(1)
                    schema_name = self.db_config["schema"]

                    with self.db.atomic():  # Use atomic transactions
                        try:
                            # Check if table exists
                            if table_name not in self.db.get_tables(schema=schema_name):
                                logger.info(
                                    f"Table {table_name} does not exist in the database. Skipping {filename}."
                                )
                                continue

                            # Clear the table
                            self.db.execute_sql(
                                f"DELETE FROM {schema_name}.{table_name}"
                            )

                            # Insert data
                            for row in reader:
                                values = ", ".join(
                                    [
                                        (
                                            f"'{row[col]}'"
                                            if row[col] is not None
                                            else "NULL"
                                        )
                                        for col in columns
                                    ]
                                )
                                insert_query = f"INSERT INTO {schema_name}.{table_name} ({', '.join(columns)}) VALUES ({values})"
                                self.db.execute_sql(insert_query)

                            logger.info(
                                f"Inserted data from {filename} into {table_name} table."
                            )
                        except Exception as e:
                            logger.error(
                                f"Failed to insert data from {filename} into {table_name} table."
                            )
                            logger.exception(e)
        except Exception as e:
            logger.error("Transaction failed and was rolled back.")
            logger.exception(e)

    def replace_csv_insert2db(self, csv_path):
        csvProcessor = CSVProcessor()
        self.csv_folder = csvProcessor.process_csv(csv_path)
        logger.info("CSV data processing completed, starting database connection")
        try:
            self.insert_csv_to_postgresql_with_transaction()
            logger.info("Data insertion completed")
            return True
        except Exception as e:
            logger.error(f"Data insertion failed: {e}")
            return False


def insert_data(csv_path):
    inserter = CSVtoPostgresInserter(True)
    inserter.replace_csv_insert2db(csv_path)


if __name__ == "__main__":
    csv_path = r"Z:\WorkSpace\NADJ20007"
    insert_data(csv_path)
