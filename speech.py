import speech_recognition as sr

r = sr.Recognizer()

with sr.Microphone() as source:
    print('Say anything')
    audio = r.listen(source)

    # google_text = r.recognize_google(audio)
    google_text = r.recognize_google(audio, language="nl-NL")
    # sphinx_text = r.recognize_sphinx(audio)
    # sphinx_text = r.recognize_sphinx(audio, language="nl-NL")
    print('Google says : {}'.format(google_text))
    # print('Sphinx says : {}'.format(sphinx_text))

