import subprocess
from src.log import get_logger

# 创建日志对象
logger = get_logger(__name__)


def generate_requirements_file(directory, filename="requirements.txt"):
    """
    Generate requirements.txt file using pipreqs.

    :param directory: Directory to scan for dependencies.
    :param filename: Name of the output requirements file.
    """
    try:
        # 构造命令
        command = ["pipreqs", directory, f"--force"]

        # 运行命令
        result = subprocess.run(
            command, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE
        )

        # 记录输出
        logger.info(f"Requirements file generated successfully: {filename}")
    except subprocess.CalledProcessError as e:
        # 处理错误
        logger.error(f"Failed to generate requirements file: {e.stderr.decode()}")
    except Exception as e:
        # 处理其他异常
        logger.error(f"An unexpected error occurred: {str(e)}")


if __name__ == "__main__":

    from src.list_subdir import list_subdir

    dirs = list_subdir()
    for dir in dirs:
        # 生成 requirements.txt 文件
        generate_requirements_file(dir)
