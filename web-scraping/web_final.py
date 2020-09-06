from bs4 import BeautifulSoup
import requests
import mysql.connector
source = requests.get('https://www.medicalnewstoday.com/').text
soup= BeautifulSoup(source,'lxml')
article=soup.find('div',{"id":"LATEST NEWS"})
def extract_source(url):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:50.0) Gecko/20100101 Firefox/50.0'}
    source=requests.get(url, headers=headers).text
    return source
source1=extract_source('https://www.hindustantimes.com/health/')
soup1= BeautifulSoup(source1,'lxml')

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
   ''' sql = """CREATE TABLE IF NOT EXISTS scrape_final(
        headline mediumtext,
        summary mediumtext,
        links mediumtext
        )
    """
    mycursor.execute(sql)


    #Reading from Database
    mycursor.execute("SELECT * FROM scrape_final")
    rows = mycursor.fetchall()
    print (rows)'''
for link in article.find_all('a',class_="css-ni2lnp"):
        headline=link.text
        summary="none"
        link='https://www.medicalnewstoday.com'+link["href"]

    #Inserting into Database
        sql = ("INSERT INTO scrape_final (headline,summary,links ) values (%s, %s, %s)") 
        data = (headline,summary,link)

        mycursor.execute(sql, data)
      # Changes are not commited until you put this, so testing ke liye nikal ke try kar sakte ho.
        print(mycursor.rowcount, "record inserted.")


for article in soup1.find_all('div',class_="media-heading headingfour"):
        link=article.a.text
        r=article.a
        summary="none"
        sql = ("INSERT INTO scrape_final (headline,summary,links ) values (%s, %s, %s)") 
        data = (link,summary,r)
        mycursor.execute(sql, data)
        print(mycursor.rowcount, "record inserted.")
mydb.commit()  

database_connect()


