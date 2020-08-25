from pynput import keyboard
import pyautogui
import pydirectinput
from pynput.keyboard import Key, Controller
import clipboard
import time
import PySimpleGUI as sg

#COMBINATIONS = [
#    {keyboard.KeyCode(char='`')}
#

# The currently active modifiers
#current = set()

#kb = Controller()
# exoskelliton speed bonus = 30%
# surface type speed bonus = stone, concrete, etc

oneTileTime = 0.2228375 #~2 tiles
#oneTileTime = 0.221
pickingUp = False

def timeAndDate():
    #clipboard.copy(time.strftime('%d-%m-%Y %H-%M-%S', time.localtime()) + ' ')
    pydirectinput.keyDown('ctrl', _pause=False)
    pydirectinput.keyDown('a', _pause=False)
    pydirectinput.keyUp('a', _pause=False)
    pydirectinput.keyUp('ctrl', _pause=False)
    #pydirectinput.typewrite(time.strftime('%d-%m-%Y %H-%M-%S', time.localtime()) + ' ', _pause=False) #slower
    pyautogui.typewrite(time.strftime('%d-%m-%Y %H-%M-%S', time.localtime()) + ' ', _pause=False) #faster

def pickUp(key):
    pydirectinput.mouseDown(button='right', _pause=False)
    pydirectinput.keyDown(key, _pause=False)

def stopPickUp():
    pydirectinput.mouseUp(button='right', _pause=False)
    pydirectinput.keyUp('w', _pause=False)
    pydirectinput.keyUp('a', _pause=False)
    pydirectinput.keyUp('s', _pause=False)
    pydirectinput.keyUp('d', _pause=False)

def place(key):
    def calcGridSize():
        posXY = pyautogui.position()  #Don't move the mouse!
        def calcRight():
            posX = 0
            blackFound = False
            while True:             
                blackFound = pyautogui.pixelMatchesColor(posXY[0] + posX, posXY[1], (0, 0, 0))
                if blackFound:
                    #pydirectinput.move(x , 0)
                    print(posX)
                    break
                else:
                    posX += 1
            return posX
        def calcLeft():
             negX = 0
             blackFound = False
             while True:             
                blackFound = pyautogui.pixelMatchesColor(posXY[0] + negX, posXY[1], (0, 0, 0))
                if blackFound:
                    #pydirectinput.move(x , 0)
                    print(negX)
                    break
                else:
                    negX -= 1
             return negX
        size = calcRight() + -calcLeft()
        print(size)
        return size

    def findBlack(gs): #gridSize
        posXY = pyautogui.position()  #Don't move the mouse!
        for x in range(gs): #get centre of grid square
                blackFound = pyautogui.pixelMatchesColor(posXY[0]+x, posXY[1], (0, 0, 0))
                if blackFound:
                    print(int((posXY[0]+x)-(gs/2)) , posXY[1])
                    #pyautogui.move(int((posXY[0]+x)-(gs/2)) , posXY[1])
                    print('Black found!', posXY[0]+x) #for debug                
                    break

    def stopPlace(stopKey): 
        nonlocal stop
        if stopKey == keyboard.KeyCode(vk=101): #numpad 5 (NUMLOCK ON)
            stop = True

    global listener
    listener.stop()
    stop = False
    placeListener = keyboard.Listener(on_press=stopPlace)    
    placeListener.start()
    #findBlack() #centre mouse cursor on current grid square
    gridSize = calcGridSize()

    while True:        
        pydirectinput.click(button='left', _pause=False)        
        pydirectinput.keyDown(key, _pause=False)  #start running  
        loopStart = time.perf_counter()   
                
        if stop:
            pydirectinput.mouseUp(button='left', _pause=False)
            pydirectinput.keyUp(key, _pause=False) #stop running
            placeListener.stop()
            listener = keyboard.Listener(on_press=on_press, on_release=on_release)
            listener.start()
            break       
        loopFinish = time.perf_counter()       

        while time.perf_counter() < (loopFinish + (oneTileTime - (loopFinish  - loopStart))): #running time
            pass
        pydirectinput.keyUp(key, _pause=False) #stop running

        findBlack(gridSize) #centre mouse cursor on current grid square
        time.sleep(1) #stop time

        
        

def on_press(key):
    global pickingUp
    #breakpoint()
    print(key)
    print('in on_press')
    if key == keyboard.KeyCode(vk=110): #Numpad Del (NUMLOCK ON)
       timeAndDate()
    if key == keyboard.KeyCode(vk=104) and pickingUp == False: #Numpad 8 (NUMLOCK ON)
       pickingUp = True
       pickUp('w')
    if key == keyboard.KeyCode(vk=100) and pickingUp == False: #Numpad 4 (NUMLOCK ON)
       pickingUp = True
       pickUp('a')
    if key == keyboard.KeyCode(vk=98) and pickingUp == False: #Numpad 4 (NUMLOCK ON)
       pickingUp = True
       pickUp('s')
    if key == keyboard.KeyCode(vk=102) and pickingUp == False: #Numpad 4 (NUMLOCK ON)
       pickingUp = True
       pickUp('d')
    if key == keyboard.Key.up and pickingUp == False:
       place('w')
    if key == keyboard.Key.left and pickingUp == False:
       place('a')
    if key == keyboard.Key.down and pickingUp == False:
       place('s')
    if key == keyboard.Key.right and pickingUp == False:
       place('d')
    if key == keyboard.KeyCode(vk=101): #numpad 5 (NUMLOCK ON)
       stopPickUp()
       pickingUp = False
    print('pickingUp', pickingUp)

#keyboard.KeyCode(vk=55): #numpad 5 (NUMLOCK OFF or ON)
def on_release(key):
    pass

#with keyboard.Listener(on_press=on_press, on_release=on_release) as listener: #'blocking' listener no good for GUI
#    listener.join()

listener = keyboard.Listener(on_press=on_press, on_release=on_release) #'non-blocking' listener good for GUI
listener.start()


sg.theme('DarkAmber')   # Add a touch of color
# All the stuff inside your window.
layout = [  [sg.Text('Some text on Row 1')],
            [sg.Text('Enter something on Row 2'), sg.InputText()],
            [sg.Button('Ok', bind_return_key=True), sg.Button('Cancel')] ]

# Create the Window
window = sg.Window('My Factorio Tools', layout, keep_on_top=True) #windows key to bring up gui
# Event Loop to process "events" and get the "values" of the inputs
while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED or event == 'Cancel': # if user closes window or clicks cancel
        break
    print(event, ' You entered ', values[0])


window.close()
listener.stop()

