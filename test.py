import win32gui
import win32con
import win32api
from time import sleep
import ctypes
import admin

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
    


def move(coords,button, win):

    if button == None:
        _button_state = 0
    elif "right" in button.lower():
        _button_state = win32con.MK_RBUTTON
    elif "left" in button.lower():
        _button_state = win32con.MK_LBUTTON
    elif "middle" in button.lower():
        _button_state = win32con.MK_MBUTTON

    else:
        raise SyntaxError('"Button" needs to contain "left", "right" or "middle"')

    l_param = win32api.MAKELONG(coords[0], coords[1])
    win32api.PostMessage(win, win32con.WM_MOUSEMOVE, _button_state, l_param) 


def key_down(key,win):
    key = hex(ord(key))
    key = int(key,16)
    win32api.PostMessage(win, win32con.WM_CHAR, key, 0)


def key_up(key,win):
    key = hex(ord(key))
    key = int(key,16)
    win32api.PostMessage(win, win32con.WM_CHAR, key, 0)



def press(key,win,t=2):
    key_down(key,win)
    sleep(t)
    key_up(key,win)



def focus(win):
    win32gui.SetForegroundWindow(win)


def attack(win,t=2):
    win32api.SendMessage(win, win32con.WM_KEYDOWN, win32con.VK_SPACE, 0)
    sleep(t)
    win32api.SendMessage(win, win32con.WM_KEYUP, win32con.VK_SPACE, 0)



    
if __name__ == '__main__':
    if not admin.isUserAdmin():
        admin.runAsAdmin()
        exit()
    win = get_window("Origins2-Global")
    if not win:
        exit()
    
    # press('c',win)
    attack(win)
    # move([150,150],'left',win)

    print('Script runned')


