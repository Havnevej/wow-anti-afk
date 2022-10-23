import re
import pyautogui
from win32gui import GetWindowText, GetForegroundWindow, EnumWindows, SetForegroundWindow
import time
import random

wowGuid=""
currentGuid=""

def sendWowKeyPress(key, delay=0.05, modifier=None):
    if "+" in key:
        keyFrag = key.split("+")
        modifier = keyFrag[0]
        key = keyFrag[1]
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
    wowTitle = "World of Warcraft"
    keys = ['a', 'd', 'space', 'alt+1', 'q']
    print(f"Loaded with keylist:{keys}")
    nextKey=''
    while True:
        currentGuid=GetForegroundWindow()
        EnumWindows(windowsCallback, wowTitle)
        
        if(currentGuid != wowGuid):
            SetForegroundWindow(wowGuid)
            
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

        interval = random.randint(60, 600)
        time.sleep(interval)

if __name__ == "__main__":
    main()
