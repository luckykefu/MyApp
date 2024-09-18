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
# WhisperWebUI
from WhisperWebUI.src.audio2text import audio2text

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
from ImgProcess.src.merge_images import merge_images
from ImgProcess.src.video_to_frames import video_to_frames
from ImgProcess.src.make_cover import make_cover

#############################################
from UpdateSubtitle.src.update_xstudio_lrc import update_xstudio_lrc
from UpdateSubtitle.src.extract_text import extract_text
from UpdateSubtitle.src.lrc2srt import lrc2srt
from UpdateSubtitle.src.update_srt_with_new_subtitles import (
    update_srt_with_new_subtitles,
)

#########################################################
from YTBDL.src.download_from_youtube import download_from_youtube

#################################################


script_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(script_dir)
output_dir = os.path.join(script_dir, "output")
####################################################
whisper_models_dir = os.path.join(script_dir, "WhisperWebUI", "whisper_models")
if os.path.exists(whisper_models_dir):
    whisper_models = os.listdir(whisper_models_dir)
    whisper_models_path = [
        os.path.join(whisper_models_dir, model) for model in whisper_models
    ]

####################################################################
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
            gr.Markdown("## YTBDL")
            ytb_url = gr.Textbox(
                label="Youtube URL",
                lines=1,
                value="https://www.youtube.com/watch?v=qASkoV5TsAg",
            )
            proxy_arg = gr.Textbox(
                label="Proxy", lines=1, value="socks5://192.168.43.1:1088"
            )
            ytb_output_dir = gr.Textbox(label="Output Dir", value=output_dir)
            download_btn = gr.Button("Download")
            download_btn.click(
                fn=download_from_youtube,
                inputs=[ytb_url, proxy_arg, ytb_output_dir],
                outputs=[],
            )

        with gr.TabItem("Update Subtitle"):
            with gr.TabItem("SRT"):
                with gr.Row():
                    srt_file_path = gr.File(label="上传srt文件", type="filepath")
                with gr.Row():
                    srt_output1 = gr.Textbox(label="原srt文本", lines=10, value="")
                    text_input1 = gr.Textbox(
                        label="输入新srt文本", lines=10, value="每行一个字幕"
                    )
                    srt_output2 = gr.Textbox(label="更新srt", lines=10, value="")

                # 当 srt_file_path 发生变化时，自动调用 extract_text 函数
                srt_file_path.change(
                    fn=extract_text,
                    inputs=[srt_file_path],
                    outputs=[srt_output1],
                )

                with gr.Row():
                    update_srt_btn = gr.Button("更新srt")
                with gr.Row():
                    srt_output_path = gr.File(label="输出srt文件", type="filepath")
                with gr.Row():
                    update_srt_btn.click(
                        fn=update_srt_with_new_subtitles,
                        inputs=[srt_file_path, text_input1],
                        outputs=[srt_output_path, srt_output2],
                    )

            with gr.TabItem("LRC2SRT"):
                with gr.Row():
                    lrc_file_path = gr.File(label="上传lrc文件", type="filepath")
                lrc2srt_btn = gr.Button("RUN")
                with gr.Row():
                    lrc_output1 = gr.Textbox(label="原lrc文本", lines=10, value="")
                    text_input1 = gr.Textbox(label="原lrc文本", lines=10, value="")
                with gr.Row():
                    lrc_output2 = gr.Textbox(label="新srt文本", lines=10, value="")
                    text_input2 = gr.Textbox(label="新srt文本", lines=10, value="")
                with gr.Row():
                    srt_file_out = gr.File(label="输出srt文件", type="filepath")
                    text_file_output = gr.File(label="输出text文件", type="filepath")

                lrc2srt_btn.click(
                    fn=lrc2srt,
                    inputs=[lrc_file_path],
                    outputs=[
                        lrc_output1,
                        text_input1,
                        lrc_output2,
                        text_input2,
                        srt_file_out,
                        text_file_output,
                    ],
                )

            with gr.TabItem("X studiolrc"):
                with gr.Row():
                    sc_lrc = gr.Textbox(label="sc_lrc", value="", lines=6)
                    tgt_lrc = gr.Textbox(label="tgt_lrc", value="", lines=6)
                run_btn = gr.Button("run")
                output_lrc = gr.Textbox(label="output_lrc", value="", lines=6)
                run_btn.click(
                    fn=update_xstudio_lrc,
                    inputs=[sc_lrc, tgt_lrc],
                    outputs=[output_lrc],
                )

        with gr.TabItem("ImgProcess"):
            with gr.TabItem("图片合并"):

                with gr.Row():

                    img1 = gr.Image(label="图片1", type="filepath")

                    img2 = gr.Image(label="图片2", type="filepath")

                merge_btn = gr.Button("合并图片")

                merged_img = gr.Image(label="合并后的图片", type="filepath")

                merge_btn.click(
                    fn=merge_images, inputs=[img1, img2], outputs=merged_img
                )

            with gr.TabItem("视频插帧"):
                with gr.Row():

                    video_input = gr.Video(label="上传视频")

                    target_fps = gr.Slider(
                        label="目标FPS", value=25, minimum=1, maximum=60
                    )

                    video_output = gr.Video(label="处理后的视频")

                with gr.Row():

                    interpolate_btn = gr.Button("ffmpeg 插帧")

                    interpolate_btn2 = gr.Button("rife 插帧")

                interpolate_btn.click(
                    fn=video_to_frames,
                    inputs=[video_input, target_fps],
                    outputs=video_output,
                )
                # interpolate_btn2.click(fn=process_video_interpolation, inputs=[video_input,target_fps], outputs=video_output)

            with gr.TabItem("Gen Cover"):
                with gr.Row():

                    img_input = gr.Image(label="上传图片")
                    with gr.Column():
                        output_dir2 = gr.Textbox(label="Output Dir", value=output_dir)
                        video_width2 = gr.Number(label="Video Width", value=1080)
                        video_height2 = gr.Number(label="Video Height", value=1920)

                with gr.Row():

                    title = gr.Textbox(label="标题", value="标题", lines=3)

                    font_path = gr.File(label="字体文件")

                    font_size = gr.Slider(
                        label="字体大小", value=250, minimum=1, maximum=500
                    )

                    font_color = gr.ColorPicker(label="字体颜色", value="#000000")
                    output_img_fmt = gr.Dropdown(
                        choices=["jpg", "png", "jpeg"],
                        label="输出图片格式",
                        value="png",
                    )
                make_cover_btn = gr.Button("make cover")

                cover_output = gr.Image(label="输出封面")

                make_cover_btn.click(
                    fn=make_cover,
                    inputs=[
                        img_input,
                        output_dir2,
                        video_width2,
                        video_height2,
                        title,
                        font_path,
                        font_size,
                        font_color,
                        output_img_fmt,
                    ],
                    outputs=[cover_output],
                )

        with gr.TabItem("GitAutoPush"):
            demo_gitautopush()

        with gr.TabItem("WhisperWebUI"):
            with gr.Row():
                audio_file_path5 = gr.Audio(label="上传音频文件", type="filepath")
                model_path = gr.Dropdown(
                    choices=whisper_models_path,
                    label="模型选择",
                    value=whisper_models_path[0],
                )
                with gr.Row():
                    prompt = gr.Textbox(label="Prompt", value="中文", lines=2)
                    output_format = gr.Dropdown(
                        choices=["txt", "vtt", "srt", "tsv", "json", "all"],
                        label="输出格式",
                        value="all",
                    )
                    output_dir1 = gr.Textbox(label="输出文件夹", value=output_dir)
            with gr.Row():
                audio_recognition_btn = gr.Button("识别")

            gr.Markdown("### 文件在output文件夹下")
            with gr.Row():

                audio_recognition_output = gr.Textbox(
                    label="识别结果", lines=5, value=""
                )

            audio_recognition_btn.click(
                fn=audio2text,
                inputs=[
                    audio_file_path5,
                    model_path,
                    prompt,
                    output_format,
                    output_dir1,
                ],
                outputs=[audio_recognition_output],
            )

        with gr.TabItem("AudioProcess"):
            with gr.TabItem("BPM"):
                demo_BPM()
            with gr.TabItem("Split Audio and Video"):
                demo_split_audio_and_video()
            with gr.TabItem("Audio Clip"):
                demo_audio_clip()
            with gr.TabItem("edge-tts"):
                demo_edge_tts()
    # Launch the interface

    demo.launch(
        server_name=args.server_name,
        server_port=args.server_port,
        root_path=args.root_path,
        show_api=False,
    )


if __name__ == "__main__":
    main()
