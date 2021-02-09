# import required modules 
import mysql.connector 
from datetime import date, timedelta
from mysql.connector import Error
import pyttsx3

def text_to_speech(speak_data_for_patient):
	#text to speech through pyttsx3
	engine = pyttsx3.init()

	# set speaking rate  
	engine.setProperty("rate", 150)  
	engine.say(speak_data_for_patient)
	engine.runAndWait()
	
def db_connect():
	try:
		# create connection object 
		con = mysql.connector.connect( 
 		 host="database-1.ctqvk0asvfes.us-east-1.rds.amazonaws.com",
  		user="admin",
 		password="Sakshi2399*",
  		database="virtual_managers") 
  
		# create cursor object 
		cursor = con.cursor() 
  
		# assign data query 
		query2 = """SELECT * FROM dashboard_patient_history
   		 WHERE
   		 patient_id = %s AND 
   		 date  
   		 BETWEEN %s AND %s;"""

		ID = 2
		#NAME ="abc"
		previous_date = "2020-9-20"
		 #= PREVIOUS_DATE.strftime("%Y-%m-%d")
		CURRENT_DATE =  date.today()
		current_date = CURRENT_DATE.strftime("%Y-%m-%d")
		

		# data variable with id, previous date, current date
		data = (ID,previous_date, current_date)

		# executing cursor 
		cursor.execute(query2,data) 
  
		# display all records 
		table = cursor.fetchall() 

		data_for_patient=" "

		#check for lenght of content in the table
		if (len(table)==0):
			print("invalid date or patient information") 
		else: 
			#fetch patient id, current dates and previous dates
			for getcontent in table:
				#fetch patient id
				id_patient = str(getcontent[1])

				data_of_patient =   id_patient, " for given patient past history is from date  ", previous_date," to ", current_date," is as follows\n "
			
				#tuple to string conversion
				data_of_patient =  ''.join(data_of_patient)
				print(data_of_patient)

				#call text_to_speech function
				text_to_speech(data_of_patient)
				break;

			# fetch all columns 
			for row in table:
				#get particular date from db
				get_date_from_db = row[2]
		
				#convert date to string
				dates = get_date_from_db.strftime("%Y-%m-%d")
		
				#sentence generation
				sentence_gen =  dates ," on this date the patient was suffering from symptoms like ", row[3], " for which he was given the prescriptions as ", row[4] ,"\n"
		
				#tuple to string conversion
				data_for_patient =  ''.join(sentence_gen)
				print(data_for_patient)

				#call text_to_speech function
				text_to_speech(data_for_patient)

		# closing cursor connection 
		cursor.close() 
	  
		# closing connection object 
		con.close()
	except mysql.connector.Error as error:
		print("Failed to create table in MySQL: {}".format(error))

db_connect()