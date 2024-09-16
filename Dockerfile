FROM python:3.11.4

COPY requirements.txt .

RUN python -m pip install -r /requirements.txt
