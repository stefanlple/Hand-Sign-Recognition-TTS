import pyttsx3
#pip install pyttsx3
#bei Fehler in sapi5.py "raise ValueError('unknown voice id %s', id_)" auskommentieren
engine = pyttsx3.init()
engine.say("Ich spreche diesen Text")
engine.runAndWait()