import time
import win32gui, win32ui, win32con, win32api
from cfg.constants import *
from PIL import Image
import numpy as np

hwnd = win32gui.FindWindow(None, GAME_TITLE)  # 窗口的编号，0号表示当前活跃窗口
w = 385
h = 451

def img_capture(filename='instant.jpg'):
    # 根据窗口句柄获取窗口的设备上下文DC（Device Context）
    hwnd_dc = win32gui.GetWindowDC(hwnd)
    # 根据窗口的DC获取mfcDC
    mfc_dc = win32ui.CreateDCFromHandle(hwnd_dc)
    # mfcDC创建可兼容的DC
    save_dc = mfc_dc.CreateCompatibleDC()
    # 创建big_map准备保存图片
    save_bit_map = win32ui.CreateBitmap()
    # 获取监控器信息
    # monitor_dev = win32api.EnumDisplayMonitors(None, None)
    # w = monitor_dev[0][2][2]# 获取显示器宽
    # h = monitor_dev[0][2][3]# 获取显示器高
    # 为bitmap开辟空间
    save_bit_map.CreateCompatibleBitmap(mfc_dc, w, h)
    # 高度saveDC，将截图保存到saveBitmap中
    save_dc.SelectObject(save_bit_map)
    # 截取从左上角（0，0）长宽为（w，h）的图片
    # save_dc.BitBlt((0, 0), (383, 457), mfc_dc, (35, 42), win32con.SRCCOPY)
    save_dc.BitBlt((0, 0), (w, h), mfc_dc, (34, 41), win32con.SRCCOPY)
    # save_bit_map.SaveBitmapFile(save_dc, filename)
    # 将位图数据转换为图像数据
    bmp_info = save_bit_map.GetInfo()
    bmp_str = save_bit_map.GetBitmapBits(True)
    image = Image.frombuffer('RGB', (w, h), bmp_str, 'raw', 'BGRX', 0, 1)
    # image.save(filename)
    array = np.array(image)
    array = np.transpose(array, (2, 0, 1))
    array = array.astype('float32')
    array /= 255.0
    print('Array shape:', array.shape)
    return array

if __name__ =='__main__':
    beg = time.time()
    # for i in range(10):
    #     window_capture("haha.jpg")
    a = img_capture("haha.jpg")
    end = time.time()
    print(end - beg)
    # print(a)
