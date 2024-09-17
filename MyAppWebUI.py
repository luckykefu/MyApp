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

#################
# WhisperWebUI
from WhisperWebUI.src.audio2text import audio2text

#################
from AudioProcess.src.audio_clip import audio_clip
from AudioProcess.src.extract_audio import extract_audio
from AudioProcess.src.get_key_and_bpm import get_key_and_bpm
from AudioProcess.src.edgeTTS import *
from AudioProcess.src.log import get_logger

####################
from AutoPublishVideo.src.auto_publish_video_func.blbl import publish_to_blbl
from AutoPublishVideo.src.auto_publish_video_func.xhs import publish_to_xhs
from AutoPublishVideo.src.auto_publish_video_func.zhihu import publish_to_zhihu
from AutoPublishVideo.src.auto_publish_video_func.weibo import publish_to_weibo
from AutoPublishVideo.src.auto_publish_video_func.dy import publish_to_dy
from AutoPublishVideo.src.auto_publish_video_func.ks import publish_to_ks
from AutoPublishVideo.src.auto_publish_video_func.sph import publish_to_sph
from AutoPublishVideo.src.auto_publish_video_func.bjh import publish_to_bjh
from AutoPublishVideo.src.auto_publish_video_func.vivo import publish_to_vivo
from AutoPublishVideo.src.auto_publish import save_title_description_tags
from AutoPublishVideo.src.clear_gradio_cache import clear_gradio_cache
from dotenv import load_dotenv
################################################
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
load_dotenv()
logger = get_logger(__name__)
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
###################################################################
PATH_FILE = os.path.join(output_dir, "git_repo_path.txt")


def read_git_repo_path():
    """从文件中读取 git_repo_path"""
    if os.path.exists(PATH_FILE):
        with open(PATH_FILE, "r") as file:
            return file.read().strip()
    else:
        return "/path/to/your/repo branch"


def write_git_repo_path(path):
    """将 git_repo_path 写入文件"""
    with open(PATH_FILE, "w") as file:
        file.write(path)
        logger.info(f"Write git_repo_path to {PATH_FILE}: {path}")
    return path


# 初始化状态变量
initial_git_repo_path = read_git_repo_path()
####################################################################


def main():

    # Define the interface
    with gr.Blocks() as demo:
        gr.Markdown("## MyApp")
        git_repo_path_state = gr.State(initial_git_repo_path)  # Store the git_repo_path

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
                    fn=update_xstudio_lrc, inputs=[sc_lrc, tgt_lrc], outputs=[output_lrc]
                )

        with gr.TabItem("ImgProcess"):
            with gr.TabItem("图片合并"):

                with gr.Row():

                    img1 = gr.Image(label="图片1", type="filepath")

                    img2 = gr.Image(label="图片2", type="filepath")

                merge_btn = gr.Button("合并图片")

                merged_img = gr.Image(label="合并后的图片", type="filepath")

                merge_btn.click(fn=merge_images, inputs=[img1, img2], outputs=merged_img)

            with gr.TabItem("视频插帧"):
                with gr.Row():

                    video_input = gr.Video(label="上传视频")

                    target_fps = gr.Slider(label="目标FPS", value=25, minimum=1, maximum=60)

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
                        choices=["jpg", "png", "jpeg"], label="输出图片格式", value="png"
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
            gr.Markdown("## GitAutoPush")
            with gr.Row():
                git_repo_path = gr.Textbox(
                    label="Git Repo Path",
                    value=initial_git_repo_path,
                    lines=1,
                )
                git_repo_path.change(
                    fn=lambda x: write_git_repo_path(x),  # 更新文件中的路径
                    inputs=[git_repo_path],
                    outputs=[git_repo_path],
                )  # 更新 State

                git_message = gr.Textbox(label="Git Message", value="", lines=2)
            with gr.Row():
                git_username = gr.Textbox(label="Git Username", value="")
                git_email = gr.Textbox(label="Git Email", value="")
            with gr.Row():
                git_auto_push_btn = gr.Button("GitAutoPush")

                git_auto_push_btn.click(
                    fn=git_auto_push,
                    inputs=[
                        git_repo_path_state,  # 使用 State 而不是 Textbox
                        git_message,
                        git_username,
                        git_email,
                    ],
                    outputs=[],
                )

        with gr.TabItem("AutoPublishWebUI"):
            gr.Markdown("## AutoPublishWebUI")
            gr.Markdown("### 清除gradio缓存")
            clear_cache_btn = gr.Button("RUN", key="clear_cache")
            clear_cache_btn.click(fn=clear_gradio_cache)

            gr.Markdown("### 发布参数")
            with gr.Row():

                video_file_path = gr.Video(label="上传视频")

                with gr.Column():
                    json_file_path = gr.File(
                        label="标题描述标签json文件", type="filepath"
                    )

                    title = gr.Textbox(label="标题", value="", lines=1)
                    description = gr.Textbox(label="描述", value="", lines=2)
                    tags = gr.Textbox(label="标签", value="#", lines=1)

                with gr.Column():
                    json_output_path = gr.File(
                        label="保存标题描述标签为json文件", type="filepath"
                    )

            title.change(
                fn=save_title_description_tags,
                inputs=[title, description, tags],
                outputs=[json_output_path],
            )
            description.change(
                fn=save_title_description_tags,
                inputs=[title, description, tags],
                outputs=[json_output_path],
            )
            tags.change(
                fn=save_title_description_tags,
                inputs=[title, description, tags],
                outputs=[json_output_path],
            )

            with gr.Row():
                xhs_btn = gr.Button("发布到xhs")
                zhihu_btn = gr.Button("发布到知乎")
                bili_btn = gr.Button("发布到哔哩哔哩")
                wb_btn = gr.Button("发布到微博")
                dy_btn = gr.Button("发布到抖音")
                ks_btn = gr.Button("发布到快手")
                sph_btn = gr.Button("发布到视频号")
                bjh_btn = gr.Button("发布到百家号")
                vivo_btn = gr.Button("发布到Vivo号")

            xhs_btn.click(
                fn=publish_to_xhs,
                inputs=[video_file_path, title, description, tags, json_file_path],
                outputs=[],
            )
            bili_btn.click(
                fn=publish_to_blbl,
                inputs=[video_file_path, title, description, tags, json_file_path],
                outputs=[],
            )
            dy_btn.click(
                fn=publish_to_dy,
                inputs=[video_file_path, title, description, tags, json_file_path],
                outputs=[],
            )
            ks_btn.click(
                fn=publish_to_ks,
                inputs=[video_file_path, title, description, tags, json_file_path],
                outputs=[],
            )
            wb_btn.click(
                fn=publish_to_weibo,
                inputs=[video_file_path, title, description, tags, json_file_path],
                outputs=[],
            )
            sph_btn.click(
                fn=publish_to_sph,
                inputs=[video_file_path, title, description, tags, json_file_path],
                outputs=[],
            )
            bjh_btn.click(
                fn=publish_to_bjh,
                inputs=[video_file_path, title, description, tags, json_file_path],
                outputs=[],
            )
            vivo_btn.click(
                fn=publish_to_vivo,
                inputs=[video_file_path, title, description, tags, json_file_path],
                outputs=[],
            )
            zhihu_btn.click(
                fn=publish_to_zhihu,
                inputs=[video_file_path, title, description, tags, json_file_path],
                outputs=[],
            )

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
                audio_file_path2 = gr.File(label="上传音频文件", type="filepath")
                bpm_btn = gr.Button("RUN")
                with gr.Row():
                    bpm_output = gr.Number(label="BPM")
                    key_output = gr.Textbox(label="Key")
                    mode_output = gr.Textbox(label="Mode")
                bpm_btn.click(
                    fn=get_key_and_bpm,
                    inputs=[audio_file_path2],
                    outputs=[bpm_output, key_output, mode_output],
                )

            with gr.TabItem("音视频分离"):
                with gr.Row():
                    video_file_path1 = gr.Video(
                        label="上传视频文件", sources=["upload"]
                    )
                    extract_audio_btn = gr.Button("RUN")
                    video_output = gr.Video(label="提取的视频")
                    audio_output_path1 = gr.Audio(label="提取的音频")

                extract_audio_btn.click(
                    fn=extract_audio,
                    inputs=[video_file_path1],
                    outputs=[video_output, audio_output_path1],
                )

            with gr.TabItem("音频裁剪"):
                with gr.Row():
                    audio_file_path3 = gr.Audio(label="上传音频文件", type="filepath")
                    start_time = gr.Number(label="开始时间", value=0)
                    end_time = gr.Number(label="结束时间", value=10)
                    audio_output_path2 = gr.Audio(label="裁剪后的音频", type="filepath")
                    audio_cut_btn = gr.Button("RUN")

                audio_cut_btn.click(
                    fn=audio_clip,
                    inputs=[audio_file_path3, start_time, end_time],
                    outputs=[audio_output_path2],
                )

            with gr.TabItem("TXT2Audio edge-tts"):
                with gr.Row():
                    text_input2 = gr.Textbox(
                        label="输入文本", lines=4, value="你好，欢迎使用 EDGETTS！"
                    )

                with gr.Column():
                    VOICE_CHOICES = asyncio.run(get_edge_tts_voices())

                    voice_dropdown = gr.Dropdown(
                        choices=VOICE_CHOICES,
                        label="声音选择",
                        value=VOICE_CHOICES[0],
                        allow_custom_value=True,
                    )
                    output_dir3 = gr.Textbox(label="Output Dir", value=output_dir)
                with gr.Column():
                    generate_button = gr.Button("Generate Audio")
                with gr.Column():
                    audio_output = gr.Audio(label="Generated Audio")
                generate_button.click(
                    fn=edge_tts_func,
                    inputs=[
                        text_input2,
                        voice_dropdown,
                        output_dir3,
                    ],
                    outputs=audio_output,
                    queue=True,  # 可选
                )

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
