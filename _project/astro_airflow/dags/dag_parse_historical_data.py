from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator
from os import getenv
from binance.spot import Spot
from datetime import datetime, timedelta
import csv

API = getenv('API_TOKEN')
API_NAME = getenv('TOKEN_NAME')
DATABRICKS_TOKEN = getenv('DATABRICKS_TOKEN')
DEFAULT_ARGS = {
    'owner': "vlad",
    'retries': 5,
    'retry_delay': timedelta(minutes=2)
}
symbol_lst = ["BTCUSDT", "DOGEUSDT", "SOLUSDT", "XRPUSDT", "SHIBUSDT", "ETHUSDT", "PEPEUSDT", "PNUTUSDT", "LTCUSDT", "BNBUSDT"]

client = Spot(api_key=API_NAME, api_secret=API)

def get_crypto_klines():
    all_crypto = []

    for smb in symbol_lst:
        coin = client.klines(symbol=smb, interval="1h", limit=1000)
        for row in coin:
            row.append(smb)

        all_crypto += coin
    print(len(all_crypto))    
    
    with open('crypto.csv', 'w', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerows(all_crypto)

with DAG(
    dag_id="btc_to_databricks",
    description="Crypto historical charts to databricks catalog",
    default_args=DEFAULT_ARGS,
    start_date=datetime(2024, 12, 1),
    schedule_interval="0 * * * *",
    catchup=False
) as dag:

    pull_data = PythonOperator(
        task_id="pull_crypto_historical_data",
        python_callable=get_crypto_klines
    )

    upload_file = BashOperator(
        task_id="upload_file_to_dbfs",
        bash_command=f"""
        curl -n -X POST -H "Authorization: Bearer {DATABRICKS_TOKEN}" \
        -F "file=@/opt/airflow/crypto.csv" \
        -F "path=/crypto/crypto.csv" \
        -F "overwrite=true" \
        https://dbc-052187db-41bc.cloud.databricks.com/api/2.0/dbfs/put
        """
    )

    clean_old_table = BashOperator(
        task_id="clean_old_table",
        bash_command = f"""
        curl -n -X POST -H "Authorization: Bearer {DATABRICKS_TOKEN}" \
        -H "Content-Type: application/json" \
        -d '{{ \
            "warehouse_id": "6410db1b05447f4d", \
            "statement": "DROP TABLE IF EXISTS crypto.default.crypto_raw;" \
        }}' \
        https://dbc-052187db-41bc.cloud.databricks.com/api/2.0/sql/statements       
        """
    )

    create_empty_table = BashOperator(
        task_id="create_empty_table",
        bash_command = f"""
        curl -n -X POST -H "Authorization: Bearer {DATABRICKS_TOKEN}" \
        -H "Content-Type: application/json" \
        -d '{{ \
            "warehouse_id": "6410db1b05447f4d", \
            "statement": "CREATE TABLE IF NOT EXISTS crypto.default.crypto_raw USING DELTA;" \
        }}' \
        https://dbc-052187db-41bc.cloud.databricks.com/api/2.0/sql/statements
        """
    )

    copy_data_to_table = BashOperator(
        task_id="copy_data_to_table",
        bash_command=f"""
        curl -n -X POST -H "Authorization: Bearer {DATABRICKS_TOKEN}" \
        -H "Content-Type: application/json" \
        -d '{{
            "warehouse_id": "6410db1b05447f4d",
            "statement": "COPY INTO crypto.default.crypto_raw FROM \\"dbfs:/crypto/crypto.csv\\" FILEFORMAT = CSV COPY_OPTIONS (\\"mergeSchema\\" = \\"true\\");"
        }}' \
        https://dbc-052187db-41bc.cloud.databricks.com/api/2.0/sql/statements
        """
    )

    dbt_source_check = BashOperator(
        task_id="dbt_source_freshness",
        bash_command="dbt source freshness"
    )

    dbt_build = BashOperator(
        task_id="perform_dbt_transformation_and_tests",
        bash_command="dbt build"
    )

    clean_old_table >> create_empty_table
    pull_data >> [upload_file, create_empty_table] >> copy_data_to_table >> dbt_source_check >> dbt_build