FROM python:3.11.4

ARG DATA

COPY . /app

RUN apt-get update && apt-get install -y \
    curl \
    unzip \
    && rm -rf /var/lib/apt/lists/* \
    && mkdir app/data \
    && mkdir -p /root/.kaggle/ \
    && mv app/kaggle.json /root/.kaggle/kaggle.json \
    && chmod 600 /root/.kaggle/kaggle.json \
    && pip3 install -r app/requirements.txt \
    && kaggle datasets download -d ${DATA} \
    && unzip *.zip -d ./app/data \
    && rm -rf *.zip \
    && cd app

WORKDIR /app

ENV DBT_PROFILES_DIR=/app/
ENV DBT_PROJECT_DIR=/app/

# CMD [ "python3", "parser.py" ]
