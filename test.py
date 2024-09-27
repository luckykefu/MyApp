import gradio as gr
import json

# 读取 JSON 文件
def read_json(file_obj):
    data = json.load(file_obj)
    return data

# 创建 Gradio 接口
def display_json(file):
    if file is None:
        return "No file uploaded."
    with open(file.name, 'r') as file_obj:
        data = read_json(file_obj)
    return json.dumps(data, indent=2)

# 创建 Gradio 文件上传和文本输出组件
iface = gr.Interface(
    fn=display_json,
    inputs=gr.File(label="Upload JSON File"),
    outputs=gr.Textbox(label="JSON Content"),
    title="JSON File Reader",
    description="Upload a JSON file and view its content."
)

# 启动 Gradio 界面
iface.launch()