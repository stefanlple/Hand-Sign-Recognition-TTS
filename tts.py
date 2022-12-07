import pyttsx3
#pip install pyttsx3
#bei Fehler in sapi5.py token hardcoden

import websockets
import asyncio
#pip install websockets

import base64

engine = pyttsx3.init()
b64file = None
newData = False
text = "Good afternoon"

#b64file = base64.b64encode(open("speech.wav", "rb").read()) #encode wav file with base64 for sending
#print(b64file)                      #base64 encoded wav file
#print(base64.b64decode(b64file))    #base64 decoded wav file ( same as print(open("speech.wav", "rb").read()) )

def createFile(messageString, filenameString):
    engine.save_to_file(messageString, filenameString + '.wav')
    engine.runAndWait()

    global b64file
    b64file = base64.b64encode(open(filenameString + '.wav', "rb").read()) #encode wav file with base64 for sending

    global newData
    newData = True

    print("generated, saved and encoded new .wav-file")

async def handleMessage(websocket):
    global newData

    if newData:
        newData = False
        await websocket.send(b64file)
        print("sent file")

    async for message in websocket:
        print(message)
        if(message == "request data"):
            if (b64file != None):
                await websocket.send(b64file)
            else:
                print("b64file: None")
                createFile(text, "speech")

        if(message == "test"):
            createFile("test", "speech")

async def main():
    async with websockets.serve(handleMessage, "localhost", 8765):
        await asyncio.Future()

asyncio.run(main())