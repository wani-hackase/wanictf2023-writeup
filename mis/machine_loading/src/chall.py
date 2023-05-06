import torch
from flask import Flask, request, render_template
from io import BytesIO
import pathlib
import os

app = Flask(__name__, template_folder="/app/templates")


@app.route("/", methods=["GET"])
def index():
    return render_template("upload.html")


@app.route("/upload", methods=["POST"])
def upload():
    file = request.files["file"]
    if not file:
        return "No file uploaded.", 422
    if file.content_length > 1024 * 1024:  # 1MB
        return "File too large. Max size is 1MB.", 400

    suffix = pathlib.Path(file.filename).suffix
    if suffix == ".ckpt":
        try:
            modelload(file)

            if os.path.exists("output_dir/output.txt"):
                with open("output_dir/output.txt", "r") as f:
                    msg = f.read()
                os.remove("output_dir/output.txt")

            return f"File loaded successfully: {msg}"
        except Exception as e:
            return "ERROR: " + str(e), 400
    else:
        return "Invalid file extension. Only .ckpt allowed.", 400


def modelload(file):
    with BytesIO(file.read()) as f:
        try:
            torch.load(f)
            return
        except Exception as e:
            raise e


if __name__ == "__main__":
    app.run(host="0.0.0.0")
