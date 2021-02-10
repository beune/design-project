#!/usr/bin/env python3

import time
from threading import Thread
from queue import Queue  # Python 3 import
import pyaudio
import speech_recognition as sr

from utilities import combine, combine_word

CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
RECORD_SECONDS = 4
p = pyaudio.PyAudio()
WAVE_OUTPUT_FILENAME = "_testing_file.wav"
r = sr.Recognizer()
audio_queue = Queue()


class QueueSpeech:

    def __init__(self):
        self.frames = []
        self.text = ""
        self.flag = False
        self.complete_text = ""

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

    def recognize(self):
        last = 0
        window = 80
        delta = 35
        uncertain = window
        assert delta <= uncertain
        self.flag = True
        while self.flag:
            length = len(self.frames)
            upper = max(0, length - uncertain)
            # lower bound: last, upper bound: upper
            # take delta on both sides to keep context
            min_frame = max(0, last - delta)
            max_frame = min(upper + delta, length)
            frames = self.frames[min_frame:max_frame]
            data = b"".join(frames)
            audio = sr.AudioData(data, RATE, p.get_sample_size(FORMAT))
            try:
                self.text = combine_word(self.text, r.recognize_google(audio, language="nl-NL"))
                print("text: " + self.text)
            except sr.UnknownValueError:
                # print("Google Speech Recognition could not understand audio")
                print("text: " + self.text)
                pass
            except sr.RequestError as e:
                print("Could not request results from Google Speech Recognition service; {0}".format(e))
            last = upper  # (upper)
            time.sleep(2)
        self.stop()

    def stop(self):
        data = b"".join(self.frames)
        audio = sr.AudioData(data, RATE, p.get_sample_size(FORMAT))
        self.complete_text = r.recognize_google(audio, language="nl-NL")
        print(self.complete_text)
        print("End of transcription")

    def startup(self):
        # start a new thread to recognize audio, while this thread focuses on listening
        listen_thread = Thread(target=self.listen_and_chop)
        listen_thread.start()
        recognize_thread = Thread(target=self.recognize, daemon=True)
        recognize_thread.start()
        time.sleep(25)
        self.flag = False


if __name__ == "__main__":
    qs = QueueSpeech()
    qs.startup()
