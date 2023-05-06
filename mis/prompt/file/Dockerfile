FROM python:3.10-bullseye

WORKDIR /app

COPY ./requirements.txt /app/requirements.txt
RUN pip install -U -r requirements.txt

COPY . .

CMD python main.py
