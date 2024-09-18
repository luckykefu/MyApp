# ImgProcessWebUI.py
# --coding:utf-8--
# Time:2024-09-17 06:50:59
# Author:Luckykefu
# Email:3124568493@qq.com
# Description:

import os
import gradio as gr
import argparse

from GitAutoPush.src.git_auto_push import git_auto_push
from src.log import get_logger

logger = get_logger(__name__)
#################
from AudioProcess.src.demo_BPM import demo_BPM
from AudioProcess.src.demo_split_audio_and_video import demo_split_audio_and_video
from AudioProcess.src.demo_audio_clip import demo_audio_clip
from AudioProcess.src.demo_edgeTTS import demo_edge_tts

####################
from AutoPublishVideo.src.demo_autopunlish import demo_auto_publish_video
from dotenv import load_dotenv

load_dotenv()
################################################
from GitAutoPush.src.demo_gitautopush import demo_gitautopush

###############################################
from ImgProcess.src.demo import demo_gen_cover, demo_video_to_frames, demo_mergeImg

#############################################
from UpdateSubtitle.src.demo import demo_srt, demo_lrc2srt, demo_xstudio_lrc

#############################################################
from WhisperWebUI.src.demo import demo_whisper

#########################################################
from YTBDL.src.demo import demo_download_from_youtube

#################################################


script_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(script_dir)

####################################################


def parse_arguments():

    # Parse command line arguments.
    parser = argparse.ArgumentParser(description=f"{__file__}")
    parser.add_argument(
        "--server_name", type=str, default="localhost", help="Server name"
    )
    parser.add_argument("--server_port", type=int, default=None, help="Server port")
    parser.add_argument("--root_path", type=str, default=None, help="Root path")
    return parser.parse_args()


def main():
    logger.info(__file__)
    args = parse_arguments()

    # Define the interface
    with gr.Blocks() as demo:
        gr.Markdown("## MyApp")
        with gr.TabItem("AutoPublishWebUI"):
            demo_auto_publish_video()
    
        with gr.TabItem("YTBDL"):
            demo_download_from_youtube()

        with gr.TabItem("Update Subtitle"):
            with gr.TabItem("SRT"):
                demo_srt()
            with gr.TabItem("LRC2SRT"):
                demo_lrc2srt()

            with gr.TabItem("X studiolrc"):
                demo_xstudio_lrc()

        with gr.TabItem("ImgProcess"):
            with gr.TabItem("Merge Images"):
                demo_mergeImg()

            with gr.TabItem("Video Frame Interpolation"):
                demo_video_to_frames()

            with gr.TabItem("Gen Cover"):
                demo_gen_cover()

        with gr.TabItem("GitAutoPush"):
            demo_gitautopush()

        with gr.TabItem("WhisperWebUI"):
            demo_whisper()

        with gr.TabItem("AudioProcess"):
            with gr.TabItem("BPM"):
                demo_BPM()
            with gr.TabItem("Split Audio and Video"):
                demo_split_audio_and_video()
            with gr.TabItem("Audio Clip"):
                demo_audio_clip()
            with gr.TabItem("edge-tts"):
                demo_edge_tts()

    demo.launch(
        server_name=args.server_name,
        server_port=args.server_port,
        root_path=args.root_path,
        show_api=False,
    )


if __name__ == "__main__":
    main()
