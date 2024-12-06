import os
import sqlalchemy
import logging
import pandas as pd



logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')

DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")
PASSWORD = os.getenv("PASSWORD")
DB_USER = os.getenv("DB_USER")

class DataBaseManager:

    def __init__(self, user, port, name, password, host) -> None:
        self.user = user
        self.port = port
        self.host = host
        self.paswrd = password
        self.dbname = name
        
        logging.info("Class successfully initialized")

    def _load_data(self) -> None:
        try:
            path = "./data"
            dataframes = []
            files = os.listdir(path)

            for fpath in files:
                file_path = os.path.join(path, fpath)

                dataframes.append(pd.read_csv(file_path))

            self.shout_df, \
            self.res_df, \
            self.goalscor_df = dataframes

            logging.info("Data was successfully read")
        except Exception as e:
            logging.exception(f"Error: {e}")

    def _start_connections(self) -> sqlalchemy.Engine:
        try:
            engine = sqlalchemy.create_engine(
                f"postgresql+psycopg2://{self.user}:{self.paswrd}@{self.host}:{self.port}/{self.dbname}"
            )

            print(f"postgresql+psycopg2://{self.user}:{self.paswrd}@{self.host}:{self.port}/{self.dbname}")

            logging.info("Successfully connected to database")
            return engine
        except Exception as e:
            logging.exception(f"Error: {e}")

    def setup_schema(self):
        try:
            self._load_data()
            engine = self._start_connections()

            with engine.begin() as cursor:
                cursor.execute(
                    sqlalchemy.text(
                        """
                        CREATE SCHEMA IF NOT EXISTS raw
                        """
                    )
                )
                result = cursor.execute(sqlalchemy.text("SELECT schema_name FROM information_schema.schemata WHERE schema_name = 'raw'"))
                if result.rowcount == 0:
                    logging.error("Schema 'raw' was not created.")

            self.res_df.to_sql('results', engine, if_exists='replace', index_label='id', schema="raw")
            self.shout_df.to_sql('shootouts', engine, if_exists='replace', index_label='id', schema="raw")
            self.goalscor_df.to_sql('goalscorers', engine, if_exists='replace', index_label='id', schema="raw")

            logging.info("Data has been successfully moved to shema Raw")
        except Exception as e:
            logging.exception(f"Error: {e}")

if __name__ == "__main__":
    logging.info("Program starts")
    db_inst = DataBaseManager(DB_USER, DB_PORT, DB_NAME, PASSWORD, DB_HOST)
    db_inst.setup_schema()
    logging.info("Program ends")
