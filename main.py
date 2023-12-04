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

def isDiscordActive(windowTitle='Discord'):
    try:
        activeWindow = gw.getActiveWindow()
        return windowTitle.lower() in activeWindow.title.lower()
    
    except:
        return False
    
def moveMouseUp(start_pos, distance=10, step=1):
    x, y = start_pos
    while y > 0:
        new_y = y - step
        pyautogui.moveTo(x, new_y)
        time.sleep(0.01) 
        y = new_y
        if y <= start_pos[1] - distance:
            break

def slowScrollUp(scroll_amount=100, step=10):
    for _ in range(0, scroll_amount, step):
        pyautogui.scroll(step) 
        time.sleep(0.1)
        
        
binImage = 'img/bin.png'
menuImage = 'img/menu.png'
confirmImage = 'img/confirm.png'

while True:
    if isDiscordActive():
        dotsImageLocation = locateOnScreen(menuImage)
        if dotsImageLocation is not None:
            pyautogui.click(dotsImageLocation)
            time.sleep(1)

            binImageLocation = locateOnScreen(binImage)
            if binImageLocation is not None:
                pyautogui.click(binImageLocation)
                time.sleep(1)
                print("Message deleted")
                
                confirmImageLocation = locateOnScreen(confirmImage)
                if confirmImageLocation is not None:
                    pyautogui.click(confirmImageLocation)
                    print("Confirmation clicked")
                else:
                    print("Confirmation not found")
                    
            else:
                pyautogui.click(dotsImageLocation)
                print("Bin not found")

            pyautogui.press('down')
            time.sleep(1)
        else:
            print("Dots not found. Moving mouse up...")
            current_mouse_pos = pyautogui.position()
            slowScrollUp(scroll_amount=1000, step=100)
            moveMouseUp(current_mouse_pos, distance=100, step=5)
            time.sleep(1) 
    
    else:
        print("Discord is not active. Waiting...")
        time.sleep(5)

    time.sleep(1)
