import datetime
import os
from .log import get_logger
import shutil

logger = get_logger(__name__)


def create_dir(dir: str):
    """Create a directory if it doesn't exist."""
    os.makedirs(dir, exist_ok=True)
    logger.info(f"Created directory: {dir}")


def create_file(file_path: str, content: str):
    """Create a file with the given content."""
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content)
    logger.info(f"Created file: {file_path}")


def create_project(project_name: str, author_name: str, email: str):
    """Create a new project with the given name, author, and email."""
    if os.path.exists(project_name):
        logger.warning(f"Project {project_name} already exists")
        if input("Do you want to continue? (y/n): ").strip().lower() != "y":
            logger.info("Operation cancelled by the user.")
            return
        shutil.rmtree(project_name)
        logger.info(f"Deleted existing project: {project_name}")
    
    if not project_name:
        logger.warning("No Project Name ")
        project_name = "NoProjectName"
    if not author_name:
        logger.warning("No Author Name ")
        author_name = "NoAuthorName"
    if not email:
        logger.warning("No Email ")
        email = "NoEmail"
    project_name = project_name.strip()
    author_name = author_name.strip()
    email = email.strip()
    if os.path.exists(project_name):
        logger.warning(f"Project {project_name} already exists")
        if input("Do you want to continue? (y/n): ").strip().lower() != "y":
            logger.info("Operation cancelled by the user.")
            return
        shutil.rmtree(project_name)
        logger.info(f"Deleted existing project: {project_name}")

    logger.info(f"Creating project: {project_name}")

    # Create project structure
    create_dir(project_name)
    create_dir(os.path.join(project_name, "src"))

    # Define file structure
    files = {
        os.path.join(project_name, "src", "log.py"): generate_log_content,
        os.path.join(
            project_name, "src", "__init__.py"
        ): lambda project_name, author_name, email: "",  # 更新为接受参数
        os.path.join(project_name, ".gitignore"): generate_gitignore_content,
        os.path.join(
            project_name, "README.md"
        ): lambda project_name, author_name, email: f"# {project_name}\n\nProject description goes here.\n",  # 更新为接受参数
        os.path.join(
            project_name, "requirements.txt"
        ): lambda project_name, author_name, email: "gradio\n",  # 更新为接受参数
        os.path.join(project_name, f"WebUI{project_name}.py"): generate_webui_content,
        os.path.join(project_name, f"Test{project_name}.py"): generate_test_content,
    }

    # Create files
    for file_path, content_generator in files.items():
        content = (
            content_generator(project_name, author_name, email)
            if callable(content_generator)
            else content_generator
        )
        create_file(file_path, content)

    logger.info(f"Project {project_name} created successfully")


def generate_log_content(project_name: str, author_name: str, email: str):
    return f"""# log.py
# --coding:utf-8--
# Time:{datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
# Author:{author_name}
# Email:{email}
# Description: Provides colored logging functionality

import logging
from colorama import Fore, Style, init
from functools import lru_cache

# Initialize colorama
init(autoreset=True)

# Define colors for different levels
LEVEL_COLORS = {{
    logging.DEBUG: Fore.BLUE,
    logging.INFO: Fore.GREEN,
    logging.WARNING: Fore.YELLOW,
    logging.ERROR: Fore.RED,
    logging.CRITICAL: Fore.MAGENTA,
}}


class ColoredFormatter(logging.Formatter):
    def format(self, record):
        color = LEVEL_COLORS.get(record.levelno, Style.RESET_ALL)
        message = super().format(record)
        return f"{{color}}{{message}}{{Style.RESET_ALL}}"


@lru_cache(maxsize=None)
def get_logger(name):
    logger = logging.getLogger(name)
    if not logger.handlers:
        logger.setLevel(logging.DEBUG)
        formatter = ColoredFormatter(
            "%(asctime)s - %(levelname)s - %(pathname)s:%(lineno)d - %(message)s"
        )
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.DEBUG)
        console_handler.setFormatter(formatter)
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


def generate_gitignore_content(*args):
    return """# Project-specific directories
/cookies/
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
#.python-version

# pipenv
#Pipfile.lock

# poetry
#poetry.lock

# pdm
.pdm.toml
.pdm-python
.pdm-build/

# PEP 582
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
#.idea/

# VS Code
.vscode/

# OS generated files
.DS_Store
.DS_Store?
._*
.Spotlight-V100
.Trashes
ehthumbs.db
Thumbs.db

# Logs and databases
*.log
*.sql
*.sqlite

# Compiled source
*.com
*.class
*.dll
*.exe
*.o
*.out
"""


def generate_webui_content(project_name: str, author_name: str, email: str):
    return f"""# {project_name}WebUI.py
# --coding:utf-8--
# Time:{datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
# Author:{author_name}
# Email:{email}
# Description: A simple Gradio web interface for testing purposes

import gradio as gr
import argparse
from src.log import get_logger
import os

logger = get_logger(__name__)

# Set up directory paths
script_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(script_dir)
output_dir = os.path.join(script_dir, "output")
os.makedirs(output_dir, exist_ok=True)


def create_interface_{project_name}():

    # Create and return the Gradio interface.
    with gr.Blocks() as demo:
        gr.Markdown("## {project_name}")
        input_text = gr.Textbox(label="Input")
        output_text = gr.Textbox(label="Output")
        submit_btn = gr.Button("Submit")

        def process_input(text):
            # Example processing function
            return f"Processed: {{text}}"

        submit_btn.click(fn=process_input, inputs=input_text, outputs=output_text)

    return demo


def parse_arguments():

    # Parse command line arguments.
    parser = argparse.ArgumentParser(description=f"{{__file__}}")
    parser.add_argument(
        "--server_name", type=str, default="localhost", help="Server name"
    )
    parser.add_argument("--server_port", type=int, default=None, help="Server port")
    parser.add_argument("--root_path", type=str, default=None, help="Root path")
    return parser.parse_args()


def main():
    args = parse_arguments()
    with gr.Blocks() as demo:
        create_interface_{project_name}()
    logger.info(f"Starting server on {{args.server_name}}:{{args.server_port}}")
    demo.launch(
        server_name=args.server_name,
        server_port=args.server_port,
        root_path=args.root_path,
        show_api=False,
    )


if __name__ == "__main__":
    main()

"""


def generate_test_content(project_name: str, author_name: str, email: str):

    return f"""# Test{project_name}.py
# --coding:utf-8--
# Time:{datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
# Author:{author_name}
# Email:{email}
# Description: Test suite for the Test project

import unittest
import os
from src.log import get_logger

logger = get_logger(__name__)

script_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(script_dir)


class TestProject(unittest.TestCase):
    def setUp(self):
        logger.info("Setting up test environment")
        # Add any setup code here

    def tearDown(self):
        logger.info("Tearing down test environment")
        # Add any cleanup code here

    def test_example(self):
        logger.info("Running example test")
        self.assertEqual(1 + 1, 2, "Basic addition test")

    def test_logger(self):
        logger.info("Testing logger functionality")
        # This test doesn't assert anything, but it demonstrates that the logger works
        logger.debug("Debug message")
        logger.info("Info message")
        logger.warning("Warning message")
        logger.error("Error message")
        logger.critical("Critical message")

    # TODO: Add more specific tests for your project here
    # def test_specific_function(self):
    #     from src.your_module import your_function
    #     result = your_function(test_input)
    #     self.assertEqual(result, expected_output)


if __name__ == "__main__":
    unittest.main()

"""


if __name__ == "__main__":
    project_name = input("Enter project name: ")
    author_name = input("Enter author name: ")
    email = input("Enter email: ")

    create_project(project_name, author_name, email)
