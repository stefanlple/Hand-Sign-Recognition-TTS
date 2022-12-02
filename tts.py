import pyttsx3
#pip install pyttsx3
#bei Fehler in sapi5.py token hardcoden
engine = pyttsx3.init()

#voices = engine.getProperty('voices')
#for voice in voices:
    #print(voice.id) #alle verfügbaren Stimmen

engine.say("good morning")
engine.save_to_file("good morning", 'speech.mp3')
engine.runAndWait()