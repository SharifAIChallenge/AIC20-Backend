FROM python:latest

RUN apt-get update && apt-get install -yq vim curl gettext
RUN apt-get install -yq redis-server
RUN mkdir /root/thebackend
COPY requirements.txt /root/thebackend/requirements.txt
WORKDIR /root/thebackend
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
COPY . /root/thebackend
