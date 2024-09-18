# clear_cache.py

import os
import shutil
from .log import get_logger

logger = get_logger(__name__)


def delete_path(path):
    """
    Delete the given file or directory.
    """
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
        except Exception as e:
            logger.error(f"Error deleting {path}: {str(e)}")
    else:
        logger.warning(f"Path does not exist: {path}")
