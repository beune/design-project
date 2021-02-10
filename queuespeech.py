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
        self.text = ""
        self.processed = 0

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
            length = len(self.frames)
            if self.processed < length - 20:
                newframes = []
                i = self.processed
                while i < length - 20:
                    newframes.append(self.frames[i])
                    i += 1
                data = b"".join(newframes)
                audio = sr.AudioData(data, RATE, p.get_sample_size(FORMAT))
                try:
                    self.text = self.text + " " + r.recognize_google(audio, language="nl-NL")
                    self.processed = i
                    window_frames = []
                    for j in range(self.processed, length - 1):
                        window_frames.append(self.frames[j])
                    window_data = b"".join(window_frames)
                    window_audio = sr.AudioData(window_data, RATE, p.get_sample_size(FORMAT))
                    try:
                        print(self.text + r.recognize_google(window_audio, language="nl-NL"))
                    except sr.UnknownValueError:
                        print(self.text)
                except sr.UnknownValueError:
                    pass
            else:
                frame_data = b"".join(self.frames)
                audio = sr.AudioData(frame_data, RATE, p.get_sample_size(FORMAT))
                if audio is None:
                    print("no audio")# stop processing if the main thread is done
                else:

                    # received audio data, now we'll recognize it using Google Speech Recognition
                    try:
                        # for testing purposes, we're just using the default API key
                        # to use another API key, use `r.recognize_google(audio, key="GOOGLE_SPEECH_RECOGNITION_API_KEY")`
                        # instead of `r.recognize_google(audio)`
                        print(self.text + r.recognize_google(audio, language="nl-NL"))
                    except sr.UnknownValueError:
                        # print("Google Speech Recognition could not understand audio")
                        pass
                    except sr.RequestError as e:
                        print("Could not request results from Google Speech Recognition service; {0}".format(e))
            time.sleep(0.5)

    def recognize(self):
        lower = 0
        last = 0
        upper = 0
        window = 80
        delta = 20
        overlap = window
        uncertain = window
        assert delta <= uncertain
        while True:
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
                self.combine(r.recognize_google(audio, language="nl-NL"))
                print("text: " + self.text)
            except sr.UnknownValueError:
                # print("Google Speech Recognition could not understand audio")
                print("text: " + self.text)
                pass
            except sr.RequestError as e:
                print("Could not request results from Google Speech Recognition service; {0}".format(e))
            last = upper  # (upper)
            time.sleep(2)

    def combine(self, new_text):
        first_char = new_text[0]
        length = len(self.text)
        minlength = max(0, length - len(new_text))
        for index in range(minlength, length):
            if self.text[index] == first_char:
                for o, n in zip(self.text[index:], new_text):
                    if o != n:
                        break
                else:
                    self.text = self.text[:index] + new_text
                    return
        print('warn: niets herkend')
        self.text = self.text + " " + new_text

    def startup(self):
        # start a new thread to recognize audio, while this thread focuses on listening
        listen_thread = Thread(target=self.listen_and_chop)
        listen_thread.start()
        recognize_thread = Thread(target=self.recognize, daemon=True)
        recognize_thread.start()
        recognize_thread.join()  # doet nu niets

if __name__ == "__main__":
    qs = Queuespeech()
    qs.startup()
