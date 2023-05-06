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
        res = requests.get(
            "https://k0gh2dp2jg.execute-api.ap-northeast-1.amazonaws.com/test/?PassWord=aflkajflalkalbnjlsrkaerl&UserName=LambdaWaniwani",
            timeout=3,
        )
        res.raise_for_status()
        if "FLAG{l4mabd4_1s_s3rverl3ss_s3rv1c3}" in res.text:
            return 0
        else:
            return 1
    except Exception:
        return 1


if __name__ == "__main__":
    if rev_wasm(sys.argv[1]) != 0:
        exit(1)
