from pynput import keyboard
from pynput.keyboard import Key, Controller
import clipboard
import time

COMBINATIONS = [
    {keyboard.KeyCode(char='`')}
]

# The currently active modifiers
current = set()

kb = Controller()

def execute():
    clipboard.copy(time.strftime('%d-%m-%Y %H-%M-%S', time.localtime()) + ' ')
    kb.press(Key.backspace)
    kb.release(Key.backspace) 
    kb.press(Key.ctrl.value)
    kb.press('v')
    kb.release('v')
    kb.release(Key.ctrl.value)

def on_press(key):
    if any([key in COMBO for COMBO in COMBINATIONS]):
        current.add(key)
        if any(all(k in current for k in COMBO) for COMBO in COMBINATIONS):
            execute()

def on_release(key):
    if any([key in COMBO for COMBO in COMBINATIONS]):
        current.remove(key)

with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
    listener.join()