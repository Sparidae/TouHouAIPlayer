import gym
from gym import spaces
import time
import numpy as np
import pydirectinput
from util.get_memory_data import GameData
from util.get_img_data import img_capture
from util.window import activate_window
from util.send_input import Keyboard
from cfg.constants import *
from cfg.config import *


class TouHouImageEnv(gym.Env):
    def __init__(self):
        # 定义状态空间和动作空间
        self.observation_space = spaces.Box(low=0.0, high=255.0, shape=(451, 385, 3))
        self.action_space = spaces.Discrete(10)  # 动作空间 0，1，2，3，4，5，6，7 八个方向 8 x清空范围弹幕短暂无敌 9 什么也不做

        # 定义状态 img数组
        self.state = img_capture()

        # 需要reset()重置的变量
        # step计数
        self.datasource = GameData()
        self.step_count = 0
        self.player_obs = self.datasource.get_player_data()

        # 测试score和power增量
        # self.f = open('increase.txt', 'w')
        # self.score_list = [0, ]
        # self.power_list = [0, ]
        pass

    def step(self, action):  # 用于编写智能体与环境交互的逻辑，它接受action的输入，给出下一时刻的状态、当前动作的回报、是否结束当前episode及调试信息
        reward = 0  # 本step奖励初始化
        self.step_count += 1  # 本回合执行的step量+1
        prev_obs = self.player_obs
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
            # self.x_inv_frames = MAX_X_INV_FRAME
        if action == 9:  # 什么也不做
            time.sleep(PRESS_INTERVAL)
            pass

        # 计算reward 移动奖励
        if action != 8:
            reward = MOVE_REWARD

        # 更新状态
        self.state = img_capture()
        self.player_obs = self.datasource.get_player_data()

        if self.player_obs['score'][0] > prev_obs['score'][0]:
            reward += 3
        if self.player_obs['power'][0] > prev_obs['power'][0]:
            reward += 2
        elif self.player_obs['power'][0] < prev_obs['power'][0]:
            reward += -4

        if self.player_obs['extra_life'][0] < prev_obs['extra_life'][0]:
            reward += (1+(3-1)*self.player_obs['score']/1_000_000)*(-300)

        # 判断是否终止
        done = self._is_done()

        # observation->state  reward->int  done->bool  info->dict
        return self.state, reward, done, {}

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
        self.state = img_capture()
        self.player_obs = self.datasource.get_player_data()
        return self.state

    def _is_done(self) -> bool:
        if self.player_obs['extra_life'][0] == -1:  # 死了
            return True
        else:
            return False

    def render(self, mode='human'):
        # 环境可视化 暂时不需要 一定程度上拖累性能
        return None

    def close(self):
        # 环境清理 文件释放等等 无
        # self.f.close()  # 测试文件
        return None


if __name__ == "__main__":
    time.sleep(3)
