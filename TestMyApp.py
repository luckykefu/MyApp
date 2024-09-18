# MyApp\TestMyApp.py
# --coding:utf-8--
# Time:2024-09-17 23:59:44
# Author:Luckykefu
# Email:3124568493@qq.com
# Description:

import os
import sys

# Get the absolute path of the script's directory
script_dir = os.path.dirname(os.path.abspath(__file__))

# Add the script's directory to the Python path
sys.path.insert(0, script_dir)

# Change the current working directory to the script's directory
os.chdir(script_dir)

from src.log import get_logger

logger = get_logger(__file__)

# if __name__ == "__main__":
#     from src.create_project import create_project

#     project_name = "log.py.bak"
#     author = "Luckykefu"
#     email = "3124568493@qq.com"
#     create_project(project_name, author, email)

# if __name__ == "__main__":
#     from src.delete_path import delete_path

#     waittodel = "log.py.bak"
#     # 找出所有log.py.bak文件并删除
#     for root, dirs, files in os.walk(os.getcwd()):
#         for file in files:
#             if file == "log.py.bak":
#                 delete_path(os.path.join(root, file))

# if __name__ == "__main__":
#     from src.update_all_log_file import update_log_files

#     current_directory = os.getcwd()
#     update_log_files(current_directory)
#     logger.info("Log file update process completed.")

if __name__ == "__main__":
    from GitAutoPush.src.git_auto_push import git_auto_push

    git_paths = r"""D:\Github\0MyApp\AudioProcess main
D:\Github\0MyApp\AutoPublishVideo main
D:\Github\0MyApp\GitAutoPush main
D:\Github\0MyApp\ImgProcess main
D:\Github\0MyApp\UpdateSubtitle main
D:\Github\0MyApp\WhisperWebUI main
D:\Github\0MyApp\YTBDL main
D:\Github\0MyApp main
"""
    git_auto_push(git_paths)

