import re
import pyautogui
from win32gui import GetWindowText, GetForegroundWindow, EnumWindows, SetForegroundWindow
import time
import random

wowGuid=""
currentGuid=""

def sendLongWowKeyPress(timeSec, key):
    pyautogui.keyDown(key)
    time.sleep(float(timeSec))
    pyautogui.keyUp(key)

def sendWowKeyPress(key, delay=0.05, modifier=None):
    if "+" in key:
        keyFrag = key.split("+")
        modifier = keyFrag[0]
        key = keyFrag[1]
    elif "s-" in key:
        sendLongWowKeyPress(key.split("s-")[0], key.split("s-")[1])
        return
    if modifier:
        pyautogui.keyDown(modifier)
    pyautogui.keyDown(key)
    time.sleep(delay)
    pyautogui.keyUp(key)
    if modifier:
        pyautogui.keyUp(modifier)
    
def windowsCallback(windowid, name):
    #Find wow window handle
    global wowGuid
    if re.match(name, str(GetWindowText(windowid))) is not None:
        wowGuid=windowid
        

def main():
    global wowGuid,currentGuid
    location="brunnHilda"
    waitLow=60
    waitHigh=300
    
    wowTitle = "World of Warcraft"
    keys = ['a', 'd', 'space', 'alt+1', 'q', 'c']
    sequences = {"brunnHilda":[['3s-w', '0.85s-a'],['3s-w','0.85-a']]}
    sequenceQueue=[]
    print(f"Loaded with keylist:{keys}")
    nextKey=''
    keyOrSeq = 0

    while True:
        currentGuid=GetForegroundWindow()
        EnumWindows(windowsCallback, wowTitle)
        if(currentGuid != wowGuid):
            SetForegroundWindow(wowGuid)
            
        if not nextKey and len(sequenceQueue)==0:
            keyOrSeq=random.randint(0, 1)
        if keyOrSeq == 1 or len(sequenceQueue)>0:
            waitLow=5
            waitHigh=30
            print("playing sequence")
            if len(sequenceQueue)>0:
                k=sequenceQueue[0]
                if len(sequenceQueue)>1:
                    sequenceQueue=sequenceQueue[1:]
                else:
                    sequenceQueue.pop()
            else:
                k=random.choice(sequences[location])
                if len(k)>=1:
                    for seq in k[1:]:
                        sequenceQueue.append(seq)
                    print(f"Sequence queue: {sequenceQueue}")
                k = k[0]
        else:
            waitLow=60
            waitHigh=300
            if nextKey != '':
                k=nextKey
                nextKey=''
            else:
                k=random.choice(keys)
                if k == 'a':
                    nextKey = 'd'
                elif k == 'd':
                    nextKey = 'a'
        sendWowKeyPress(k)
        print("pressing key: " + k)
        SetForegroundWindow(currentGuid)

        interval = random.randint(waitLow, waitHigh)
        time.sleep(interval)

if __name__ == "__main__":
    main()
