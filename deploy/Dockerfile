FROM python:latest

WORKDIR /app/

RUN apt update && \
    apt install -y vim curl

ENV PIP_NO_CACHE_DIR 1
ADD ../requirements.txt ./
RUN pip install -r ./requirements.txt

ADD ./ ./
RUN ./manage.py collectstatic --noinput

ENTRYPOINT ["/bin/bash", "entry.sh"]
CMD ["api-server"]
