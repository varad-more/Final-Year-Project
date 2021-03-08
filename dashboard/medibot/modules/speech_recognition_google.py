import pyaudio
import wave
import speech_recognition as sr
import os
from pydub import AudioSegment
from pydub.silence import split_on_silence


def split(input_path):
    print("Start cutting")
    sound = AudioSegment.from_wav(input_path)

    chunks = split_on_silence(sound,
                              # must be silent for at least half a second
                              min_silence_len=700,
                              # consider it silent if quieter than -50 dBFS
                              silence_thresh=-60
                              )

    # export the chunk
    # i for the output file count
    i = 0
    data_store = []
    slash_index = input_path.rfind("/") + 1
    filename = input_path[slash_index: -4]
    print(filename)
    files = []
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
            print(names)

            if os.path.exists(names):
                os.remove(names)
            else:
                print("The file does not exist")

        except:
            print('Sorry.. run again...')
            continue

        data_store.append(text)
       # print("name", dir + name + '_' + str(count))
    print('There are splited into {number} files'.format(number=i + 1))
    print("resultant array is==", data_store)

    resultant = ' '
    return resultant.join(data_store)

#   os.remove(output.wav)
#   return i + 1
