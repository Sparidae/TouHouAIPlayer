import time
import pydirectinput
import win32api
import win32com.client
import win32con
import win32gui
from cfg.constants import *


def activate_window():
    hwnd = win32gui.FindWindow(None, GAME_TITLE)
    # print('句柄', hwnd)
    win32gui.BringWindowToTop(hwnd)
    # shell = win32com.client.Dispatch("WScript.Shell") 先取消否则会点出设置窗口
    # shell.SendKeys('%')  # alt
    win32gui.SetForegroundWindow(hwnd)  # 设置为当前活动窗口
    win32gui.ShowWindow(hwnd, win32con.SW_RESTORE)  # 保持窗口



# def _window_enum_callback(hwnd, wildcard):
#     '''
#     Pass to win32gui.EnumWindows() to check all the opened windows
#     把想要置顶的窗口放到最前面，并最大化
#     '''
#     if re.match(wildcard, str(win32gui.GetWindowText(hwnd))) is not None:
#         win32gui.BringWindowToTop(hwnd)
#         # 先发送一个alt事件，否则会报错导致后面的设置无效：pywintypes.error: (0, 'SetForegroundWindow', 'No error message is available')
#         shell = win32com.client.Dispatch("WScript.Shell")
#         shell.SendKeys('%')
#         # 设置为当前活动窗口
#         win32gui.SetForegroundWindow(hwnd)
#         # 保持窗口
#         win32gui.ShowWindow(hwnd, win32con.SW_RESTORE)
#
#
# # win32gui.EnumWindows(_window_enum_callback, ".*%s.*" % '无标题 - Notepad')  # 此处为你要设置的活动窗口名

if __name__ == '__main__':
    time.sleep(5)
    # hwnd = win32gui.FindWindow(None, GAME_TITLE)
    # title = str(win32gui.GetWindowText(hwnd))
    # print(title)

    # 硬件扫描码
    # up = win32api.MapVirtualKey(win32con.VK_UP, 0)

    activate_window()
    pydirectinput.keyDown('z')
    pydirectinput.keyDown('shift')

    while True:
        time.sleep(0.1)
        # win32api.keybd_event(win32con.VK_UP, up, 0, 0)
        # time.sleep(0.2)
        # win32api.keybd_event(win32con.VK_UP, up, win32con.KEYEVENTF_KEYUP, 0)
        # pydirectinput.keyDown('up')
        # pydirectinput.keyUp('up')
        pydirectinput.press('up')
        pydirectinput.press('right')
        pydirectinput.press('down')
        pydirectinput.press('left')
