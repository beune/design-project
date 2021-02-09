#!/usr/bin/env python3

# NOTE: this example requires PyAudio because it uses the Microphone class
import time
from threading import Thread
from queue import Queue  # Python 3 import
# except ImportError:
#     from Queue import Queue  # Python 2 import
import pyaudio
import wave

import speech_recognition as sr

CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
RECORD_SECONDS = 4
p = pyaudio.PyAudio()
WAVE_OUTPUT_FILENAME = "_testing_file.wav"
r = sr.Recognizer()
audio_queue = Queue()

class Queuespeech:

    def __init__(self):
        self.frames = []

    def listen_and_chop(self):
        stream = p.open(format=FORMAT,
                        channels=CHANNELS,
                        rate=RATE,
                        input=True,
                        frames_per_buffer=CHUNK)
        while True:
            # print("* recording new round")
            for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
                data = stream.read(CHUNK)
                self.frames.append(data)



    def recognize_worker(self):
        # this runs in a background thread
        while True:
            frame_data = b"".join(self.frames)  # retrieve the next audio processing job from the main thread
            audio = sr.AudioData(frame_data, RATE, p.get_sample_size(FORMAT))
            if audio is None:
                print("no audio")# stop processing if the main thread is done
            else:

                # received audio data, now we'll recognize it using Google Speech Recognition
                try:
                    # for testing purposes, we're just using the default API key
                    # to use another API key, use `r.recognize_google(audio, key="GOOGLE_SPEECH_RECOGNITION_API_KEY")`
                    # instead of `r.recognize_google(audio)`
                    print(r.recognize_google(audio, language="nl-NL"))
                except sr.UnknownValueError:
                    # print("Google Speech Recognition could not understand audio")
                    pass
                except sr.RequestError as e:
                    print("Could not request results from Google Speech Recognition service; {0}".format(e))
            time.sleep(0.25)

    def startup(self):
        # start a new thread to recognize audio, while this thread focuses on listening
        listen_thread = Thread(target=self.listen_and_chop)
        listen_thread.start()
        recognize_thread = Thread(target=self.recognize_worker)
        recognize_thread.daemon = True
        recognize_thread.start()
        # with sr.Microphone() as source:
        #     try:
        #         while True:  # repeatedly listen for phrases and put the resulting audio on the audio processing job queue
        #             audio_queue.put(r.listen(source))
        #     except KeyboardInterrupt:  # allow Ctrl + C to shut down the program
        #         pass
        recognize_thread.join()  # wait for the recognize_thread to actually stop

if __name__ == "__main__":
    qs = Queuespeech()
    qs.startup()
