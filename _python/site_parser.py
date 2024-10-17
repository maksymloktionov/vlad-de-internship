import psycopg2 as ps
import bs4
import pandas as pd
import requests
import os
import logging
from sqlalchemy import create_engine

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')

class Webscrapper:

    def __init__(self, url: str) -> None:
        logging.info("Script started")
        self.url = url


    @staticmethod
    def _start_connections() -> ps.extensions.connection:
        try:
            engine = create_engine(f"postgresql+psycopg2://{os.getenv('DB_USER')}:{os.getenv('PASSWORD')}@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}")
            return engine
        except Exception as e:
            logging.exception(f"Error: {e}")

    @staticmethod
    def _get_data(url: str) -> list[tuple[str, str, str]]:
        try:
            content = requests.request("get", url)
            soup = bs4.BeautifulSoup(content.text, "html.parser")

            all_lists = soup.find_all('ul', id="", recursive=True)
            res = []

            for ele in all_lists:
                if not ele.get('class') and len(ele) == 21:
                    text_list = ele.text.replace("\xa0", "").split("\n")

            for line in text_list:
                splitted = line.split("— ")
                splitter = splitted[1].index(",")

                res.append((splitted[0], splitted[1][:splitter], splitted[1][splitter+2:]))

            logging.info(f"Data has been succesfully parsed from {url}")

            return res
        except Exception as e:
            logging.exception(f"During execution {e} ocurred")
    
    def _construct_df(self) -> pd.DataFrame:
        try:
            site_data = self._get_data(self.url)

            dict_data = {
                "Date": [f"{date} 2000" for date, _, _ in site_data],
                "Name": [name for _, name, _ in site_data],
                "Info": [info for _, _, info in site_data],
            }

            df = pd.DataFrame.from_dict(dict_data)

            logging.info("Data has been succesfully moved to DataFrame")

            return df
        except Exception as e:
            logging.exception(f"During execution {e} ocurred")
    
    def website_data_to_db(self) -> None:
        try:
            df = self._construct_df()
            engine = self._start_connections()

            df.to_sql('Sites', engine, if_exists='replace', index_label='id')

            logging.info("Data has been successfully loaded")
            
        except Exception as e:
            logging.info(f"Error: {e}")

if __name__ == "__main__":

    webscrp = Webscrapper("https://uk.wikipedia.org/wiki/2000")

    webscrp.website_data_to_db()