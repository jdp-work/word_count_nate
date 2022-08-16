# syntax=docker/dockerfile:1
 
FROM python:3.9.13-bullseye

COPY test_files /home/test_files
COPY *.py /home
COPY requirements.txt /home

WORKDIR "/home"

RUN pip install -r requirements.txt

EXPOSE 8080

ENTRYPOINT [ "python", "html_parse_server.py" ]