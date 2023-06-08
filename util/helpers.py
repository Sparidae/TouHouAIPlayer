import os
import time
from util.get_memory_data import GameData
from util.send_input import Keyboard
from cfg.constants import *
import matplotlib.pyplot as plt
import numpy as np
from scipy import stats

# game = GameData()

__all__ = ['get_timestr', 'save_config', 'get_short_timestr', 'linear_schedule']


def linear_schedule(initial_value, final_value=0.0):
    if isinstance(initial_value, str):
        initial_value = float(initial_value)
        final_value = float(final_value)
        assert (initial_value > 0.0)

    def scheduler(progress):
        return final_value + progress * (initial_value - final_value)

    return scheduler


def get_timestr():
    timestamp = int(time.time())
    time_struct = time.localtime(timestamp)
    time_str = time.strftime("%Y-%m-%d_%H-%Mm", time_struct)
    return time_str


def get_short_timestr():
    timestamp = int(time.time())
    time_struct = time.localtime(timestamp)
    time_str = time.strftime("%m%d_%H%M", time_struct)
    return time_str


def save_config(source_path, target_path):
    os.makedirs(os.path.dirname(target_path), exist_ok=True)
    with open(source_path, 'r', encoding='utf-8') as source, open(target_path, 'w', encoding='utf-8') as target:
        content = source.read()
        target.write(content)


def _timer_pressbutton(times):
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


def _timer_getdata(times):
    time_start = time.time()
    for i in range(times):
        # game.print_formatted_data()
        data = game.get_formatted_data()
    time_end = time.time()
    time_cost = time_end - time_start
    print('freq:called/sec', times / time_cost)


def _get_max_volume():
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
    print(get_short_timestr())
    # save_config('../cfg/config.py', '../log/1/config')
    # # get_max_volume()
    # # _way()
    # a = []
    # b = []
    # print(len(a), len(b))
    # a = [x for x in a if x != 0]
    # b = [x for x in b if x != 0]
    # a = np.sort(a)
    # b = np.sort(b)
    # print(a)
    # print(b)
    # print(len(a), len(b))
    # # print(a[int(len(a) / 2)], a[int(len(a) / 4)], a[int(len(a) / 8)])
    # # density = stats.gaussian_kde(a)
    # # density = stats.gaussian_kde(data)
    # # x = np.linspace(min(a), max(a), len(a))
    # # plt.plot(a, density(a))
    # a = [x for x in a if x <= 500]
    # b = [x for x in b if x > 0]
    # print(len(a), len(b))
    # c = [x for x in b if x < 5]
    # print(len(c))
    # c = [x for x in b if x > 10 and x < 40]
    # print(len(c))
    # c = [x for x in b if x >= 40]
    # print(len(c))
    # plt.hist(a, bins=50)
    # # xticks = np.linspace(0, 500, num=10)
    # # xticklabels = ['%.2f' % i for i in xticks]
    # # plt.xticks(xticks, xticklabels)
    # plt.savefig('output.png', dpi=500)
    # plt.show()
    # plt.hist(b, bins=50)
    # plt.show()

    while True:
        # timer_pressbutton(1000)
        # timer_getdata(200)
        # print(get_timestr())
        # _ = os.system('cls')
        pass
