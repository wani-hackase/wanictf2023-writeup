import requests
from urllib.parse import urljoin
import sys


def rev_wasm(host):
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
        res = requests.get(urljoin(host, "index.wasm"), timeout=3)
        res.raise_for_status()
        return 0
    except Exception:
        return 1


if __name__ == "__main__":
    if rev_wasm(sys.argv[1]) != 0:
        exit(1)
