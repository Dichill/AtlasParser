from logging import disable
from pathlib import Path
import gradio as gr
import os
import shutil
import subprocess


def convert_file(fileobj):
    name = Path(fileobj).name
    SAVE_FOLDER = "./output"
    if not os.path.exists(SAVE_FOLDER):
        os.mkdir(SAVE_FOLDER)

    command = [
        "marker_single",
        "./data/" + name,
        "./output/",
        "--batch_multiplier",
        "2",
        "--langs",
        "English",
    ]

    result = subprocess.run(command, capture_output=True, text=True)

    # Check the result
    if result.returncode == 0:
        gr.Info("Converted Successfully")
        print("Output:\n", result.stdout)
    else:
        gr.Info("Error occured, see terminal")
        print(result.stderr)


def process_file(fileobj):
    name = Path(fileobj).name
    UPLOAD_FOLDER = "./data"
    if not os.path.exists(UPLOAD_FOLDER):
        os.mkdir(UPLOAD_FOLDER)
    shutil.copy(fileobj, UPLOAD_FOLDER)
    gr.Info("Uploaded " + name)
    return [
        gr.UploadButton(visible=False),
        gr.Textbox(placeholder=f"{name}", visible=True),
        gr.Button(visible=True),
    ]


with gr.Blocks() as demo:
    gr.Markdown(
        """
        # Atlas Parser
        Improving Accuracy for LLMs
        """
    )
    upload_button = gr.UploadButton("Click to Upload a File")
    output = gr.Textbox(
        label="Status", placeholder="Waiting for File...", interactive=False
    )
    markup_button = gr.Button("Markup", visible=False)
    markup_button.click(
        fn=convert_file, inputs=upload_button, outputs=output, api_name="convert_file"
    )

    upload_button.upload(
        process_file, upload_button, [upload_button, output, markup_button]
    )

demo.launch()
