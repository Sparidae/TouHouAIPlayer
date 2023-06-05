import gym
from gym import spaces
import time
import numpy as np
import pydirectinput
from util.get_memory_data import GameData
from util.window import activate_window
from util.config import *
from util.send_input import Keyboard
from util.constants import *

class TouHouEnv(gym.Env):
    def __init__(self):
        # 定义一些控制参数
        self._X = 200  # x坐标的左右上限  184和-184
        self._PY = 450  # y坐标的上限 实为432
        self._NY = 0  # y坐标的下限 32
        self._ARC = 3.2  # 角度的 -pi~pi

        # 定义状态空间和动作空间
        self.observation_space = spaces.Dict({
            'powers': spaces.Box(low=np.array(MAX_POWERS * [[-self._X, self._NY, 0, 0]]),
                                 high=np.array(MAX_POWERS * [[self._X, self._PY, 100, 100]]),
                                 shape=(MAX_POWERS, 4)),
            'enemy': spaces.Box(low=np.array(MAX_ENEMY * [[-self._X, self._NY, 0, 0]]),
                                high=np.array(MAX_ENEMY * [[self._X, self._PY, 100, 100]]),
                                shape=(MAX_ENEMY, 4)),
            'bullet': spaces.Box(low=np.array(MAX_BULLET * [[-self._X, self._NY, 0, 0, 0, 0]]),
                                 high=np.array(MAX_BULLET * [[self._X, self._PY, 100, 100, 100, 100]]),
                                 shape=(MAX_BULLET, 6)),
            'laser': spaces.Box(low=np.array(MAX_LASER * [[-self._X, self._NY, 0, 0, -self._ARC]]),
                                high=np.array(MAX_LASER * [[self._X, self._PY, 100, 100, self._ARC]]),
                                shape=(MAX_LASER, 5)),
            'player': spaces.Box(low=np.array([-self._X, self._NY]), high=np.array([self._X, self._PY]), shape=(2,)),
            'score': spaces.Box(low=0, high=100_000_000, shape=(1,)),  # !警惕Discrete 会申请大量内存
            'power': spaces.Box(low=0, high=101, shape=(1,)),
            'extra_life': spaces.Box(low=0, high=10, shape=(1,)),
        })
        self.action_space = spaces.Discrete(9)  # 状态空间 0，1，2，3 上下左右 4，5，6，7 shift 变慢并收束子弹 8 x对应消耗1p清空弹幕并无敌一段时间

        # 游戏数据源
        self.datasource = GameData()

        # 定义状态 依赖于datasource
        self.state = self._get_state()

        # 计数
        self.counts = 0
        pass

    def step(self, action):  # 用于编写智能体与环境交互的逻辑，它接受action的输入，给出下一时刻的状态、当前动作的回报、是否结束当前episode及调试信息
        reward = 0
        # 记录执行动作前的状态
        last_state = self.state
        # action动作
        if action == 0:  # 上
            Keyboard.pressByScanCode(SC_UP)
            time.sleep(PRESS_INTERVAL)
            Keyboard.releaseByScanCode(SC_UP)
            reward = 2
        if action == 1:  # 下
            Keyboard.pressByScanCode(SC_DOWN)
            time.sleep(PRESS_INTERVAL)
            Keyboard.releaseByScanCode(SC_DOWN)
            reward = 2
        if action == 2:  # 左
            Keyboard.pressByScanCode(SC_LEFT)
            time.sleep(PRESS_INTERVAL)
            Keyboard.releaseByScanCode(SC_LEFT)
            reward = 2
        if action == 3:  # 右
            Keyboard.pressByScanCode(SC_RIGHT)
            time.sleep(PRESS_INTERVAL)
            Keyboard.releaseByScanCode(SC_RIGHT)
            reward = 2
        if action == 4:  # shift上
            Keyboard.pressByScanCode(SC_SHIFT)
            Keyboard.pressByScanCode(SC_UP)
            time.sleep(PRESS_INTERVAL)
            Keyboard.releaseByScanCode(SC_UP)
            Keyboard.releaseByScanCode(SC_SHIFT)
            reward = 2
        if action == 5:  # shift下
            Keyboard.pressByScanCode(SC_SHIFT)
            Keyboard.pressByScanCode(SC_DOWN)
            time.sleep(PRESS_INTERVAL)
            Keyboard.releaseByScanCode(SC_DOWN)
            Keyboard.releaseByScanCode(SC_SHIFT)
            reward = 2
        if action == 6:  # shift左
            Keyboard.pressByScanCode(SC_SHIFT)
            Keyboard.pressByScanCode(SC_LEFT)
            time.sleep(PRESS_INTERVAL)
            Keyboard.releaseByScanCode(SC_LEFT)
            Keyboard.releaseByScanCode(SC_SHIFT)
            reward = 2
        if action == 7:  # shift右
            Keyboard.pressByScanCode(SC_SHIFT)
            Keyboard.pressByScanCode(SC_RIGHT)
            time.sleep(PRESS_INTERVAL)
            Keyboard.releaseByScanCode(SC_RIGHT)
            Keyboard.releaseByScanCode(SC_SHIFT)
            reward = 2
        if action == 8:  # x
            Keyboard.pressByScanCode(SC_X)
            time.sleep(0.01)
            Keyboard.releaseByScanCode(SC_X)
            reward = -20

        # 更新状态
        self.state = self._get_state()

        # 判断是否终止
        done = self._is_done()

        # 计算reward奖励
        if self.state['extra_life'][0] < last_state['extra_life'][0]:  # 掉生命了
            reward = -200
        else:
            if self.state['score'][0] > last_state['score'][0]:  # 涨分了 和分数挂钩？ 分数不会下降
                reward += 2
            if self.state['power'][0] > last_state['power'][0]:  # power提升 和power挂钩？
                reward += 2

        # 智能体agent 与 环境environment、状态states、动作actions、回报rewards等等
        # observation->state  reward->int  done->bool  info->dict
        return self.state, reward, done, {}

    def reset(self):
        # 游戏失败后重置游戏的操作
        print('---env.reset() is called---')
        self.counts = 0
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
        return self.state

    def _get_state(self) -> dict:
        return self.datasource.get_formatted_data()

    def _is_done(self) -> bool:
        if self.state['extra_life'][0] == -1:  # 死了
            return True
        else:
            return False

    def render(self, mode='human'):
        # 环境可视化 暂时不需要 一定程度上拖累性能
        return None

    def close(self):
        # 环境清理 文件释放等等 无
        return None



if __name__ == "__main__":
    time.sleep(3)

