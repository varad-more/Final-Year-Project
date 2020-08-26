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
    data = ("2","abc","def")

    mycursor.execute(sql, data)
    mydb.commit()  # Changes are not commited until you put this, so testing ke liye nikal ke try kar sakte ho.
    print(mycursor.rowcount, "record inserted.")

database_connect()
