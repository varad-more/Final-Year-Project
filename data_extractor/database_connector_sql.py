import mysql.connector

# pip3 install mysql-connector-python 

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="",
  database="virtual_managers" # Change as per requirements
)

mycursor = mydb.cursor()



def database_connect():

    # Creates Table if not exist
    # sql = """CREATE TABLE IF NOT EXISTS dashboard_reports(
    #     name varchar (20),
    #     gender varchar (6),
    #     age int,
    #     date varchar (15),
    #     normal varchar (100),
    #     abnormal varchar (100),
    #     notes varchar (100)
    #     )
    # """
    # mycursor.execute(sql)


    #Reading from Database
    mycursor.execute("SELECT * FROM dashboard_reports")
    rows = mycursor.fetchall()
    print (rows)

    #Inserting into Database
    sql = ("INSERT INTO dashboard_reports (name, gender, age, date, normal, abnormal, notes ) values (%s, %s, %s, %s, %s, %s, %s)") 
    data = ('Test','Male','18','2020-02-01','abc', 'xyz','test')
    mycursor.execute(sql, data)
    mydb.commit()  # Changes are not commited until you put this, so testing ke liye nikal ke try kar sakte ho.
    print(mycursor.rowcount, "record inserted.")

database_connect()

