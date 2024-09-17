import datetime
import os
from src.log import get_logger
import shutil

logger = get_logger(__name__)


def create_dir(dir):
    """
    Create the src directory in the given project.
    """
    os.makedirs(dir, exist_ok=True)
    logger.info(f"Created Dir {dir} successfully")


def create_file(file_path, content):
    """
    Create a file with the given content in the given path.
    """
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content)
    logger.info(f"Created file {file_path} successfully")


def create_project(project_name=None, author_name=None, email=None):
    """
    Create a new project with the given name.
    """
    # Check if project already exists
    if os.path.exists(project_name):
        logger.error(f"Project {project_name} already exists")

        user_input = input("Do you want to continue? (y/n): ").strip().lower()

        if user_input != "y":
            logger.error("Operation cancelled by the user.")
            return  # 取消操作

        else:
            shutil.rmtree(project_name)
            logger.info(f"Deleted existing project {project_name}")

        logger.info("Continuing with the operation...")

    logger.info(f"Creating project {project_name}")

    #  Create project directory
    create_dir(project_name)

    # Create src directory
    src_dir = os.path.join(project_name, "src")
    create_dir(src_dir)

    # Create log.py file
    log_file = os.path.join(src_dir, "log.py")
    log_content = f"""# log.py
# --coding:utf-8--
# Time:{datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
# Author:{author_name}
# Email:{email}
# Description:

import logging
from colorama import Fore, Style, init

# Initialize colorama
init(autoreset=True)

# Define colors for different levels
LEVEL_COLORS = {{
    logging.DEBUG: Fore.BLUE,      # Debug messages in blue
    logging.INFO: Fore.GREEN,       # Info messages in green
    logging.WARNING: Fore.YELLOW,    # Warning messages in yellow
    logging.ERROR: Fore.RED,        # Error messages in red
    logging.CRITICAL: Fore.MAGENTA,  # Critical messages in magenta
}}

class ColoredFormatter(logging.Formatter):
    def format(self, record):
        # Get the color for the record
        color = LEVEL_COLORS.get(record.levelno, Style.RESET_ALL)
        # Set the log format
        message = super().format(record)
        return f"{{color}}{{message}}{{Style.RESET_ALL}}"

def get_logger(name):
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    # Use the custom ColoredFormatter
    formatter = ColoredFormatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.DEBUG)
    console_handler.setFormatter(formatter)

    # Clear duplicate handlers
    if logger.hasHandlers():
        logger.handlers.clear()

    logger.addHandler(console_handler)
    return logger

if __name__ == "__main__":
    logger = get_logger("MyLogger")

    logger.debug("This is a debug message.")
    logger.info("This is an info message.")
    logger.warning("This is a warning message.")
    logger.error("This is an error message.")
    logger.critical("This is a critical message.")

"""
    create_file(log_file, log_content)

    # Create src/__init__.py file
    init_file = os.path.join(src_dir, "__init__.py")
    create_file(init_file, "")

    # create .gitignore file
    gitignore_file = os.path.join(project_name, ".gitignore")
    gitignore_content = """/cookies/
/cache/
/models/
/.conda/
/temp/
/venv/
/env/
/build/
/dist/
/whisper_models/
/output/
/config/
/data/
/logs/

# Byte-compiled / optimized / DLL files
__pycache__/
*.py[cod]
*$py.class

# C extensions
*.so

# Distribution / packaging
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
share/python-wheels/
*.egg-info/
.installed.cfg
*.egg
MANIFEST

# PyInstaller
#  Usually these files are written by a python script from a template
#  before PyInstaller builds the exe, so as to inject date/other infos into it.
*.manifest
*.spec

# Installer logs
pip-log.txt
pip-delete-this-directory.txt

# Unit test / coverage reports
htmlcov/
.tox/
.nox/
.coverage
.coverage.*
.cache
nosetests.xml
coverage.xml
*.cover
*.py,cover
.hypothesis/
.pytest_cache/
cover/

# Translations
*.mo
*.pot

# Django stuff:
*.log
local_settings.py
db.sqlite3
db.sqlite3-journal

# Flask stuff:
instance/
.webassets-cache

# Scrapy stuff:
.scrapy

# Sphinx documentation
docs/_build/

# PyBuilder
.pybuilder/
target/

# Jupyter Notebook
.ipynb_checkpoints

# IPython
profile_default/
ipython_config.py

# pyenv
#   For a library or package, you might want to ignore these files since the code is
#   intended to run in multiple environments; otherwise, check them in:
# .python-version

# pipenv
#   According to pypa/pipenv#598, it is recommended to include Pipfile.lock in version control.
#   However, in case of collaboration, if having platform-specific dependencies or dependencies
#   having no cross-platform support, pipenv may install dependencies that don't work, or not
#   install all needed dependencies.
#Pipfile.lock

# poetry
#   Similar to Pipfile.lock, it is generally recommended to include poetry.lock in version control.
#   This is especially recommended for binary packages to ensure reproducibility, and is more
#   commonly ignored for libraries.
#   https://python-poetry.org/docs/basic-usage/#commit-your-poetrylock-file-to-version-control
#poetry.lock

# pdm
#   Similar to Pipfile.lock, it is generally recommended to include pdm.lock in version control.
#pdm.lock
#   pdm stores project-wide configurations in .pdm.toml, but it is recommended to not include it
#   in version control.
#   https://pdm.fming.dev/latest/usage/project/#working-with-version-control
.pdm.toml
.pdm-python
.pdm-build/

# PEP 582; used by e.g. github.com/David-OConnor/pyflow and github.com/pdm-project/pdm
__pypackages__/

# Celery stuff
celerybeat-schedule
celerybeat.pid

# SageMath parsed files
*.sage.py

# Environments
.env
.venv
env/
venv/
ENV/
env.bak/
venv.bak/

# Spyder project settings
.spyderproject
.spyproject

# Rope project settings
.ropeproject

# mkdocs documentation
/site

# mypy
.mypy_cache/
.dmypy.json
dmypy.json

# Pyre type checker
.pyre/

# pytype static type analyzer
.pytype/

# Cython debug symbols
cython_debug/

# PyCharm
#  JetBrains specific template is maintained in a separate JetBrains.gitignore that can
#  be found at https://github.com/github/gitignore/blob/main/Global/JetBrains.gitignore
#  and can be added to the global gitignore or merged into this file.  For a more nuclear
#  option (not recommended) you can uncomment the following to ignore the entire idea folder.
#.idea/

"""
    create_file(gitignore_file, gitignore_content)

    # Create __init__.py file
    init_file = os.path.join(project_name, "__init__.py")
    create_file(init_file, "")

    # Create README.md file
    readme_file = os.path.join(project_name, "README.md")
    readme_content = f"""# {project_name}

Project description goes here.

"""
    create_file(readme_file, readme_content)

    # Create requirements.txt file
    requirements_file = os.path.join(project_name, "requirements.txt")
    requirements_content = "gradio\n"
    create_file(requirements_file, requirements_content)

    # Create WebUI files
    webui_file = os.path.join(project_name, f"{project_name}WebUI.py")
    webui_content = f"""# {project_name}WebUI.py
# --coding:utf-8--
# Time:{datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
# Author:{author_name}
# Email:{email}
# Description:

import gradio as gr
import argparse
from src.log import get_logger
import os

logger = get_logger(__name__)

script_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(script_dir)
output_dir = os.path.join(script_dir, "output")

def main():

    # Define the interface
    with gr.Blocks() as demo:
        with gr.TabItem("{project_name}"):
            gr.Markdown("## {project_name}")

            
    # Launch the interface
    parser = argparse.ArgumentParser(description="Demo")
    parser.add_argument(
        "--server_name", type=str, default="localhost", help="server name"
    )
    parser.add_argument("--server_port", type=int, default=8080, help="server port")
    parser.add_argument("--root_path", type=str, default=None, help="root path")
    args = parser.parse_args()

    demo.launch(
        server_name=args.server_name,
        server_port=args.server_port,
        root_path=args.root_path,
        show_api=False,
    )

if __name__ == "__main__":
    main()

"""
    create_file(webui_file, webui_content)

    # Create test files
    test_file = os.path.join(project_name, f"Test{project_name}.py")
    test_content = f"""# {test_file}
# --coding:utf-8--
# Time:{datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
# Author:{author_name}
# Email:{email}
# Description:

import os
script_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(script_dir)

#####################################################
# TODO: Add tests for {project_name}
# from src.xxx import xxx

# if __name__ == "__main__":
#     xxx()


#####################################################
# TODO: Add more tests for {project_name}

"""
    create_file(test_file, test_content)


if __name__ == "__main__":

    # Example usage:
    project_name = "MyApp"
    author_name = "Luckykefu"
    email = "3124568493@qq.com"

    # if os.path.exists(project_name):
    #     logger.error("Project already exists")
    #     # delete the project folder if it already exists
    #     import shutil

    #     shutil.rmtree(project_name)

    create_project(project_name, author_name, email)
