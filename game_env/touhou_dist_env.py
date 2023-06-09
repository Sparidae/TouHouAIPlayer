import gym
from gym import spaces
import time
import numpy as np
import math
import pydirectinput
from util.get_memory_data import GameData
from util.window import activate_window
from util.send_input import Keyboard
from cfg.constants import *
from cfg.config import *
from PIL import Image


class TouHouDistEnv(gym.Env):
    def __init__(self):
        # 定义状态空间和动作空间
        self.observation_space = spaces.Box(low=0,
                                            high=255,
                                            shape=(128, 128, 3),
                                            dtype=np.uint8)
        self.action_space = spaces.Discrete(10)  # 动作空间 0，1，2，3，4，5，6，7 八个方向 8 x清空范围弹幕短暂无敌 9 什么也不做

        # 游戏数据源
        self.datasource = GameData()

        # 定义状态 依赖于datasource
        self.state = self._get_state()
        self.ob = self._generate_observation()

        # 需要reset()重置的变量
        # step计数 无敌帧 score奖励倍率
        self.step_count = 0

        pass

    def step(self, action):  # 用于编写智能体与环境交互的逻辑，它接受action的输入，给出下一时刻的状态、当前动作的回报、是否结束当前episode及调试信息
        reward = 0  # 本step奖励初始化
        self.step_count += 1  # 本回合执行的step量+1
        # 记录执行动作前的状态
        last_state = self.state
        # action动作
        if action == 0:  # 上
            Keyboard.pressByScanCode(SC_UP)
            time.sleep(PRESS_INTERVAL)
            Keyboard.releaseByScanCode(SC_UP)
        if action == 1:  # 下
            Keyboard.pressByScanCode(SC_DOWN)
            time.sleep(PRESS_INTERVAL)
            Keyboard.releaseByScanCode(SC_DOWN)
        if action == 2:  # 左
            Keyboard.pressByScanCode(SC_LEFT)
            time.sleep(PRESS_INTERVAL)
            Keyboard.releaseByScanCode(SC_LEFT)
        if action == 3:  # 右
            Keyboard.pressByScanCode(SC_RIGHT)
            time.sleep(PRESS_INTERVAL)
            Keyboard.releaseByScanCode(SC_RIGHT)
        if action == 4:  # 右下
            Keyboard.pressByScanCode(SC_RIGHT)
            Keyboard.pressByScanCode(SC_DOWN)
            time.sleep(PRESS_INTERVAL)
            Keyboard.releaseByScanCode(SC_RIGHT)
            Keyboard.releaseByScanCode(SC_DOWN)
        if action == 5:  # 左上
            Keyboard.pressByScanCode(SC_LEFT)
            Keyboard.pressByScanCode(SC_UP)
            time.sleep(PRESS_INTERVAL)
            Keyboard.releaseByScanCode(SC_LEFT)
            Keyboard.releaseByScanCode(SC_UP)
        if action == 6:  # 左下
            Keyboard.pressByScanCode(SC_LEFT)
            Keyboard.pressByScanCode(SC_DOWN)
            time.sleep(PRESS_INTERVAL)
            Keyboard.releaseByScanCode(SC_LEFT)
            Keyboard.releaseByScanCode(SC_DOWN)
        if action == 7:  # 右上
            Keyboard.pressByScanCode(SC_RIGHT)
            Keyboard.pressByScanCode(SC_UP)
            time.sleep(PRESS_INTERVAL)
            Keyboard.releaseByScanCode(SC_RIGHT)
            Keyboard.releaseByScanCode(SC_UP)
        if action == 8:  # X
            Keyboard.pressByScanCode(SC_X)
            time.sleep(0.01)
            Keyboard.releaseByScanCode(SC_X)
            reward = X_INSTANT_PUNISH
        if action == 9:  # 什么也不做
            time.sleep(PRESS_INTERVAL)
            pass

        # 计算reward 移动奖励
        if action != 8:
            reward = MOVE_REWARD

        # 更新状态
        self.state = self._get_state()
        self.ob = self._generate_observation()

        # 判断是否终止
        done = self._is_done()

        # 按照曼哈顿距离迭代计算reward
        # 和敌人距离的关系
        player = self.state['player']
        for enemy in self.state['enemy']:
            if abs(enemy[0] - player[0]) < 10 and player[1] > enemy[1]:
                reward += 4
        # 和弹幕距离的关系
        for bullet in self.state['bullet']:
            dist = (bullet[0] - player[0]) ** 2 + (bullet[1] - player[1]) ** 2
            if dist < 15:
                reward -= 8
            elif dist < 30:
                reward -= 5
            elif 30 <= dist < 50:
                reward -= 2

        if self.state['extra_life'][0] < last_state['extra_life'][0]:  # 掉生命了
            reward = DEAD_PUNISH
        elif self.state['extra_life'][0] > last_state['extra_life'][0]:  # 残机增加
            reward = OBTAIN_LIFE_REWARD

        # observation->state  reward->int  done->bool  info->dict
        return self.ob, reward, done, {}

    def reset(self):
        # 游戏失败后重置游戏的操作
        print('---env.reset() is called---')
        # 重置变量
        self.step_count = 0
        activate_window()
        if self._is_done():  # 游戏失败重开的情况
            # '满身疮痍enter -> '返回标题画面down -> '继续游戏enter
            time.sleep(1)
            pydirectinput.press('enter')
            time.sleep(1)
            pydirectinput.press('down')
            time.sleep(1)
            pydirectinput.press('enter')
            time.sleep(1)
            pydirectinput.keyDown('z')
        else:  # 游戏刚开始的情况 现在方案：开始游戏后开始训练（ 取色脚本？ 图像识别？
            pass
        self.state = self._get_state()
        self.ob = self._generate_observation()
        # '%d %d %d %d' print('%d %d %d %d' % (max(self.score_list), min(self.score_list), max(self.power_list),
        # min(self.power_list))) print('%.2f %.2f' % (sum(self.score_list) / len(self.score_list),
        # sum(self.power_list) / len(self.power_list)))
        return self.ob

    def _get_state(self) -> dict:
        return self.datasource.get_formatted_data()

    def _is_done(self) -> bool:
        if self.state['extra_life'][0] == -1:  # 死了
            return True
        else:
            return False

    def _generate_observation(self):  # 360-400 -> 256-256 -> 128-128 /=2,4
        # self.state = self._get_state()
        # beg = time.time()
        obs = np.zeros((128, 128), dtype=np.uint8)
        obs = np.stack((obs, obs, obs), axis=-1)
        # powers
        for x, y, w, h in self.state['powers']:  # 注意浮点数
            _x, _y = self._x_y_transfer(x, y)
            w, h = w / 8, h / 8
            w, h = math.floor(w) if w > 1 else 1, math.floor(h) if h > 1 else 1
            for _w in range(-w, w + 1):
                for _h in range(-h, h + 1):
                    obs[_x + _w, _y + _h] = [0, 255, 0]  # 绿色power
        for x, y, w, h in self.state['enemy']:  # 注意浮点数
            _x, _y = self._x_y_transfer(x, y)
            w, h = w / 8, h / 8
            w, h = math.floor(w) if w > 1 else 1, math.floor(h) if h > 1 else 1
            for _w in range(-w, w + 1):
                for _h in range(-h, h + 1):
                    obs[_x + _w, _y + _h] = [255, 0, 0]
        for x, y, w, h, dx, dy in self.state['bullet']:  # 注意浮点数
            _x, _y = self._x_y_transfer(x, y)
            w, h = w / 8, h / 8
            w, h = math.floor(w) if w > 1 else 1, math.floor(h) if h > 1 else 1
            for _w in range(-w, w + 1):
                for _h in range(-h, h + 1):
                    obs[_x + _w, _y + _h] = [255, 0, 0]
        # for x, y, w, h, arc in self.state['laser']:
        #     obs[x, y] = [255, 0, 0]
        x, y = self.state['player'][0], self.state['player'][1]
        _x, _y = self._x_y_transfer(x, y)
        w, h = 1, 1
        for _w in range(-w, w + 1):
            for _h in range(-h, h + 1):
                obs[_x + _w, _y + _h] = [0, 0, 255]
        obs = np.transpose(obs, (1, 0, 2))
        # obs = np.transpose(obs, (2, 0, 1))
        # img = Image.fromarray(obs)
        # end = time.time()
        # print(end - beg)
        # img.show()
        # img.save('game.png')
        return obs

    def _x_y_transfer(self, x, y, zoom_factor=4):
        return math.floor((x + 256) / zoom_factor), math.floor((y - 32 + 56) / zoom_factor)

    def render(self, mode='human'):
        # 环境可视化 暂时不需要 一定程度上拖累性能
        return None

    def close(self):
        # 环境清理 文件释放等等 无
        # self.f.close()  # 测试文件
        return None


if __name__ == "__main__":
    time.sleep(3)
    e = TouHouDistEnv()

    e._generate_observation()
