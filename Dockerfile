FROM python:3.11.4

WORKDIR /app

RUN pip install flask
RUN pip install psycopg2-binary

COPY . .

CMD ["flask", "run", "--host=0.0.0.0"]
