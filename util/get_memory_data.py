import ctypes
from ctypes import wintypes
import psutil
import sys
import os
import time
import numpy as np
from cfg.config import *
from cfg.constants import *

# WindowsAPI Func
kernel32 = ctypes.WinDLL('kernel32')

OpenProcess = kernel32.OpenProcess
OpenProcess.argtypes = [wintypes.DWORD, wintypes.BOOL, wintypes.DWORD]
OpenProcess.restype = wintypes.HANDLE

ReadProcessMemory = kernel32.ReadProcessMemory
ReadProcessMemory.argtypes = [
    wintypes.HANDLE,  # hProcess
    wintypes.LPCVOID,  # lpBaseAddress LongPointer to Constant Void
    wintypes.LPVOID,  # lpBuffer Lp to Void
    ctypes.c_size_t,  # nSize
    ctypes.POINTER(ctypes.c_size_t)  # lpNumberOfBytesRead
]  # 进程句柄 内存地址 缓冲区buffer（存储读取的数据） 缓冲区的大小（字节） 已经读取的字节数
ReadProcessMemory.restype = wintypes.BOOL


# Class Of GameObject
class GameObject:
    def __init__(self, x, y, w, h, dx=0.0, dy=0.0):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.dx = dx
        self.dy = dy


class Laser(GameObject):
    def __init__(self, x, y, w, h, arc):
        super().__init__(x, y, w, h)
        self.arc = arc  # 弧度值


class Player(GameObject):
    def __init__(self, x, y, w=2, h=2):
        super().__init__(x, y, w, h)


class GameData:
    def __init__(self):
        # Variable
        self.is_process_running = False
        self.pid = self.__get_process_pid()
        self.handle = OpenProcess(PROCESS_VM_READ, True, self.pid)  # 根据pid获取 进程句柄
        self.player = Player(0, 0)
        self.powers = []
        self.enemy = []
        self.bullet = []
        self.laser = []
        self.score = 0
        self.power = 0
        self.extra_life = 0

    def get_formatted_data(self):
        self.__data_update()
        powers = np.array([[i.x, i.y, i.w, i.h] for i in self.powers] if len(self.powers) != 0 else [[.0, .0, .0, .0]])
        powers = np.pad(
            powers,
            ((0, MAX_POWERS - len(powers)), (0, 0))) if len(powers) < MAX_POWERS else np.resize(powers, (MAX_POWERS, 4))

        enemy = np.array([[i.x, i.y, i.w, i.h] for i in self.enemy] if len(self.enemy) != 0 else [[.0, .0, .0, .0]])
        enemy = np.pad(
            enemy,
            ((0, MAX_ENEMY - len(enemy)), (0, 0))) if len(enemy) < MAX_ENEMY else np.resize(enemy, (MAX_ENEMY, 4))

        bullet = np.array(
            [[i.x, i.y, i.w, i.h, i.dx, i.dy] for i in self.bullet] if len(self.bullet) != 0 else [
                [.0, .0, .0, .0, .0, .0]])
        bullet = np.pad(
            bullet,
            ((0, MAX_BULLET - len(bullet)), (0, 0))) if len(bullet) < MAX_BULLET else np.resize(bullet, (MAX_BULLET, 6))

        laser = np.array(
            [[i.x, i.y, i.w, i.h, i.arc] for i in self.laser] if len(self.laser) != 0 else [[.0, .0, .0, .0, .0]])
        laser = np.pad(
            laser,
            ((0, MAX_LASER - len(laser)), (0, 0))) if len(laser) < MAX_LASER else np.resize(laser, (MAX_LASER, 5))
        return {
            'player': np.array([self.player.x, self.player.y]),
            'score': np.array([self.score]),
            'power': np.array([self.power]),
            'extra_life': np.array([self.extra_life]),
            'powers': powers,
            'enemy': enemy,
            'bullet': bullet,
            'laser': laser,
        }

    def get_player_data(self):
        self.__get_player_data()
        return {
            'player': np.array([self.player.x, self.player.y]),
            'score': np.array([self.score]),
            'power': np.array([self.power]),
            'extra_life': np.array([self.extra_life]),
        }

    def print_formatted_data(self):
        self.__data_update()
        print('Player(%.2f,%.2f)' % (self.player.x, self.player.y))
        print('score:%d | power:%.2f | extra_life:%d' % (self.score * 10, self.power / 20, self.extra_life))
        # for i in self.powers:
        #     print('power:%.2f %.2f %.2f %.2f' % (i.x, i.y, i.w, i.h))
        # for i in self.enemy:
        #     print('enemy:%.2f %.2f %.2f %.2f' % (i.x, i.y, i.w, i.h))
        # for i in self.bullet:
        #     print('bullet:%.2f %.2f %.2f %.2f %.2f %.2f' % (i.x, i.y, i.w, i.h, i.dx, i.dy))
        # for i in self.laser:
        #     print('laser:%.2f %.2f %.2f %.2f %.2f' % (i.x, i.y, i.w, i.h, i.arc))
        time.sleep(0.1)
        _ = os.system('cls')  # windows

    def __data_update(self):
        self.__get_player_data()
        self.__get_enemy_data()
        self.__get_bullet_data()
        self.__get_laser_data()
        self.__get_powers()

    def __get_process_pid(self):
        for prcs in psutil.process_iter():  # 获取进程id
            if prcs.name().lower() == "th10chs.exe":
                # print(prcs.pid)
                self.is_process_running = True
                return prcs.pid
        if not self.is_process_running:  # 判断程序是否在运行
            print('th10chs.exe is not running! Program ended.')
            sys.exit(0)

    def __get_player_data(self):
        self.player = Player(0, 0)
        obj_base = ctypes.c_int()  # int obj_base
        nbr = ctypes.c_ulonglong()  # DWORD nbr 已经读取的字节number
        # print(handle)
        ReadProcessMemory(self.handle, 0x00477834, ctypes.byref(obj_base), 4, ctypes.byref(nbr))  # 获取玩家基址
        # print(obj_base)
        if obj_base.value != 0:  # 当前运行游戏有玩家对象
            x = ctypes.c_float()
            y = ctypes.c_float()
            ReadProcessMemory(self.handle, obj_base.value + 0x3c0, ctypes.byref(x), 4, ctypes.byref(nbr))
            ReadProcessMemory(self.handle, obj_base.value + 0x3c4, ctypes.byref(y), 4, ctypes.byref(nbr))
            self.player.x = x.value
            self.player.y = y.value
        # score&powers&extralife
        z = ctypes.c_int()
        ReadProcessMemory(self.handle, 0x474c44, ctypes.byref(z), 4, ctypes.byref(nbr))
        self.score = z.value
        z = ctypes.c_int()
        ReadProcessMemory(self.handle, 0x474c48, ctypes.byref(z), 4, ctypes.byref(nbr))
        self.power = z.value
        z = ctypes.c_int()
        ReadProcessMemory(self.handle, 0x474c70, ctypes.byref(z), 4, ctypes.byref(nbr))
        self.extra_life = z.value
        return

    def __get_powers(self):
        nbr = ctypes.c_ulonglong()
        self.powers = []  # 只存放GameObject
        base = ctypes.c_int()
        ReadProcessMemory(self.handle, 0x00477818, ctypes.byref(base), 4, ctypes.byref(nbr))
        if base.value == 0:
            return
        esi = ctypes.c_int(base.value + 0x14)
        ebp = ctypes.c_int(esi.value + 0x3b0)
        for _ in range(2000):
            eax = ctypes.c_int(0)
            ReadProcessMemory(self.handle, ebp.value + 0x2c, ctypes.byref(eax), 4, ctypes.byref(nbr))
            if eax.value != 0:  # 还有power对象
                x = ctypes.c_float()
                y = ctypes.c_float()
                ReadProcessMemory(self.handle, ebp.value - 0x4, ctypes.byref(x), 4, ctypes.byref(nbr))
                ReadProcessMemory(self.handle, ebp.value, ctypes.byref(y), 4, ctypes.byref(nbr))
                self.powers.append(GameObject(x.value, y.value, 6, 6))
            ebp.value += 0x3f0
        return

    def __get_enemy_data(self):
        nbr = ctypes.c_ulonglong()
        base = ctypes.c_int()
        obj_base = ctypes.c_int()
        obj_addr = ctypes.c_int()
        obj_next = ctypes.c_int()
        self.enemy = []
        ReadProcessMemory(self.handle, 0x00477704, ctypes.byref(base), 4, ctypes.byref(nbr))
        if base.value == 0:
            return
        ReadProcessMemory(self.handle, base.value + 0x58, ctypes.byref(obj_base), 4, ctypes.byref(nbr))
        if obj_base.value != 0:
            while True:
                ReadProcessMemory(self.handle, obj_base.value, ctypes.byref(obj_addr), 4, ctypes.byref(nbr))
                ReadProcessMemory(self.handle, obj_base.value + 4, ctypes.byref(obj_next), 4, ctypes.byref(nbr))
                obj_addr.value += 0x103c
                t = ctypes.c_uint()
                ReadProcessMemory(self.handle, obj_addr.value + 0x1444, ctypes.byref(t), 4, ctypes.byref(nbr))
                if not (t.value & 0x40):
                    ReadProcessMemory(self.handle, obj_addr.value + 0x1444, ctypes.byref(t), 4, ctypes.byref(nbr))
                    if not (t.value & 0x12):
                        x = ctypes.c_float()
                        y = ctypes.c_float()
                        w = ctypes.c_float()
                        h = ctypes.c_float()
                        ReadProcessMemory(self.handle, obj_addr.value + 0x2C, ctypes.byref(x), 4, ctypes.byref(nbr))
                        ReadProcessMemory(self.handle, obj_addr.value + 0x30, ctypes.byref(y), 4, ctypes.byref(nbr))
                        ReadProcessMemory(self.handle, obj_addr.value + 0xB8, ctypes.byref(w), 4, ctypes.byref(nbr))
                        ReadProcessMemory(self.handle, obj_addr.value + 0xBC, ctypes.byref(h), 4, ctypes.byref(nbr))
                        self.enemy.append(GameObject(x.value, y.value, w.value, h.value))
                if obj_next.value == 0:
                    break
                obj_base.value = obj_next.value  # 在 ctypes 中，不能直接使用 y = x 的方式将一个 ctypes 对象赋给另一个对象。这是因为 ctypes 对象是通过引用传递的，而不是通过值传递的。直接使用 y = x 会将 y 和 x 指向同一个内存地址，而不是创建一个新的对象。
        return

    def __get_bullet_data(self):
        self.bullet = []
        base = ctypes.c_int()
        nbr = ctypes.c_ulonglong()
        ReadProcessMemory(self.handle, 0x004776f0, ctypes.byref(base), 4, ctypes.byref(nbr))
        if base.value == 0:
            return
        ebx = ctypes.c_int(base.value + 0x60)
        for _ in range(2000):
            edi = ctypes.c_int(ebx.value + 0x400)
            bp = ctypes.c_int()
            ReadProcessMemory(self.handle, edi.value + 0x46, ctypes.byref(bp), 4, ctypes.byref(nbr))
            bp.value = bp.value & 0x0000FFFF  # 用于获取 bp.value 的低 16 位
            if bp.value != 0:  #
                eax = ctypes.c_int()
                ReadProcessMemory(self.handle, 0x477810, ctypes.byref(eax), 4, ctypes.byref(nbr))
                if eax.value != 0:
                    ReadProcessMemory(self.handle, eax.value + 0x58, ctypes.byref(eax), 4, ctypes.byref(nbr))
                    if not (eax.value & 0x00000400):
                        x = ctypes.c_float()
                        y = ctypes.c_float()
                        w = ctypes.c_float()
                        h = ctypes.c_float()
                        dx = ctypes.c_float()
                        dy = ctypes.c_float()
                        ReadProcessMemory(self.handle, ebx.value + 0x3C0, ctypes.byref(dx), 4, ctypes.byref(nbr))
                        ReadProcessMemory(self.handle, ebx.value + 0x3C4, ctypes.byref(dy), 4, ctypes.byref(nbr))
                        ReadProcessMemory(self.handle, ebx.value + 0x3B4, ctypes.byref(x), 4, ctypes.byref(nbr))
                        ReadProcessMemory(self.handle, ebx.value + 0x3B8, ctypes.byref(y), 4, ctypes.byref(nbr))
                        ReadProcessMemory(self.handle, ebx.value + 0x3F0, ctypes.byref(w), 4, ctypes.byref(nbr))
                        ReadProcessMemory(self.handle, ebx.value + 0x3F4, ctypes.byref(h), 4, ctypes.byref(nbr))
                        self.bullet.append(
                            GameObject(x.value, y.value, w.value, h.value, dx.value / 2.0, dy.value / 2.0))
            ebx.value += 0x7F0
        return

    def __get_laser_data(self):
        self.laser = []
        base = ctypes.c_int()
        nbr = ctypes.c_ulonglong()
        ReadProcessMemory(self.handle, 0x0047781c, ctypes.byref(base), 4, ctypes.byref(nbr))
        if base.value == 0:
            return
        esi = ctypes.c_int()
        ebx = ctypes.c_int()
        ReadProcessMemory(self.handle, base.value + 0x18, ctypes.byref(esi), 4, ctypes.byref(nbr))
        if esi.value != 0:
            while True:
                ReadProcessMemory(self.handle, esi.value + 0x8, ctypes.byref(ebx), 4, ctypes.byref(nbr))
                x = ctypes.c_float()
                y = ctypes.c_float()
                h = ctypes.c_float()
                w = ctypes.c_float()
                arc = ctypes.c_float()
                ReadProcessMemory(self.handle, esi.value + 0x24, ctypes.byref(x), 4, ctypes.byref(nbr))
                ReadProcessMemory(self.handle, esi.value + 0x28, ctypes.byref(y), 4, ctypes.byref(nbr))
                ReadProcessMemory(self.handle, esi.value + 0x3c, ctypes.byref(arc), 4, ctypes.byref(nbr))
                ReadProcessMemory(self.handle, esi.value + 0x40, ctypes.byref(h), 4, ctypes.byref(nbr))
                ReadProcessMemory(self.handle, esi.value + 0x44, ctypes.byref(w), 4, ctypes.byref(nbr))
                self.laser.append(Laser(x.value, y.value, w.value / 2.0, h.value, arc.value))
                if ebx.value == 0:
                    break
                esi.value = ebx.value
        return


if __name__ == "__main__":
    while True:
        game = GameData()
        game.print_formatted_data()
        # _ = os.system('cls')

'''获取数据量的最大值
    max_powers = 0
    max_enemy = 0
    max_bullet = 0
    max_laser = 0
    while True:
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
'''
