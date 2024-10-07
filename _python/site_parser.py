import psycopg2 as ps
import bs4
import pandas as pd
import requests

def website_to_df(): 
    url = "https://uk.wikipedia.org/wiki/2000"
    content = requests.request("get", url)
    soup = bs4.BeautifulSoup(content.text, 'html.parser')

    all_lists = soup.find_all('ul', id="",recursive=True)
    res = []

    for ele in all_lists:
        if not ele.get('class') and len(ele) == 21:
            text_list = ele.text.replace("\xa0", "").split("\n")

    for line in text_list:
        splitted = line.split("— ")
        splitter = splitted[1].index(",")

        res.append((splitted[0], splitted[1][:splitter], splitted[1][splitter+2:]))

    dict_data = {
        "Date": [ele[0] + ' 2000' for ele in res],
        "Name": [ele[1] for ele in res],
        "Info": [ele[2] for ele in res],
    }

    df = pd.DataFrame.from_dict(dict_data)

    return df


df = website_to_df()

try:
    connection = ps.connect(
        host = "localhost",
        port = "5444",
        dbname = "postgres",
        password = "1234",
        user = "postgres"
    )

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

except Exception as e:
    print(e)


