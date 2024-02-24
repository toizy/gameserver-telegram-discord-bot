"""
    Модуль логирования в файл, названный по дате и времени
"""

import logging
import os
from datetime import datetime


class Logger:
    _instance = None
    log_file = None
    last_date = None

    def __new__(cls):
        if not cls._instance:
            cls._instance = super(Logger, cls).__new__(cls)
            cls._instance.logger = cls.setup_logger()
        return cls._instance

    @staticmethod
    def setup_logger():
        logger = logging.getLogger("my_logger")
        logger.setLevel(logging.DEBUG)

        cls = Logger
        cls.update_log_file()

        file_handler = logging.FileHandler(cls.log_file)
        file_handler.setLevel(logging.DEBUG)

        formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
        file_handler.setFormatter(formatter)

        logger.addHandler(file_handler)

        return logger

    @classmethod
    def update_log_file(cls):
        current_date = datetime.now()
        current_month_year = current_date.strftime('%m-%Y')

        if cls.last_date != current_month_year:
            log_directory = os.path.join(os.path.dirname(os.path.abspath(__file__)), "logs")
            cls.last_date = current_month_year
            log_subdirectory = os.path.join(log_directory, current_month_year)

            # Создаем каталог и поддиректорию, если их нет
            os.makedirs(log_directory, exist_ok=True)
            os.makedirs(log_subdirectory, exist_ok=True)

            cls.log_file = os.path.join(log_subdirectory, f"{current_date.strftime('%Y-%m-%d')}.log")

    def debug(self, message, print_to_console=True):
        if print_to_console:
            print(message)
        self.update_log_file()
        self.logger.debug(message)

    def info(self, message, print_to_console=True):
        if print_to_console:
            print(message)
        self.update_log_file()
        self.logger.info(message)

    def warning(self, message, print_to_console=True):
        if print_to_console:
            print(message)
        self.update_log_file()
        self.logger.warning(message)

    def error(self, message, print_to_console=True):
        if print_to_console:
            print(message)
        self.update_log_file()
        self.logger.error(message)

    def exception(self, message, print_to_console=True):
        if print_to_console:
            print(message)
        self.update_log_file()
        self.logger.exception(message)

    def critical(self, message, print_to_console=True):
        if print_to_console:
            print(message)
        self.update_log_file()
        self.logger.critical(message)

    def timestamp(self):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.update_log_file()
        self.logger.info(f"Timestamp: {timestamp}")


# Создаем синглтон
log = Logger()
