import cv2
from cvzone.HandTrackingModule import HandDetector

class Button:
    def __init__(self, pos, width, height, value):

        self.pos = pos
        self.width = width
        self.height = height
        self.value = value

    def drawButton(self, img):
        cv2.rectangle(img, self.pos, (self.pos[0] + self.width, self.pos[1] + self.height), (225, 225, 255), cv2.FILLED)
        cv2.rectangle(img,  self.pos, (self.pos[0] + self.width, self.pos[1] + self.height),(50, 50, 50), 2)
        cv2.putText(img, self.value, (self.pos[0]+30, self.pos[1]+70) , cv2.FONT_HERSHEY_PLAIN, 4, (50, 50, 50), 3)

    @staticmethod
    def drawResult(img):
        cv2.rectangle(img, (800, 70), (800 + 400, 70 + 100), (225, 225, 255), cv2.FILLED)
        cv2.rectangle(img, (800, 70), (800 + 400, 70 + 100), (50, 50, 50), 2)

    def checkClick(self, x, y):
        if self.pos[0] < x < self.pos[0] + self.width \
                and self.pos[1] < y < self.pos[1] + self.height:
            cv2.rectangle(img, self.pos, (self.pos[0] + self.width, self.pos[1] + self.height),
                          (255, 255, 255),cv2.FILLED)
            cv2.rectangle(img, self.pos, (self.pos[0] + self.width, self.pos[1] + self.height),
                          (50, 50, 50), 2)
            cv2.putText(img, self.value, (self.pos[0] + 30, self.pos[1] + 70), cv2.FONT_HERSHEY_PLAIN, 4,
                        (0, 0, 0),5)
            return True
        else:
            return False


cap = cv2.VideoCapture(0)
cap.set(3, 1280)
cap.set(4, 720)
detector = HandDetector(detectionCon=0.8, maxHands=1)

buttonValuesList = [['7', '8', '9', '*'],
                    ['4', '5', '6', '-'],
                    ['1', '2', '3', '+'],
                    ['0', '/', '.', '=']]

myEquation = ""
delayCounter = 0

buttonList = []
for x in range(4):
    xpos = x * 100 + 800
    for y in range(4):
        ypos = y * 100 + 150
        buttonList.append(Button((xpos, ypos), 100, 100, buttonValuesList[y][x]))

while True:
    #capture holder
    success, img = cap.read()
    img = cv2.flip(img, 1)

    #detection part
    hands, img = detector.findHands(img, flipType= False)
    #calculator drawing
    Button.drawResult(img)
    for button in buttonList:
        button.drawButton(img)

    #processing
    #check hands
    if hands:
        lmList = hands[0]['lmList']
        length, _, img = detector.findDistance(lmList[8], lmList[12], img)
        x, y = lmList[8]
        print(length)
        if length < 50:
            for i, button in enumerate(buttonList):
                if button.checkClick(x, y) and delayCounter == 0:
                    myVal = buttonValuesList[int(i%4)][int(i/4)]
                    if myVal == "=":
                        try:
                            myEquation = str(eval(myEquation))
                        except SyntaxError:
                            myEquation = "Error"
                        except ZeroDivisionError:
                            myEquation = "Error"
                    else:
                        myEquation += myVal

                    delayCounter=1
    #delay counter
    if delayCounter !=0:
        delayCounter +=1
        if delayCounter > 10:
            delayCounter = 0

    #display result
    cv2.putText(img, myEquation, (810, 130), cv2.FONT_HERSHEY_PLAIN, 4, (50, 50, 50), 3)


    cv2.imshow("Image", img)
    key = cv2.waitKey(5)
    if key == ord('c'): #empty string
        myEquation = ""
    if key == 27: # escape
        break
