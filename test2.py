import win32con
import win32gui
import ctypes
import ctypes.wintypes
from keys import KEYS
import time

SendMessage = ctypes.windll.user32.SendMessageW


def get_window(window_name):
    hwnd = 0
    if window_name is not None:
        hwnd = win32gui.FindWindow(None, window_name)
    if hwnd == 0:
        def callback(h, extra):
            if window_name in win32gui.GetWindowText(h):
                extra.append(h)
            return True
        extra = []
        win32gui.EnumWindows(callback, extra)
        if extra: hwnd = extra[0]
    if hwnd == 0:
        print("Windows Application <%s> not found!" % window_name)

    return hwnd


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



class COPYDATASTRUCT(ctypes.Structure):
    _fields_ = [
        ('dwData', ctypes.wintypes.LPARAM),
        ('cbData', ctypes.wintypes.DWORD),
        ('lpData', ctypes.c_char_p)
        #formally lpData is c_void_p, but we do it this way for convenience
]


def PressKey(hexKeyCode):
    extra = ctypes.c_ulong(0)
    ii_ = Input_I()
    ii_.ki = KeyBdInput( 0, hexKeyCode, 0x0008, 0, ctypes.pointer(extra) )
    x = Input( ctypes.c_ulong(1), ii_ )
    return x

def ReleaseKey(hexKeyCode):
    extra = ctypes.c_ulong(0)
    ii_ = Input_I()
    ii_.ki = KeyBdInput( 0, hexKeyCode, 0x0008 | 0x0002, 0, ctypes.pointer(extra) )
    x = Input( ctypes.c_ulong(1), ii_ )
    return x



hwnd = get_window('Origins2-Global')

print(hwnd)

space = KEYS.get('SPACE',None)
cds = PressKey(space)
print(cds)
SendMessage(hwnd, win32con.WM_KEYDOWN, 0, ctypes.byref(cds))
time.sleep(5)