import ctypes
import time
import admin
from random import choice
from keys import KEYS


SendInput = ctypes.windll.user32.SendInput


# C struct redefinitions 
PUL = ctypes.POINTER(ctypes.c_ulong)
class KeyBdInput(ctypes.Structure):
    _fields_ = [("wVk", ctypes.c_ushort),
                ("wScan", ctypes.c_ushort),
                ("dwFlags", ctypes.c_ulong),
                ("time", ctypes.c_ulong),
                ("dwExtraInfo", PUL)]

class HardwareInput(ctypes.Structure):
    _fields_ = [("uMsg", ctypes.c_ulong),
                ("wParamL", ctypes.c_short),
                ("wParamH", ctypes.c_ushort)]

class MouseInput(ctypes.Structure):
    _fields_ = [("dx", ctypes.c_long),
                ("dy", ctypes.c_long),
                ("mouseData", ctypes.c_ulong),
                ("dwFlags", ctypes.c_ulong),
                ("time",ctypes.c_ulong),
                ("dwExtraInfo", PUL)]

class Input_I(ctypes.Union):
    _fields_ = [("ki", KeyBdInput),
                 ("mi", MouseInput),
                 ("hi", HardwareInput)]

class Input(ctypes.Structure):
    _fields_ = [("type", ctypes.c_ulong),
                ("ii", Input_I)]

# Actuals Functions

def PressKey(hexKeyCode):
    extra = ctypes.c_ulong(0)
    ii_ = Input_I()
    ii_.ki = KeyBdInput( 0, hexKeyCode, 0x0008, 0, ctypes.pointer(extra) )
    x = Input( ctypes.c_ulong(1), ii_ )
    ctypes.windll.user32.SendInput(1, ctypes.pointer(x), ctypes.sizeof(x))

def ReleaseKey(hexKeyCode):
    extra = ctypes.c_ulong(0)
    ii_ = Input_I()
    ii_.ki = KeyBdInput( 0, hexKeyCode, 0x0008 | 0x0002, 0, ctypes.pointer(extra) )
    x = Input( ctypes.c_ulong(1), ii_ )
    ctypes.windll.user32.SendInput(1, ctypes.pointer(x), ctypes.sizeof(x))


def Press(key,t=1):
    inp_key = key
    key = KEYS.get(inp_key,None)
    if key:
        PressKey(key)
        print(f'{inp_key} pressed.')
        time.sleep(t)
        ReleaseKey(key)
        print(f'{inp_key} released.')
    else:
        print('Unrecognised key')


def delay(secs):
    for x in range(secs):
        print(x+1)
        time.sleep(1)


def call_monsters(calls=2):
    for _ in range(calls):
        Press(key='1',t=.5)



def random_move(t=2):
    moves = ['W','A','S','D']
    ch = KEYS.get(choice(moves))
    PressKey(ch)
    time.sleep(t)
    ReleaseKey(ch)




if __name__ == '__main__':
    if not admin.isUserAdmin():
        admin.runAsAdmin()

    calling_delay = 5
    delay(5)

    while True:
        PressKey(KEYS.get('SPACE'))
        call_monsters(15)
        time.sleep(calling_delay)
        ReleaseKey(KEYS.get('SPACE'))
        Press('Z')
        random_move(t=4)
        

        





