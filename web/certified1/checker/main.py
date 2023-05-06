import os
import requests
import sys


IMAGE_PATH = os.path.join(os.path.dirname(__file__), "payload.png")


def web_certified1(host):
    with open(IMAGE_PATH, "rb") as f:
        payload = f.read()

    try:
        res = requests.post(
            f"https://{host}/create",
            files={"file": ("payload.png", payload)},
            timeout=3,
        )
    except requests.exceptions.RequestException:
        return 2

    if res.content.startswith(b"\x89PNG"):
        return 0
    else:
        return 1


if __name__ == "__main__":
    if web_certified1(sys.argv[1]) != 0:
        exit(1)
