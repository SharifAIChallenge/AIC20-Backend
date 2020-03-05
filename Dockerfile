FROM python:3.8

RUN apt update && apt install -y vim curl gettext

WORKDIR /app/
ADD ./requirements.txt ./requirements.txt

ENV PIP_NO_CACHE_DIR 1
RUN pip install -r ./requirements.txt

ADD ./ ./
