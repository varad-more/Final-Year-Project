import speech_recognition as sr
r = sr.Recognizer()
m = sr.Microphone()

def strlist(s):
	print("following is the list")
	for st in s:
			print(st)

try:
	s = list()
	for a in range(5):

		with m as source: 
			r.adjust_for_ambient_noise(source)
			print("Set minimum energy threshold to {}".format(r.energy_threshold))
			print("Say something!") 
			audio = r.listen(source)
			text = r.recognize_google(audio)
			print('{}'.format(text))
			y="{}".format(text)
			s.append(y)
			

        
except sr.UnknownValueError:
    print("Oops! Didn't catch that")
except sr.RequestError as e:
    print("Uh oh! Couldn't request results from Google Speech Recognition service; {0}".format(e))    	
except KeyboardInterrupt:
    pass
strlist(s)