# 列出当前dir all files and dirs
import os
from src.log import get_logger

logger = get_logger(__name__)


def list_subdir(
    exclude_dirs=[
        "src",
        "venv",
    ]
):
    # 获取当前目录下所有文件和目录
    dirs = []
    subdirs = os.listdir()
    for subdir in subdirs:
        if os.path.isdir(subdir):
            # 排除 目录
            if subdir in exclude_dirs:
                continue
            # 排除.开头的目录
            if subdir.startswith("."):
                continue
            # 排除__开头的目录
            if subdir.startswith("_"):
                continue

            logger.info(subdir)
            dirs.append(subdir)
    return dirs


if __name__ == "__main__":
    list_subdir()
