import requests
import sys
import urllib.parse as urlparse


def web_db(host):
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
        res = requests.get(urlparse.urljoin(host, "/"), timeout=3)
        res.raise_for_status()
        if "FLAG{y0u_c4n_u3e_db_1n_br0wser}" in res.text:
            return 0
    except Exception:
        return 1


if __name__ == "__main__":
    if web_db(sys.argv[1]) != 0:
        exit(1)
