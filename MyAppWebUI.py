# ImgProcessWebUI.py
# --coding:utf-8--
# Time:2024-09-17 06:50:59
# Author:Luckykefu
# Email:3124568493@qq.com
# Description:

import os
import gradio as gr
import argparse
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
load_dotenv()


logger = get_logger(__name__)

# 获取脚本所在目录的绝对路径
script_dir = os.path.dirname(os.path.abspath(__file__))

# 更改当前工作目录
os.chdir(script_dir)

# 创建临时文件夹
output_dir = os.path.join(script_dir, "output")
whisper_models_dir = os.path.join(script_dir, "WhisperWebUI", "whisper_models")
if os.path.exists(whisper_models_dir):
    whisper_models = os.listdir(whisper_models_dir)
    whisper_models_path = [
        os.path.join(whisper_models_dir, model) for model in whisper_models
    ]


def main():

    # Define the interface
    with gr.Blocks() as demo:
        gr.Markdown("## MyApp")
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
