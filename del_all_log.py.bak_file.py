import os
from src.log import get_logger

logger = get_logger(__name__)

def delete_log_bak_files(directory):
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('log.py.bak'):
                file_path = os.path.join(root, file)
                try:
                    os.remove(file_path)
                    logger.info(f"Deleted backup file: {file_path}")
                except Exception as e:
                    logger.error(f"Error deleting {file_path}: {str(e)}")

if __name__ == "__main__":
    current_directory = os.getcwd()
    delete_log_bak_files(current_directory)
    logger.info("Deletion of log.py.bak files completed.")
