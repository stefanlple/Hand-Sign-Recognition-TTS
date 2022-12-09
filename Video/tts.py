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
text = "This is some long text to test the play and stop functionality of the play-stop-button"

#b64file = base64.b64encode(open("speech.wav", "rb").read()) #encode wav file with base64 for sending
#print(b64file)                      #base64 encoded wav file
#print(base64.b64decode(b64file))    #base64 decoded wav file ( same as print(open("speech.wav", "rb").read()) )

#call this method to generate, save, encode and send a .wav file from a string
def createFile(messageString, filenameString):
    engine.save_to_file(messageString, filenameString + '.wav')
    engine.runAndWait()

    global b64file
    b64file = base64.b64encode(open(filenameString + '.wav', "rb").read()) #encode wav file with base64 for sending

    global newData
    newData = True

    print("generated, saved and encoded new .wav-file")

#checks if there is any new data (i.e if createFile was called) and sends it
async def checkNewData(websocket):
    global newData

    while True:
        if (newData):
            print("new Data!")
            await websocket.send(b64file)
            print("new Data sent")
            newData = False
        await asyncio.sleep(0.5)


async def handleMessage(websocket):

    asyncio.ensure_future(checkNewData(websocket))

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