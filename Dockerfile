FROM python:3.9-slim-buster

WORKDIR /main

ENV FILE_PATH=''

COPY main.py ./main.py
COPY requirements.txt ./requirements.txt
COPY health-importer-poll.yml ./health-importer-poll.yml

RUN pip3 install -r requirements.txt

CMD python3 -u main.py $FILE_PATH
