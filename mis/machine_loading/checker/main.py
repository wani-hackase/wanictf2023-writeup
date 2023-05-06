import requests
from urllib.parse import urljoin
import sys


def mis_machine_loading(host):
    if "http" not in host:
        host = "https://" + host

    # connect check (main page)
    try:
        res = requests.get(host, timeout=3)
        res.raise_for_status()
    except Exception:
        return 2

    # check (secret page)
    try:
        with open("solver.ckpt", "rb") as solver:
            res = requests.post(
                urljoin(host, "upload"),
                files={"file": solver},
                timeout=3,
            )
        if "FLAG{Use_0ther_extens10n_such_as_safetensors}" in res.text:
            return 0
        else:
            return 1
    except Exception:
        return 1


if __name__ == "__main__":
    if mis_machine_loading(sys.argv[1]) != 0:
        exit(1)
