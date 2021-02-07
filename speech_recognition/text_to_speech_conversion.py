import speech_recognition as sr
import pymongo
import pyttsx3
import csv

rows=[]
p=" "
with open("patient1.csv", 'r') as csvfile: 
    # creating a csv reader object 
    csvreader = csv.reader(csvfile) 
      
    # extracting field names through first row 
    fields = next(csvreader) 
  
    # extracting each data row one by one 
    for row in csvreader: 
        rows.append(row)	
    engine = pyttsx3.init()
    engine.say(rows)    
    engine.runAndWait()
    for i in range(len(rows)):
        	p=rows[i]
        	print("medicine ",i,":",p)