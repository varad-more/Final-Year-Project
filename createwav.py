import pyaudio
import wave
import speech_recognition as sr
import deepspeech
import wave
import numpy as np
import os
from pydub import AudioSegment
from pydub.silence import split_on_silence

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

  #history command
  history_list=['history', 'last history', 'previous data', 'background data', 'background history','past history']
  
  for data in data_store:
    res = any(ele in data for ele in prescription_list) 
    if(res==True):
        print("command = history")
        
            
  #prescription command
  prescription_list=['write a prescription', 'take down prescription', 'take a prescription', 'note down prescription', 'take prescription', 'write prescription', 'prescription please', 'prescription', 'like to suggest', 'would suggest to take', 'suggest', 'suggest some medicines']
  
  length = len(data_store)
  for data in data_store:
    res = any(ele in data for ele in prescription_list) 
    print(str(res))
    indx = data_store.index(data)
  # print(data)
    if(res==True):
        print("command = prescription")
        for presc in range(indx, length):
            print(data_store[presc])
  
        break;
  os.remove(output.wav)
  return i + 1

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

try:
    p = pyaudio.PyAudio()

    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK)

    print("* recording")

    
    while 1:
    #for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
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


