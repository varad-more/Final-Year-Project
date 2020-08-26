from bs4 import BeautifulSoup
import requests
import mysql.connector

# pip3 install mysql-connector-python 

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="",
  database="web_scraping" # Change as per requirements
)

mycursor = mydb.cursor()



def database_connect():

    # Creates Table if not exist
    sql = """CREATE TABLE IF NOT EXISTS scraper(
        headline varchar (40),
        summary varchar (500),
        links varchar(40)
        )
    """
    mycursor.execute(sql)


    #Reading from Database
    mycursor.execute("SELECT * FROM scraper")
    rows = mycursor.fetchall()
    print (rows)

    #Inserting into Database
    sql = ("INSERT INTO scraper (headline,summary,links ) values (%s, %s, %s)") 
    data = (headline,summary,links)

    mycursor.execute(sql, data)
    mydb.commit()  # Changes are not commited until you put this, so testing ke liye nikal ke try kar sakte ho.
    print(mycursor.rowcount, "record inserted.")



source1 = requests.get('https://www.medicalnewstoday.com/').text
soup1= BeautifulSoup(source1,'lxml')
article=soup1.find('div',{"id":"LATEST NEWS"})

for link in article.find_all('a',class_="css-ni2lnp"):
    headline=link.text
    link='https://www.medicalnewstoday.com'+link["href"]
    summary='none'
    database_connect()

def extract_source(url):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:50.0) Gecko/20100101 Firefox/50.0'}
    source=requests.get(url, headers=headers).text
    return source
          
def extract_data(source):
    soup= BeautifulSoup(source,'lxml')
    for article in soup.find_all('div',class_="media-heading headingfour"):
      headline=article.a.text
      summary='none'
      link=r['href']
      database_connect()
extract_data(extract_source('https://www.hindustantimes.com/health/'))
