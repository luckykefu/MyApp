import os
from .log import get_logger

logger = get_logger(__file__)

def gen_reqs(dir):
    logger.info("Generating requirements.txt")

    if isinstance(dir, str):
        dirs = dir.split("\n")
    for path in dirs:
        try:
            if not os.path.exists(path):
                logger.error(f"Directory {path} does not exist")
                continue
            os.system(f"pipreqs --force {path}")
            logger.info(f"requirements.txt generated successfully in {path}")
        except Exception as e:
            logger.error(f"Failed to generate requirements.txt: {e}")

if __name__ == "__main__":
    gen_reqs(os.getcwd())