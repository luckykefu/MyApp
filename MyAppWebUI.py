# ImgProcessWebUI.py
# --coding:utf-8--
# Time:2024-09-17 06:50:59
# Author:Luckykefu
# Email:3124568493@qq.com
# Description:

import gradio as gr
import argparse
from src.log import get_logger

logger = get_logger(__name__)


def main():

    # Define the interface
    with gr.Blocks() as demo:
        gr.Markdown("## MyApp")

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
