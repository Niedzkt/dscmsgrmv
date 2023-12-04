import cv2
import numpy as np
import pyautogui
import time
import pygetwindow as gw

def locateOnScreen(imagePath, confidence=0.8):
    referenceImage = cv2.imread(imagePath, cv2.IMREAD_UNCHANGED)
    
    if referenceImage.shape[2] == 4:
        referenceImage = cv2.cvtColor(referenceImage, cv2.COLOR_BGRA2BGR)
    
    screenshot = pyautogui.screenshot()
    screenshot = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)
    
    result = cv2.matchTemplate(screenshot, referenceImage, cv2.TM_CCOEFF_NORMED)
    _, max_val, _, max_loc = cv2.minMaxLoc(result)
    if max_val < confidence:
        return None
    return max_loc

def isDiscordActive(windowTitle = 'Discord'):
    try:
        activeWindow = gw.getActiveWindow()
        return windowTitle.lower() in activeWindow.title.lower()
    
    except:
        return False

binImage = 'img/bin.png'

while True:
    if isDiscordActive():
        binImageLocation = locateOnScreen(binImage)
        if binImageLocation is not None:
            pyautogui.keyDown('shift')
            pyautogui.click(binImageLocation)
            pyautogui.keyUp('shift')
            time.sleep(1)
            
            pyautogui.press('up')
            time.sleep(1)
            pass
        
    else:
        print("Discord is not active. Waiting...")
        time.sleep(5)
        print("Bin not found")
    
    time.sleep(1)
