import pyaudio
import wave
import speech_recognition as sr
import os
from pydub import AudioSegment
from pydub.silence import split_on_silence


def split(input_path):
    print("Start cutting")
    sound = AudioSegment.from_wav(input_path)

    i = 0
    data_store = []
    slash_index = input_path.rfind("/") + 1
    filename = input_path[slash_index: -4]
    print(filename)

    chunks = split_on_silence(sound,
                              # must be silent for at least half a second
                              min_silence_len=300,
                              # consider it silent if quieter than -50 dBFS
                              silence_thresh=-40
                              )
    print (chunks)
    # export the chunk
    # i for the output file count

    files = []
    for i, chunk in enumerate(chunks):
        chunk.export("{name}{count}.wav".format(
            name=filename,
            count=i), format="wav")
        names = filename + str(i) + '.wav'
        print(names)
        files.append(names)
        r = sr.Recognizer()
        with sr.AudioFile(names) as source:
            audio_text = r.listen(source)
        try:

            # using google speech recognition
            text = r.recognize_google(audio_text)
            print('Converting audio transcripts into text ...')
            print(text)
            data_store.append(text)
            print(names)

            if os.path.exists(names):
                os.remove(names)
            else:
                print("The file does not exist")

        except:
            print('Sorry.. run again...')
            continue
        i = i+1

        print (files)
        data_store.append(text)
       # print("name", dir + name + '_' + str(count))
    print('There are splited into {number} files'.format(number=i + 1))
    print("resultant array is==", data_store)

    resultant = ' '
    return resultant.join(data_store)
    # return data_store

#   os.remove(output.wav)
#   return i + 1
'''

# importing libraries 
import speech_recognition as sr 
  
import os 
  
from pydub import AudioSegment 
from pydub.silence import split_on_silence 
  
# a function that splits the audio file into chunks 
# and applies speech recognition 
def split(path): 
  
    # open the audio file stored in 
    # the local system as a wav file. 
    song = AudioSegment.from_wav(path) 
  
    # open a file where we will concatenate   
    # and store the recognized text 
    fh = open("recognized.txt", "w+") 
          
    # split track where silence is 0.5 seconds  
    # or more and get chunks 
    chunks = split_on_silence(song, 
        # must be silent for at least 0.5 seconds 
        # or 500 ms. adjust this value based on user 
        # requirement. if the speaker stays silent for  
        # longer, increase this value. else, decrease it. 
        min_silence_len = 500, 
  
        # consider it silent if quieter than -16 dBFS 
        # adjust this per requirement 
        silence_thresh = -16
    ) 
  
    # create a directory to store the audio chunks. 
    try: 
        os.mkdir('audio_chunks') 
    except(FileExistsError): 
        pass
  
    # move into the directory to 
    # store the audio files. 
    os.chdir('audio_chunks') 
  
    i = 0
    # process each chunk 
    for chunk in chunks: 
              
        # Create 0.5 seconds silence chunk 
        chunk_silent = AudioSegment.silent(duration = 10) 
  
        # add 0.5 sec silence to beginning and  
        # end of audio chunk. This is done so that 
        # it doesn't seem abruptly sliced. 
        audio_chunk = chunk_silent + chunk + chunk_silent 
  
        # export audio chunk and save it in  
        # the current directory. 
        print("saving chunk{0}.wav".format(i)) 
        # specify the bitrate to be 192 k 
        audio_chunk.export("./chunk{0}.wav".format(i), bitrate ='192k', format ="wav") 
  
        # the name of the newly created chunk 
        filename = 'chunk'+str(i)+'.wav'
  
        print("Processing chunk "+str(i)) 
  
        # get the name of the newly created chunk 
        # in the AUDIO_FILE variable for later use. 
        file = filename 
  
        # create a speech recognition object 
        r = sr.Recognizer() 
  
        # recognize the chunk 
        with sr.AudioFile(file) as source: 
            # remove this if it is not working 
            # correctly. 
            r.adjust_for_ambient_noise(source) 
            audio_listened = r.listen(source) 
  
        try: 
            # try converting it to text 
            rec = r.recognize_google(audio_listened) 
            # write the output to the file. 
            fh.write(rec+". ") 
  
        # catch any errors. 
        except sr.UnknownValueError: 
            print("Could not understand audio") 
  
        except sr.RequestError as e: 
            print("Could not request results. check your internet connection") 
'''
  
