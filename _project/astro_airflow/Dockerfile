FROM quay.io/astronomer/astro-runtime:12.5.0

COPY ./btc_transformer /opt/airflow/dbt_prjct

WORKDIR /opt/airflow

USER root

RUN apt-get update \
    && apt-get install -y git \
    && { chmod -R 777 / || echo "Failed to change permissions for /"; }

ENV DBT_PROFILES_DIR=/opt/airflow/dbt_prjct
ENV DBT_PROJECT_DIR=/opt/airflow/dbt_prjct