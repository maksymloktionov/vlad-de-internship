import psycopg2 as ps
import bs4
import pandas as pd
import requests
import os
import logging
from dotenv import load_dotenv

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')
load_dotenv()

class Webscrapper:

    def __init__(self, url: str) -> None:
        self.url = url

    @staticmethod
    def _start_connections() -> ps.extensions.connection:
        try:
            connection = ps.connect(
                host = os.getenv('DB_HOST'),
                port = os.getenv('DB_PORT'),
                dbname = os.getenv('DB_NAME'),
                password = os.getenv('PASSWORD'),
                user = os.getenv('DB_USER')
            )

            return connection
        except Exception as e:
            logging.info(f"Error: {e}")

    @staticmethod
    def _get_data(url: str) -> list[tuple[str, str, str]]:
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

        return res
    
    def _construct_df(self) -> pd.DataFrame:
        site_data = self._get_data(self.url)

        dict_data = {
            "Date": [f"{date} 2000" for date, _, _ in site_data],
            "Name": [name for _, name, _ in site_data],
            "Info": [info for _, _, info in site_data],
        }

        df = pd.DataFrame.from_dict(dict_data)

        return df
    
    def website_data_to_db(self) -> None:
        try:
            connection = self._start_connections()
            df = self._construct_df()

            cursor = connection.cursor()

            cursor.execute("""CREATE TABLE IF NOT EXISTS public.Sites ( 
                    id INT PRIMARY KEY,
                    date VARCHAR(32),
                    name VARCHAR(50),
                    content TEXT
               )""")
    
            connection.commit()

            for i, row in df.iterrows():
                cursor.execute("""
                    INSERT INTO public.Sites (id, date, name, content) 
                    VALUES (%s, %s, %s, %s) 
                    ON CONFLICT (id) DO NOTHING
                    """, (i, row['Date'], row['Name'], row['Info']))
                connection.commit()

            logging.info("Data has been successfully moved")

            cursor.close()
            connection.close()
            
        except Exception as e:
            logging.info(f"Error: {e}")

if __name__ == "__main__":

    webscrp = Webscrapper("https://uk.wikipedia.org/wiki/2000")

    webscrp.website_data_to_db()