import bs4
import csv
import mysql.connector

from bs4 import BeautifulSoup as soup
from urllib.request import urlopen


mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="",
  database="web_scraping" # Change as per requirements
)


news_url="https://news.google.com/news/rss"
Client=urlopen(news_url)
xml_page=Client.read()
Client.close()

soup_page=soup(xml_page,"xml")
news_list=soup_page.findAll("item")
# Print news title, url and publish date
for news in news_list:
	headline=news.title.text
	summary=news.pubDate.text
	link1=news.link.text
	csv_writer.writerow([headline, summary,link1])


def database_connect():

    # Creates Table if not exist
    sql = """CREATE TABLE IF NOT EXISTS reports(
        name varchar (20),
        gender varchar (6),
        age int,
        date varchar (15),
        normal varchar (100),
        abnormal varchar (100),
        notes varchar (100)
        )
    """
    mycursor.execute(sql)


    #Reading from Database
    mycursor.execute("SELECT * FROM reports")
    rows = mycursor.fetchall()
    print (rows)

    #Inserting into Database
    sql = ("INSERT INTO scraper (headline,summary,links ) values (%s, %s, %s)") 
    data = ("2","abc","def")
    data = ('Test','Male','18','2020-02-01','abc', 'xyz','test')
    mycursor.execute(sql, data)
    mydb.commit()  # Changes are not commited until you put this, so testing ke liye nikal ke try kar sakte ho.
    print(mycursor.rowcount, "record inserted.")

database_connect()
