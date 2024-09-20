# clear_cache.py

import os
import shutil
from .log import get_logger

logger = get_logger(__name__)


def delete_path(path):
    """
    Delete the given file or directory.
    """
    logger.info(f"Deleting path: {path}")
    path = os.path.join(os.getcwd(), path)
    if os.path.exists(path):
        try:
            if os.path.isdir(path):
                shutil.rmtree(path)
                logger.info(f"Successfully deleted directory: {path}")
            elif os.path.isfile(path):
                os.remove(path)
                logger.info(f"Successfully deleted file: {path}")
            else:
                logger.warning(f"Path is neither a file nor a directory: {path}")
        except PermissionError:
            logger.error(f"Permission denied when trying to delete {path}")
        except OSError as e:
            logger.error(f"Error deleting {path}: {str(e)}")
    else:
        logger.warning(f"Path does not exist: {path}")

def delete_path_in_dir(dir,path):
    """
    delete all dirs in given under dir
    """
    if not os.path.exists(dir):
        logger.warning(f"Directory does not exist: {dir}")
        return
    if isinstance(path, str):
        path_list = [path]
    elif isinstance(path, list):
        path_list = path
    else:
        logger.error("path must be a string or a list")
        return
    logger.info(f"Deleting path in dir: {dir}")
    for path in path_list:
        for root, dirs, files in os.walk(dir):
            for directory in dirs:
                if directory == path:
                    delete_path(os.path.join(root, dir))
    logger.info("Delete path in dir completed")