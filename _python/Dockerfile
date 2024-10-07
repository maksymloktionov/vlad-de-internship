FROM python:3.11.4

COPY requirements.txt .
COPY site_parser.py .

RUN python -m pip install -r /requirements.txt

CMD ["python", "./site_parser.py"]
