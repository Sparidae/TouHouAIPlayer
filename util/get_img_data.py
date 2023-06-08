import time
import win32gui, win32ui, win32con, win32api
from cfg.constants import *
from PIL import Image
import numpy as np
from util.get_memory_data import GameData

hwnd = win32gui.FindWindow(None, GAME_TITLE)  # 窗口的编号，0号表示当前活跃窗口
w = 385
h = 451


def img_capture(filename='instantGame.jpg', reshape=False):  # 需将窗口置于前台，不能最小化
    # 根据窗口句柄获取窗口的设备上下文DC（Device Context）
    hwnd_dc = win32gui.GetWindowDC(hwnd)
    # 根据窗口的DC获取mfcDC mfcDC创建可兼容的DC 创建big_map准备保存图片
    mfc_dc = win32ui.CreateDCFromHandle(hwnd_dc)
    save_dc = mfc_dc.CreateCompatibleDC()
    save_bit_map = win32ui.CreateBitmap()
    # 为bitmap开辟空间 高度saveDC，将截图保存到saveBitmap中
    save_bit_map.CreateCompatibleBitmap(mfc_dc, w, h)
    save_dc.SelectObject(save_bit_map)
    # 截取从左上角（0，0）长宽为（w，h）的图片
    save_dc.BitBlt((0, 0), (w, h), mfc_dc, (34, 41), win32con.SRCCOPY)
    # save_bit_map.SaveBitmapFile(save_dc, filename)
    # 将位图数据转换为图像数据
    bmp_info = save_bit_map.GetInfo()
    bmp_str = save_bit_map.GetBitmapBits(True)
    image = Image.frombuffer('RGB', (w, h), bmp_str, 'raw', 'BGRX', 0, 1)
    image.save(filename)
    array = np.array(image)
    if reshape:
        array = np.transpose(array, (2, 0, 1))
    # array = array.astype('float32')
    # print('Array shape:', array.shape)
    return array


def _generate_observation(self):
    self.data = GameData()
    self.state = self.data.get_formatted_data()
    obs = np.zeros((w, h, 3), dtype=np.uint8)  # 设置矩阵的大小和游戏界面相同 385*451 底色为黑色

    # 设置玩家的位置为蓝色 3*3
    x_p, y_p = int(self.state['player'][0]), int(self.state['player'][1])
    for i in range(3):
        for j in range(3):
            if x_p in range(w) and y_p in range(h):
                obs[x_p-1+i, y_p-1+j] = np.array([0, 0, 255], dtype=np.uint8)

    # Stack single layer into 3-channel-image.
    # obs = np.stack((obs, obs, obs), axis=-1)

    # 设置敌人的位置为红色 3*3
    # x_e, y_e = self.state['enemy'][0], self.state['enemy'][1]
    for enemy in self.state['enemy']:
        x, y = int(enemy[0]), int(enemy[1])   # 获取每行的前两个元素作为坐标
        if x in range(w) and y in range(h):
            obs[x, y] = np.array([255, 0, 0], dtype=np.uint8)  # 设置对应坐标的像素颜色为红色

    # 设置敌机子弹为绿色
    for bullet in self.state['bullet']:
        x, y = int(bullet[0]), int(bullet[1])  # 获取每行的前两个元素作为坐标
        if x in range(w) and y in range(h):
            obs[x, y] = np.array([0, 255, 0], dtype=np.uint8)

    # 设置奖励物品为白色
    for powers in self.state['powers']:
        x, y = int(powers[0]), int(powers[1])  # 获取每行的前两个元素作为坐标
        if x in range(w) and y in range(h):
            obs[x, y] = np.array([255, 255, 255], dtype=np.uint8)

    # Enlarge the observation to 84x84
    # obs = np.repeat(np.repeat(obs, 7, axis=0), 7, axis=1)

    return obs

if __name__ == '__main__':
    beg = time.time()
    # for i in range(10):
    #     window_capture("haha.jpg")
    a = img_capture("haha.jpg")
    end = time.time()
    print(end - beg)
    # print(a)
    # 获取监控器信息
    # monitor_dev = win32api.EnumDisplayMonitors(None, None)
    # w = monitor_dev[0][2][2]# 获取显示器宽
    # h = monitor_dev[0][2][3]# 获取显示器高
