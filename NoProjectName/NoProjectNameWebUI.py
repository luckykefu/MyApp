# NoProjectNameWebUI.py
# --coding:utf-8--
# Time:2024-09-18 19:28:59
# Author:NoAuthorName
# Email:NoEmail
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


def create_interface():

    # Create and return the Gradio interface.
    with gr.Blocks() as demo:
        with gr.TabItem("Test"):
            gr.Markdown("## Test Interface")
            input_text = gr.Textbox(label="Input")
            output_text = gr.Textbox(label="Output")
            submit_btn = gr.Button("Submit")

            def process_input(text):
                # Example processing function
                return f"Processed: {text}"

            submit_btn.click(fn=process_input, inputs=input_text, outputs=output_text)

    return demo


def parse_arguments():

    # Parse command line arguments.
    parser = argparse.ArgumentParser(description="Test Web UI")
    parser.add_argument(
        "--server_name", type=str, default="localhost", help="Server name"
    )
    parser.add_argument("--server_port", type=int, default=7860, help="Server port")
    parser.add_argument("--root_path", type=str, default=None, help="Root path")
    return parser.parse_args()


def main():
    args = parse_arguments()
    demo = create_interface()

    logger.info(f"Starting server on {args.server_name}:{args.server_port}")
    demo.launch(
        server_name=args.server_name,
        server_port=args.server_port,
        root_path=args.root_path,
        show_api=False,
    )


if __name__ == "__main__":
    main()

