import ctypes
import time
import admin
from random import choice

SendInput = ctypes.windll.user32.SendInput

KEYS = {
"ESCAPE":          0x01,
"1":               0x02,
"2":               0x03,
"3":               0x04,
"4":               0x05,
"5":               0x06,
"6":               0x07,
"7":               0x08,
"8":               0x09,
"9":               0x0A,
"0":               0x0B,
"MINUS":           0x0C,    
"EQUALS":          0x0D,
"BACK":            0x0E,    
"TAB":             0x0F,
"Q":               0x10,
"W":               0x11,
"E":               0x12,
"R":               0x13,
"T":               0x14,
"Y":               0x15,
"U":               0x16,
"I":               0x17,
"O":               0x18,
"P":               0x19,
"LBRACKET":        0x1A,
"RBRACKET":        0x1B,
"RETURN":          0x1C,   
"LCONTROL":        0x1D,
"A":               0x1E,
"S":               0x1F,
"D":               0x20,
"F":               0x21,
"G":               0x22,
"H":               0x23,
"J":               0x24,
"K":               0x25,
"L":               0x26,
"SEMICOLON":       0x27,
"APOSTROPHE":      0x28,
"GRAVE":           0x29,   
"LSHIFT":          0x2A,
"BACKSLASH":       0x2B,
"Z":               0x2C,
"X":               0x2D,
"C":               0x2E,
"V":               0x2F,
"B":               0x30,
"N":               0x31,
"M":               0x32,
"COMMA":           0x33,
"PERIOD":          0x34,    
"SLASH":           0x35,    
"RSHIFT":          0x36,
"MULTIPLY":        0x37,    
"LMENU":           0x38,    
"SPACE":           0x39,
"CAPITAL":         0x3A,
"F1":              0x3B,
"F2":              0x3C,
"F3":              0x3D,
"F4":              0x3E,
"F5":              0x3F,
"F6":              0x40,
"F7":              0x41,
"F8":              0x42,
"F9":              0x43,
"F10":             0x44,
"NUMLOCK":         0x45,
"SCROLL":          0x46,   
"NUMPAD7":         0x47,
"NUMPAD8":         0x48,
"NUMPAD9":         0x49,
"SUBTRACT":        0x4A,    
"NUMPAD4":         0x4B,
"NUMPAD5":         0x4C,
"NUMPAD6":         0x4D,
"ADD":             0x4E,    
"NUMPAD1":         0x4F,
"NUMPAD2":         0x50,
"NUMPAD3":         0x51,
"NUMPAD0":         0x52,
"DECIMAL":         0x53,    
"F11":             0x57,
"F12":             0x58,


}
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
        random_move()
        

        





