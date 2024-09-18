# 更新当前文件夹下的所有log.py文件
import datetime
import os
import shutil
from .log import get_logger

logger = get_logger(__name__)

def update_log_files(directory):
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file == 'log.py':
                file_path = os.path.join(root, file)
                try:
                    # 备份原文件
                    backup_path = file_path + '.bak'
                    shutil.copy2(file_path, backup_path)
                    logger.info(f"Backed up {file_path} to {backup_path}")

                    # 更新文件内容
                    with open(file_path, 'w', encoding='utf-8') as f:
                        f.write(generate_log_content())
                    logger.info(f"Updated {file_path}")
                except Exception as e:
                    logger.error(f"Error updating {file_path}: {str(e)}")

def generate_log_content(author_name="luckykefu", email= "3124568493@qq.com"):
    return f"""# log.py
# --coding:utf-8--
# Time:{datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
# Author:{author_name}
# Email:{email}
# Description: Provides colored logging functionality with enhanced features

import logging
from colorama import Fore, Style, init
from functools import lru_cache

# Initialize colorama
init(autoreset=True)

# Define colors for different levels
LEVEL_COLORS = {{
    logging.DEBUG: Fore.CYAN,
    logging.INFO: Fore.GREEN,
    logging.WARNING: Fore.YELLOW,
    logging.ERROR: Fore.RED,
    logging.CRITICAL: Fore.MAGENTA + Style.BRIGHT,
    }}


class ColoredFormatter(logging.Formatter):
    def format(self, record):
        color = LEVEL_COLORS.get(record.levelno, Style.RESET_ALL)
        message = super().format(record)
        return f"{{color}}{{message}}{{Style.RESET_ALL}}"


@lru_cache(maxsize=None)
def get_logger(name, log_file=None):
    logger = logging.getLogger(name)
    if not logger.handlers:
        logger.setLevel(logging.DEBUG)
        formatter = ColoredFormatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(pathname)s:%(lineno)d - %(message)s"
        )

        # Console handler
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.DEBUG)
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)

        # File handler (if log_file is provided)
        if log_file:
            file_handler = logging.FileHandler(log_file, encoding="utf-8")
            file_handler.setLevel(logging.DEBUG)
            file_handler.setFormatter(
                logging.Formatter(
                    "%(asctime)s - %(levelname)s - %(pathname)s:%(lineno)d - %(message)s"
                )
            )
            logger.addHandler(file_handler)

    return logger


if __name__ == "__main__":
    logger = get_logger(__file__)
    logger.debug("This is a debug message.")
    logger.info("This is an info message.")
    logger.warning("This is a warning message.")
    logger.error("This is an error message.")
    logger.critical("This is a critical message.")
    
"""

if __name__ == "__main__":
    current_directory = os.getcwd()
    update_log_files(current_directory)
    logger.info("Log file update process completed.")
