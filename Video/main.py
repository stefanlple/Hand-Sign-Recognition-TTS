import numpy as np
import cvzone
from cvzone.HandTrackingModule import HandDetector
from cvzone.ClassificationModule import Classifier
import cv2
import math
import random
import string
#import mediapipe as mp

#pip3 install cvzone==1.5.6  
#pip3 install numpy
#pip3 install opencv-python==4.5.4.60
#pip3 install/ pip3 install mediapipe-silicon==0.8.10.1
#pip3 install tensorflow-macos==2.9.1 #pip3 install tensorflow==2.9.1
import asyncio

classes= ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', " "]
message=""
index = None

camera = None

def mouseCallback(event, x, y, flags, param):
    global message
    global classes
    global index
    global camera
    if event == cv2.EVENT_LBUTTONDOWN:
        print("clicked")
        if y <= 50:
            #print("clicked in button area")
            if x < math.ceil(param.shape[1] / 4) - 10:
                #print("first button")
                message+=str(classes[index])
            elif x > math.ceil(param.shape[1] / 4) and x < math.ceil(param.shape[1] / 2) - 10:
                #print("second button")
                message=message[:-1]
            elif x > math.ceil(param.shape[1] / 2) and x < math.ceil(3 * (param.shape[1] / 4)) - 10:
                #print("third button")
                createFile(message, "speech")
            elif x > math.ceil(3 * (param.shape[1] / 4)) and x < param.shape[1]:
                #print("fourth button")
                camera.release()
                cv2.destroyAllWindows()


async def videoMain():
    global camera
    camera = cv2.VideoCapture(0)
    detector= cvzone.HandTrackingModule.HandDetector(detectionCon=0.8,maxHands=1)
    classifier= Classifier("Model/keras_model.h5","AlphabetReferences/classes.txt")
    fpsReader = cvzone.FPS()

    offset=20
    imgSize=800

    #classes= ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', " "]

    #message=""

    while camera.isOpened():
        await asyncio.sleep(0.01)
        global message
        global classes
        global index
        #print(randomString(10))
        success, img= camera.read()
        mainImg=img.copy()
        hands, img= detector.findHands(img)
        fps, img = fpsReader.update(img,pos=(50,80),color=(0,255,0),scale=5,thickness=5)
        whiteImage = np.zeros((imgSize, imgSize, 3), np.uint8)
        whiteImage[:] = (255,255,255)
        if hands:
            landmarksPoints= hands[0]
            x,y,width,height= hands[0]["bbox"]
            onlyHand= img[y-offset:y+height+offset,x-offset:x+width+offset]
            #print(landmarksPoints)
            #img=cv2.flip(img,1)
            #cvzone.cornerRect(img, hands[0]["bbox"])
            

            aspectRatio= height/width
            try:
                if aspectRatio>1:
                    k=imgSize/height
                    calculatedWidth=math.ceil(k*width)
                    imgResize= cv2.resize(onlyHand,(calculatedWidth,imgSize))
                    imageResized= imgResize.shape
                    widthGap=math.ceil((imgSize-calculatedWidth)/2)
                    whiteImage[:,widthGap:calculatedWidth+widthGap]=imgResize
                    prediction, index= classifier.getPrediction(whiteImage,draw=False)
                
                else:
                    k=imgSize/width
                    calculatedHeight=math.ceil(k*height)
                    imgResize= cv2.resize(onlyHand,(imgSize,calculatedHeight))
                    imageResized= imgResize.shape
                    heightGap=math.ceil((imgSize-calculatedHeight)/2)
                    whiteImage[heightGap:calculatedHeight+heightGap,:]=imgResize
                    prediction, index= classifier.getPrediction(whiteImage,draw=False)
            except:
                print("resize failed")
            #print(prediction,index)
            cv2.imshow("White",whiteImage)
            #cv2.imshow("OnlyHand",onlyHand)
            if(classes[index]==" "):
                cv2.putText(mainImg, "Space",(x+100,y-85), cv2.FONT_ITALIC, 3 , (255,0,0),5)
            else:
                cv2.putText(mainImg, classes[index],(x+100,y-85), cv2.FONT_ITALIC, 3 , (255,0,0),5)
            cv2.rectangle(mainImg,(x-offset-50,y-offset-50),(x+offset+width+50,y+offset+height+50),(255,0,0),4)
        #cv2.imshow("White",whiteImage)
        cv2.putText(mainImg, message,(00,100), cv2.FONT_HERSHEY_SIMPLEX, 2 , (255,255,255),5)

        #first button
        for x in range(0, math.ceil(mainImg.shape[1] / 4) - 10):
            for y in range(0, 50):
                mainImg[y][x] = [192, 192, 192]
        cv2.putText(mainImg, "Add", (math.ceil(mainImg.shape[1] / 8) - 30, 35), cv2.FONT_HERSHEY_SIMPLEX, 1 , (255,255,255), 2)

        #second button
        for x in range(math.ceil(mainImg.shape[1] / 4), math.ceil(mainImg.shape[1] / 2) - 10):
            for y in range(0, 50):
                mainImg[y][x] = [192, 192, 192]
        cv2.putText(mainImg, "Remove", (math.ceil(mainImg.shape[1] / 4) + 180, 35), cv2.FONT_HERSHEY_SIMPLEX, 1 , (255,255,255), 2)

        #third button
        for x in range(math.ceil(mainImg.shape[1] / 2), math.ceil(3 * (mainImg.shape[1] / 4)) - 10):
            for y in range(0, 50):
                mainImg[y][x] = [192, 192, 192]
        cv2.putText(mainImg, "Send", (math.ceil(mainImg.shape[1] / 2) +190 , 35), cv2.FONT_HERSHEY_SIMPLEX, 1 , (255,255,255), 2)

        #fourth button
        for x in range(math.ceil(3 * (mainImg.shape[1] / 4)+37), mainImg.shape[1]):
            for y in range(0, 50):
                mainImg[y][x] = [192, 192, 192]
        cv2.putText(mainImg, "Quit", (mainImg.shape[1]-250, 35), cv2.FONT_HERSHEY_SIMPLEX, 1 , (255,255,255), 2)

        cv2.imshow("Webcam",mainImg)

        cv2.setMouseCallback("Webcam", mouseCallback, mainImg)

        """
        if cv2.waitKey(1) == ord("c"):
            print("close window")
            break
            
        if cv2.waitKey(25) == ord(" "):
            message+=str(classes[index])
        
        if cv2.waitKey(25) == 8: #delete key
            message=message[:-1]

        if cv2.waitKey(25) == 13:
            createFile(message, "speech")
        """        

        cv2.waitKey(1)

        #print(message)
    camera.release()
    cv2.destroyAllWindows()










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
    asyncio.ensure_future(videoMain())
    async with websockets.serve(handleMessage, "localhost", 8765):
        await asyncio.Future()











asyncio.run(main())