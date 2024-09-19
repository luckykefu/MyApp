import gradio as gr
import os

from .create_project import create_project
from .log import get_logger
from .gen_pipreqs import gen_reqs
from .delete_path import delete_path
from .audio2wav import convert_audio

logger = get_logger(__file__)


def demo_audio2wav():
    with gr.Blocks() as demo:
        gr.Markdown("Audio to WAV")
        input_file = gr.Audio(label="Input File", type="filepath")
        with gr.Row():
            output_format = gr.Dropdown(
                label="Output Format", choices=["wav", "mp3", "ogg", "flac"]
            )
            output_dir = gr.Textbox(
                label="Output Directory", value=os.path.join(os.getcwd(), "output")
            )
            output_file = gr.Audio(label="Output File", type="filepath")
        with gr.Row():
            convert_button = gr.Button("Convert")
            convert_button.click(
                fn=convert_audio,
                inputs=[input_file, output_format, output_dir],
                outputs=[output_file],
            )
    return demo


def demo_delete_path():
    with gr.Blocks() as demo:
        gr.Markdown("Delete Path")
        with gr.Row():
            path = gr.Textbox(label="Path")
            delete_button = gr.Button("Delete")
            delete_button.click(fn=delete_path, inputs=[path], outputs=[path])
    return demo


def demo_create_project():
    with gr.Blocks() as demo:
        gr.Markdown("Create a new project")
        with gr.Row():
            project_name = gr.Textbox(label="Project Name")
        with gr.Row():
            author = gr.Textbox(label="Author")
        with gr.Row():
            email = gr.Textbox(label="Email")

        with gr.Row():
            create_project_button = gr.Button("Create Project")
            create_project_button.click(
                create_project,
                inputs=[project_name, author, email],
                outputs=[],
            )
    return demo


data_dir = os.path.join(os.getcwd(), "data")
os.makedirs(data_dir, exist_ok=True)

PATH_FILE = os.path.join(data_dir, "gen_pipreqs_path.txt")


def read_path():
    """从文件中读取 git_repo_path"""
    if os.path.exists(PATH_FILE):
        with open(PATH_FILE, "r", encoding="utf-8") as file:
            return file.read().strip()
    else:
        return "/path/to/your/project"


def write_path(path):
    """将 git_repo_path 写入文件"""
    with open(PATH_FILE, "w", encoding="utf-8") as file:
        file.write(path)
        logger.info(f"Write git_repo_path to {PATH_FILE}: {path}")
    return path


def demo_gen_pipreqs():
    with gr.Blocks() as demo:
        initial_git_repo_path = read_path()
        gr.Markdown("## Gen Pipreqs")
        with gr.Row():
            path = gr.Textbox(label="Path", value=initial_git_repo_path)
            path.change(fn=lambda x: write_path(x), inputs=[path], outputs=[path])
        with gr.Row():
            gen_pipreqs_button = gr.Button("Gen Pipreqs")
            gen_pipreqs_button.click(fn=gen_reqs, inputs=[path], outputs=[path])
    return demo
