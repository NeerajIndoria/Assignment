import requests
from bs4 import BeautifulSoup
from datetime import date
import pandas
import sqlite3

SITE = "https://www.theverge.com/"
today = date.today().strftime("%d%m%y")
TITLE = f"{today}_verge.csv"


def data_to_db():
    con = sqlite3.connect('information.db')
    cur = con.cursor()
    cur.execute("create table if not exists verge_data(id integer primary key,url text,headlines text,author text,date text)")

    datax = pandas.read_csv(TITLE)
    datax.to_sql('verge_data', con, if_exists='replace', index=False)
    con.commit()

    cur.execute("select * from verge_data")
    records = cur.fetchall()
    for row in records:
        print(row)

    con.close()


response = requests.get(SITE)
web_html = response.text
soup = BeautifulSoup(web_html, "html.parser")

headlines = [headline.get_text("h2") for headline in soup.find_all(name="li", class_='pb-20 last:pb-0 mb-20 last:mb-0 '
                                                                                     'text-franklin last'
                                                                                     ':border-0 border-b '
                                                                                     'lg:last:mb-20 lg:w-[300px] '
                                                                                     'border-b-franklin')]
links = [f"{SITE}{link.get('href')}" for link in soup.find_all(name='a', class_='text-white hover:text-franklin')]
authors = [author.text for author in soup.find_all(name="span", class_="mr-8 text-gray-ef")]
dates = [date.get_text("span") for date in soup.find_all(name="li", class_='pb-20 last:pb-0 mb-20 last:mb-0 text-'
                                                                           'franklin last:border-0 border-b lg:last:mb'
                                                                           '-20 lg:w-[300px] border-b-franklin')]
ids = [i for i in range(len(headlines))]

data_dict = {
    "id": ids,
    "url": links,
    "headline": headlines,
    "author": authors,
    "date": dates,
}

data = pandas.DataFrame(data_dict)
# print(data)
data.to_csv(TITLE)
data_to_db()
