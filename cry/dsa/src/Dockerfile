FROM python:3.10

RUN apt update && apt upgrade -y
RUN apt install socat -y
RUN pip install pycryptodome

ADD chall.py chall.py
CMD socat -T 2 -dd -v >/dev/stdout TCP-L:50000,fork,reuseaddr EXEC:"python -u chall.py"
