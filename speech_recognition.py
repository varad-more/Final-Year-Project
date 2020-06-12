import pymongo
import datetime
import speech_recognition as sr 
import pyttsx3
#text to speech speaking
'''def Speak(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()'''
    
def demodatabase(s):
    client =  pymongo.MongoClient('mongodb://localhost:27017/')
    db = client['speechdb'] #database name
    mycol = db["prescription"]#collection list 
    print (mycol)
    collist = db.list_collection_names()
    if "prescription" in collist:
          print("The collection exists.")
    #b=s[0];c=s[1];d=s[2];e=s[3];f=s[4];
    
    post = {"name": s}
    x = mycol.insert_one(post)
    print(x)
    

# Initialize the recognizer  

r = sr.Recognizer()
m = sr.Microphone()
#s = list()

def talk():
    try:
    #s = list()
        x="yes"
        while(x!="no"):
            with m as source: 
                r.adjust_for_ambient_noise(source)
                print("Set minimum energy threshold to {}".format(r.energy_threshold))
                print("Say something!") 
                audio = r.listen(source)
                text = r.recognize_google(audio)
                print('{}'.format(text))
                y = "{}".format(text)
            #s.append(y)
            demodatabase(y)
        
            with m as source2:
                print("want to say something YES/NO:")
                audio2 = r.listen(source2)
                text2 = r.recognize_google(audio2)
                print(text2)
                x=text2
    
    
            #connect_database()
    except sr.UnknownValueError:
        print("Oops! Didn't catch that....speek from first")
        talk()
    except sr.RequestError as e:
        print("Uh oh! Couldn't request results from Google Speech Recognition service; {0}".format(e))      
    except KeyboardInterrupt:
        pass

talk()



 

