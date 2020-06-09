import pymongo
import datetime
import speech_recognition as sr 
import pyttsx3

def Speak(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()
# Initialize the recognizer  
while(1):
    r = sr.Recognizer()  
    try:
        print("speek...")
        with sr.Microphone() as source:
    
            r.adjust_for_ambient_noise(source, duration=0.2) 
            audio = r.listen(source)
            text = r.recognize_google(audio)
            print("you spoke.... :{}".format(text)) 
            y = "{}".format(text)
            Speak(text)
            #connect_database()
    except:

        print("sorry we could no recognize your voice")


def connect_database():
    client =  pymongo.MongoClient('mongodb://localhost:27017/')
    db = client['demodb']
    mycol = db["prescription"]
    print (mycol)
    collist = db.list_collection_names()
    if "reports" in collist:
          print("The collection exists.")


    print(1)
    print("The collection exists.")
    print(2)
    post = {"name": y,
            "power": "500g",
            "time": datetime.datetime.utcnow()}
    print(3)
    x = mycol.insert_one(post)
    print(x)
    print(4)
    
connect_database()