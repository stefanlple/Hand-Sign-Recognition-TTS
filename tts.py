import pyttsx3
#pip install pyttsx3
#bei Fehler in sapi5.py token hardcoden

import websockets
import asyncio
#pip install websockets

import base64

b64file = base64.b64encode(open("speech.wav", "rb").read()) #encode wav file with base64 for sending
#print(b64file)                      #base64 encoded wav file
#print(base64.b64decode(b64file))    #base64 decoded wav file ( same as print(open("speech.wav", "rb").read()) )

async def handleMessage(websocket):
    async for message in websocket:
        if (message == "connected"):
            print("New connection")
            await websocket.send("Hello new client")
            await websocket.send(b64file)

        print("Client: " + message)

async def main():
    async with websockets.serve(handleMessage, "localhost", 8765):
        await asyncio.Future()

asyncio.run(main())
"""
engine = pyttsx3.init()

#voices = engine.getProperty('voices')
#for voice in voices:
    #print(voice.id) #alle verfügbaren Stimmen

#engine.say("good morning")
engine.save_to_file("good morning", 'speech.wav')
engine.runAndWait()
"""