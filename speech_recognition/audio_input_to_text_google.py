import pyaudio
import wave
import speech_recognition as sr
import os
from pydub import AudioSegment
from pydub.silence import split_on_silence

def split(input_path):
  print ("Start cutting")
  sound = AudioSegment.from_wav(input_path)

  chunks = split_on_silence(sound, 
    # must be silent for at least half a second
    min_silence_len = 700,
    # consider it silent if quieter than -50 dBFS
    silence_thresh = -60
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
    r = sr.Recognizer()
    with sr.AudioFile(names) as source:
        audio_text = r.listen(source)
    try:
        
        # using google speech recognition
        text = r.recognize_google(audio_text)
        print('Converting audio transcripts into text ...')
        print(text)
        data_store.append(text)
        '''if os.path.exists(names):
            os.remove(names)
        else:
            print("The file does not exist")'''
     
    except:
         print('Sorry.. run again...')
    data_store.append(text) 
   # print("name", dir + name + '_' + str(count))
  print ('There are splited into {number} files'.format(number=i + 1))
  print("resultant array is==", data_store)
  os.remove(output.wav)
  return i + 1
  
CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 16000
RECORD_SECONDS = 5
WAVE_OUTPUT_FILENAME = "output.wav"
try:
    p = pyaudio.PyAudio()

    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK)

    print("* recording")

    frames = []
    while 1:
        #for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
        data = stream.read(CHUNK)
        frames.append(data)
except:
    print("* done recording")

    stream.stop_stream()
    stream.close()
    p.terminate()
    #print(frames)
    '''audio_text = r.listen(frames)
    
# recoginize_() method will throw a request error if the API is unreachable, hence using exception handling
    try:
        
        # using google speech recognition
        text = r.recognize_google(audio_text)
        print('Converting audio transcripts into text ...')
        print(text)
     
    except:
         print('Sorry.. run again...')'''
    wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(p.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))
    wf.close()
    split('output.wav')