from pathlib import Path
import gradio as gr
import os
import glob
import shutil
import subprocess

import db

# Initialize AtlasDatabase
atlasDB = db.AtlasDatabase()


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
        "5",
        "--langs",
        "English",
    ]

    result = subprocess.run(command, capture_output=True, text=True)

    # Check the result
    if result.returncode == 0:
        gr.Info("Converted Successfully")
        print("[AtlasParser Logs] ", result.stdout)
        return [
            gr.Textbox(placeholder=f"{name} Successfully converted!"),
            gr.Button(visible=False),
            gr.Button(visible=True),
            gr.Textbox(
                value="/output/" + name.split(".")[0] + "/" + name.split(".")[0] + ".md"
            ),
        ]
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
        gr.Button(visible=True),
    ]


def save_to_db(fileobj):
    print(f"Path is {fileobj}")

    decadal_path = Path(fileobj).parent

    image_files = glob.glob(os.path.join(os.getcwd() + str(decadal_path), "*.png"))

    print(image_files)

    atlasDB.upload_files(os.path.join(os.getcwd() + fileobj), image_files, gr)


with gr.Blocks() as demo:
    gr.Markdown(
        """
        # Atlas Parser
        Improving Accuracy for LLMs
        """
    )
    path_to_file = gr.Textbox(visible=False)

    upload_button = gr.UploadButton("Click to Upload a File")
    output = gr.Textbox(
        label="Status", placeholder="Waiting for File...", interactive=False
    )
    markup_button = gr.Button("Markup", visible=False)

    save_to_db_button = gr.Button("Save to Database", visible=False)

    upload_button.upload(
        process_file,
        upload_button,
        [upload_button, output, markup_button],
    )

    markup_button.click(
        fn=convert_file,
        inputs=upload_button,
        outputs=[output, markup_button, save_to_db_button, path_to_file],
        api_name="convert_file",
    )

    save_to_db_button.click(fn=save_to_db, inputs=path_to_file)


demo.launch()
