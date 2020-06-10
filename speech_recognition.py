import pymongo
import datetime
import speech_recognition as sr 
import pyttsx3
#text to speech speaking
'''def Speak(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()'''
    
def demodatabase(y):
    client =  pymongo.MongoClient('mongodb://localhost:27017/')
    db = client['demodb'] #database name
    mycol = db["prescription"]#collection list 
    print (mycol)
    collist = db.list_collection_names()
    if "reports" in collist:
          print("The collection exists.")

    print("The collection exists.")
    post = {"name": y,
            "power": "500g",
            "time": datetime.datetime.utcnow()}
    x = mycol.insert_one(post)
    print(x)
    

# Initialize the recognizer  

r = sr.Recognizer()
m = sr.Microphone()
try:
    
    with m as source: 
        r.adjust_for_ambient_noise(source)
        print("Set minimum energy threshold to {}".format(r.energy_threshold))
        print("Say something!")
        audio = r.listen(source)
        text = r.recognize_google(audio)
        print('{}'.format(text))
        y = "{}".format(text)
        #Speak(text)
        demodatabase(y)
            #connect_database()
except sr.UnknownValueError:
    print("Oops! Didn't catch that")
except sr.RequestError as e:
    print("Uh oh! Couldn't request results from Google Speech Recognition service; {0}".format(e))      
except KeyboardInterrupt:
    pass




 

