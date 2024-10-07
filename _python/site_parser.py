import psycopg2 as ps
import bs4
import pandas as pd
import requests

class Webscrapper:

    def __init__(self, url: str) -> None:
        self.url = url

    def __start_connections(self) -> ps.extensions.connection:
        try:
            connection = ps.connect(
                host = "db",
                port = "5432",
                dbname = "postgres",
                password = "1234",
                user = "postgres"
            )

            return connection
        except Exception as e:
            print(f"Error: {e}")

    def __get_data(self) -> list[tuple[str, str, str]]:
        content = requests.request("get", self.url)
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
    
    def __construct_df(self) -> pd.DataFrame:
        site_data = self.__get_data()

        dict_data = {
            "Date": [ele[0] + ' 2000' for ele in site_data],
            "Name": [ele[1] for ele in site_data],
            "Info": [ele[2] for ele in site_data],
        }

        df = pd.DataFrame.from_dict(dict_data)

        return df
    
    def website_data_to_db(self) -> None:
        try:
            connection = self.__start_connections()
            df = self.__construct_df()

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

            print("Done")

            cursor.close()
            connection.close()
            
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":

    webscrp = Webscrapper("https://uk.wikipedia.org/wiki/2000")

    webscrp.website_data_to_db()


