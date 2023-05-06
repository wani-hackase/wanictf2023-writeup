FROM python:3.10-buster

WORKDIR /app

RUN pip3 install torch==1.12.0+cpu torchvision==0.13.0+cpu torchaudio==0.12.0 --extra-index-url https://download.pytorch.org/whl/cpu
RUN pip3 install flask Werkzeug

ADD chall.py .
ADD templates templates
ADD flag.txt .
RUN mkdir output_dir

RUN chmod 755 /app/
RUN chmod 777 output_dir
RUN chmod 744 flag.txt
RUN chmod 755 chall.py
RUN chmod 755 -R templates

RUN useradd ctf_user

USER ctf_user

CMD ["python3", "chall.py"]
