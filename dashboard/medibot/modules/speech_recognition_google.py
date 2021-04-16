import pyaudio
import wave
import speech_recognition as sr
import os
from pydub import AudioSegment
from pydub.silence import split_on_silence

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

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
        chunk.export(BASE_DIR+"/media/{name}{count}.wav".format(
            name=filename,
            count=i), format="wav")
        names = BASE_DIR + "/media/" + filename + str(i) + '.wav'
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
            if os.path.exists(names):
                os.remove(names)
            print('Sorry.. run again...')
            continue
        i = i+1

        print ('file',files)
        ## Incase there is error in file deletion
        # for file in files:
        #     os.remove(file)

    print('There are splited into {number} files'.format(number=i + 1))
    print("resultant array is==", data_store)

    resultant = ' '
    return resultant.join(data_store)
