import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)

green = 27
red = 17
blue = 22

global RUNNING
RUNNING = True

global isFlowing
isFlowing = False

global flowInterrupted
flowInterrupted = False

GPIO.setup(red, GPIO.OUT)
GPIO.setup(green, GPIO.OUT)
GPIO.setup(blue, GPIO.OUT)

Freq = 100

RED = GPIO.PWM(red, Freq)
GREEN = GPIO.PWM(green, Freq)
BLUE = GPIO.PWM(blue, Freq)

def calculateRGB(h):
    r, g, b = 0, 0, 0

    if h > 1:
        h = 1

    if h < 1 / 3:
        r = 2 - h * 6
        g = h * 6
        b = 0
    elif h < 2 / 3:
        r = 0
        g = 4 - h * 6
        b = h * 6 - 2
    else:
        r = h * 6 - 4
        g = 0
        b = (1 - h) * 6
  
    if r > 1:
        r = 1
    if g > 1:
        g = 1
    if b > 1:
        b = 1
  
    r = r * 255
    g = g * 255
    b = b * 255
    return {"r" : r, "g" : g, "b" : b}

def outputColorToLED(colorDict):
    setRedDutyCycle(colorDict['r']    / 2.55)
    setGreenDutyCycle(colorDict['g'] / 2.55)
    setBlueDutyCycle(colorDict['b'] / 2.55)

def insertHue(hue):
    setFlowInterrupted(True)
    setIsFlowing(False)
    time.sleep(0.01)
    outputColorToLED(calculateRGB(hue))
    setFlowInterrupted(False)

def flow():
    setIsFlowing(True)
    for i in range(0,1000):
        if not getFlowInterrupted():
            outputColorToLED(calculateRGB(i/1000))
            time.sleep(0.025)
        else:
            break
    setFlowInterrupted(False)
    setIsFlowing(False)

def setRedDutyCycle(value):
    RED.ChangeDutyCycle(value)

def setGreenDutyCycle(value):
    GREEN.ChangeDutyCycle(value)


def setBlueDutyCycle(value):
    BLUE.ChangeDutyCycle(value)


def offToFullToOff():
    for i in range(0,100):
        setRedDutyCycle(i)
        setGreenDutyCycle(i)
        setBlueDutyCycle(i)
        time.sleep(0.05)
    for i in range(100,-1,-1):
        setRedDutyCycle(i)
        setGreenDutyCycle(i)
        setBlueDutyCycle(i)
        time.sleep(0.05)    

def listenToInput():
    while True:
        userInput = input("command: ")
        if userInput == "s":
            RUNNING = False
            defaultLedState()
        if userInput == "flow":
            flow()
        if isFloat(userInput):
            defaultLedState()
            insertHue(float(userInput))

def isFloat(input):
    try:
        float(input)
    except ValueError:
        return False
    return True

def defaultLedState():
    RED.start(0)
    GREEN.start(0)
    BLUE.start(0)

def getFlowInterrupted():
    return flowInterrupted

def setFlowInterrupted(flowInterruptionState):
    global flowInterrupted
    flowInterrupted = flowInterruptionState

def getIsFlowing():
    return isFlowing

def setIsFlowing(isFlowingState):
    global isFlowing
    isFlowing = isFlowingState

# listenToInput()