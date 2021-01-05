import pyaudio
import wave
import speech_recognition as sr
import deepspeech
import wave
import numpy as np
import os
from pydub import AudioSegment
from pydub.silence import split_on_silence
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

def similarity_index_history(data):
    X =data
    Y="show previous history"
    X_list = word_tokenize(X)                                                                                               Y_list = word_tokenize(Y)
    sw = stopwords.words('english')
    l1 =[];l2 =[]

# remove stop words from the string
    X_set = {w for w in X_list if not w in sw}
    Y_set = {w for w in Y_list if not w in sw}
    print(X_set)
    print(Y_set)

# form a set containing keywords of both strings
    rvector = X_set.intersection(Y_set)

    #rvector.add("give")
    rvector.add("display")

    #rvector = X_set.intersection(Y_set)
    print("vectorr=", rvector)

#rvector = X_set.union(Y_set)
    for w in rvector:
        if w in X_set: l1.append(1) # create a vector
        else: l1.append(0)
        if w in Y_set: l2.append(1)
        else: l2.append(0)
    c = 0
    print(l1)
    print(l2)
    
# cosine formula
    try:
        for i in range(len(rvector)):
            c+= l1[i]*l2[i]
        cosine = c / float((sum(l1)*sum(l2))**0.5)
        print("similarity: ", cosine)
        return cosine
    except:
        similarity = 0.0
        return similarity

 # Program to measure the similarity between
# two sentences using cosine similarity.
def similarity_index_prescription():
    
# Program to measure the similarity between
# two sentences using cosine similarity.

#list1 = ["prescription", "write", "note", "down", "take"]
#list2 = "make a note of it"
#Y_list = [word for line in list2 for word in line.split()]
#list_2 = word_tokenize(list2)
#print(list_2)
#orderedsets = list(set(list1).intersection(list_2))

# X = input("Enter first string: ").lower()
# Y = input("Enter second string: ").lower()
    X =data
    Y="write prescription"
#Y =['note down prescription ', 'write prescription ', 'make a note of prescription ']
#Y=["prescription"]
# tokenization
    X_list = word_tokenize(X)
    Y_list = word_tokenize(Y)
#Y_list = [sub.split() for sub in Y]
#Y_list = [word for line in Y for word in line.split()]
#print(orderedsets)#Y_list = [sub.split() for sub in Y]
#Y_list = [word for line in Y for word in line.split()]
#print(orderedsets)
#print(Y_list)                                                                                                          
# sw contains the list of stopwords
    sw = stopwords.words('english')
    l1 =[];l2 =[]

# remove stop words from the string
    X_set = {w for w in X_list if not w in sw}
    Y_set = {w for w in Y_list if not w in sw}
    print(X_set)
    print(Y_set)

# form a set containing keywords of both strings
    rvector = X_set.intersection(Y_set)
    rvector.add("write")
    rvector.add("note")

#rvector = X_set.intersection(Y_set)
    print("vectorr=", rvector)

#rvector = X_set.union(Y_set)
    for w in rvector:
        if w in X_set: l1.append(1) # create a vector
        else: l1.append(0)
        if w in Y_set: l2.append(1)
        else: l2.append(0)
    c = 0
    print(l1)
    print(l2)

# cosine formula
    try:
        for i in range(len(rvector)):
            c+= l1[i]*l2[i]
        cosine = c / float((sum(l1)*sum(l2))**0.5)
        print("similarity: ", cosine)
        return cosine
    except:
        similarity = 0.0
        return similarity


#audio file to text conversion
def split(input_path):
  print ("Start cutting")
  sound = AudioSegment.from_wav(input_path)

  chunks = split_on_silence(sound, 
    # must be silent for at least half a second
    min_silence_len = 500,
    # consider it silent if quieter than -50 dBFS
    silence_thresh = -30
  )

  # export the chunk
  # i for the output file count
  i = 0
  data_store = []
  slash_index = input_path.rfind("/") + 1
  filename = input_path[slash_index: -4]
  print(filename)
  for i, chunk in enumerate(chunks):
    chunk.export("{name}{count}.wav".format(
      name=filename, 
      count=i), format="wav")
    names = filename + str(i) + '.wav'
    print(names)
    #deepspeech recognition
    w = wave.open(names, 'r')
    rate = w.getframerate()
    frames2 = w.getnframes()
    buffer = w.readframes(frames2)
    print(rate)

    print(model.sampleRate())

    type(buffer)
   
    data16 = np.frombuffer(buffer, dtype=np.int16)
    type(data16)
    text = model.stt(data16)
    print(text)
    w.close()
    data_store.append(text)
    if os.path.exists(names):
        os.remove(names)
    else:
        print("The file does not exist")
     
    
  print ('There are splited into {number} files'.format(number=i + 1))
  print("resultant array is==", data_store)

  length = len(data_store)

  #history command handler
  for data in data_store:
    print(data)
    if(similarity_index_history(data) >= 0.5):
        #indx = data_store.index(data)
        print("history command")

  #prescription command handler
  for data in data_store:
    print(data)
    if(similarity_index_prescription(data) >= 0.5):
        indx = data_store.index(data)
        print("prescription command")
        for presc in range(indx, length):
            print(data_store[presc])
  
        break;
    break;

  os.remove(output.wav)
  return i + 1


#audio recording function
def audio_recording():
    try:
        p = pyaudio.PyAudio()
        stream = p.open(format=FORMAT,
                        channels=CHANNELS,
                        rate=RATE,
                        input=True,
                        frames_per_buffer=CHUNK)

        print("* recording")

    
        while 1:
            data = stream.read(CHUNK)
            frames.append(data)
    except:
        print("* done recording")

        stream.stop_stream()
        stream.close()
        p.terminate()
    
    #Write content to file
    
        wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(p.get_sample_size(FORMAT))
        wf.setframerate(RATE)
        wf.writeframes(b''.join(frames))
        wf.close()
        split(WAVE_OUTPUT_FILENAME)

        
CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 16000
#RECORD_SECONDS = 20

WAVE_OUTPUT_FILENAME = "output.wav"
model_file_path = 'deepspeech-0.6.0-models/output_graph.pbmm'
beam_width = 500
model = deepspeech.Model(model_file_path, beam_width)
lm_file_path = 'deepspeech-0.6.0-models/lm.binary'
trie_file_path = 'deepspeech-0.6.0-models/trie'
lm_alpha = 0.75
lm_beta = 1.85
model.enableDecoderWithLM(lm_file_path, trie_file_path, lm_alpha, lm_beta)

