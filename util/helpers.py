import os
import time
# import sys
# sys.path.append('E:\\车万\\project')
from util.get_memory_data import GameData
from util.send_input import Keyboard
from cfg.constants import *

game = GameData()

__all__ = ['get_timestr']


def timer_pressbutton(times):
    time_start = time.time()
    for i in range(times):
        # 操作
        # pydirectinput.keyDown('shift')
        # pydirectinput.press('right')
        # pydirectinput.keyUp('shift')
        time.sleep(0.2)
        # Keyboard.pressByScanCode(SC_SHIFT)
        Keyboard.pressByScanCode(SC_DOWN)
        time.sleep(0.03)
        Keyboard.releaseByScanCode(SC_DOWN)
        # Keyboard.releaseByScanCode(SC_SHIFT)
    time_end = time.time()
    time_cost = time_end - time_start
    print('Each_cost:%.3fs Freq:%.2fcalled/sec' % (time_cost / times, times / time_cost))


def timer_getdata(times):
    time_start = time.time()
    for i in range(times):
        # game.print_formatted_data()
        data = game.get_formatted_data()
    time_end = time.time()
    time_cost = time_end - time_start
    print('freq:called/sec', times / time_cost)


def get_max_volume():
    max_powers = 0
    max_enemy = 0
    max_bullet = 0
    max_laser = 0
    while True:
        data = game.get_formatted_data()
        if max_powers < data['powers'].shape[0]:
            max_powers = data['powers'].shape[0]
        if max_enemy < data['enemy'].shape[0]:
            max_enemy = data['enemy'].shape[0]
        if max_bullet < data['bullet'].shape[0]:
            max_bullet = data['bullet'].shape[0]
        if max_laser < data['laser'].shape[0]:
            max_laser = data['laser'].shape[0]
        print('mpwr%d,menm%d,mblt%d,mlsr%d' % (max_powers, max_enemy, max_bullet, max_laser))
        time.sleep(0.1)


def get_timestr():
    timestamp = int(time.time())
    time_struct = time.localtime(timestamp)
    time_str = time.strftime("%Y-%m-%d_%H-%Mm", time_struct)
    return time_str


def _way():
    path = os.path.join(r'ab.txt')
    # with open(path, 'w+') as f:
    #     f.write('Hello World')
    print(path)
    f = open(path, 'w')
    f.write('Hello World')
    f.close()
    print(__file__)
    return path


if __name__ == "__main__":
    time.sleep(3)
    # get_max_volume()
    _way()
    while True:
        # timer_pressbutton(1000)
        # timer_getdata(200)
        # print(get_timestr())
        # _ = os.system('cls')
        pass
