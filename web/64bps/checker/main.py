import requests
import sys


def web_64bps(host):
    if "http" not in host:
        host = "https://" + host

    try:
        res = requests.get(
            f"{host}/2gb.txt",
            headers={"Range": "bytes=2147483648-"},
            timeout=60,
        )
    except requests.exceptions.RequestException:
        return 2

    if res.text.strip() == "FLAG{m@ke_use_0f_r@n0e_reques7s_f0r_l@r9e_f1les}":
        return 0
    else:
        return 1


if __name__ == "__main__":
    if web_64bps(sys.argv[1]) != 0:
        exit(1)
