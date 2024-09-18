# Update all git submodules
import subprocess
from src.log import get_logger

logger = get_logger(__name__)

def update_git_submodules():
    try:
        # Initialize submodules
        subprocess.run(["git", "submodule", "init"], check=True)
        logger.info("Git submodules initialized.")

        # Update submodules
        subprocess.run(["git", "submodule", "update", "--recursive", "--remote"], check=True)
        logger.info("Git submodules updated successfully.")
    except subprocess.CalledProcessError as e:
        logger.error(f"Error updating git submodules: {str(e)}")

if __name__ == "__main__":
    update_git_submodules()