import gym
from gym import spaces
import time
import numpy as np
import pydirectinput
from util.get_memory_data import GameData
from util.window import activate_window
from cfg.config import *
from util.send_input import Keyboard
from cfg.constants import *


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
        self.action_space = spaces.Discrete(10)  # 动作空间 0，1，2，3，4，5，6，7 八个方向 8 x清空范围弹幕短暂无敌 9 什么也不做

        # 游戏数据源
        self.datasource = GameData()

        # 定义状态 依赖于datasource
        self.state = self._get_state()

        # 需要reset()重置的变量
        # step计数 无敌帧 score奖励倍率
        self.step_count = 0
        self.dead_inv_frames = 0  # 5s 死亡无敌40  x算30
        self.x_inv_frames = 0  # x 无敌惩罚 30帧
        self.score_reward_rate = 1

        # 测试score和power增量
        # self.f = open('increase.txt', 'w')
        # self.score_list = [0, ]
        # self.power_list = [0, ]
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
            reward = -10
            self.x_inv_frames = 30
        if action == 9:  # 什么也不做
            time.sleep(PRESS_INTERVAL)
            pass

        # 计算reward 移动奖励
        if action != 8:
            reward = 2

        # 计算reward 撞墙部分 未更新的状态+action说明已经撞墙 需要惩罚
        if self.state['player'][0] - (-184) < 1:  # 左墙
            if action in [2, 5, 6]:  # 左，左上，左下
                reward += WALL_PUNISH  # -6
        if 184 - self.state['player'][0] < 1:  # 右墙
            if action in [3, 4, 7]:  # 右，右上，右下
                reward += WALL_PUNISH
        if 432 - self.state['player'][1] < 1:  # 下墙
            if action in [1, 4, 6]:  # 下 左右下
                reward += WALL_PUNISH
        if self.state['player'][1] - 32 < 1:  # 上墙
            if action in [0, 5, 7]:  # 上 左右上
                reward += WALL_PUNISH

        # 更新状态
        self.state = self._get_state()

        # 判断是否终止
        done = self._is_done()

        # 计算reward 生命部分
        if self.state['extra_life'][0] < last_state['extra_life'][0]:  # 掉生命了
            reward = -300
            self.dead_inv_frames = 40
        elif self.state['extra_life'][0] > last_state['extra_life'][0]:  # 残机增加
            reward = 300

        # 计算reward score部分  步进奖励
        score_reward = 0
        delta_score = self.state['score'][0] - last_state['score'][0]
        if 100 < self.step_count < 10100:
            self.score_reward_rate = 1 + (MAX_SCORE_REWARD_RATE - 1) * (self.step_count - 100) / 10000  # 1-3 随着步数增加提升奖励
        if 0 < delta_score <= 500:  # 增分且小于500
            score_reward = 3
        elif delta_score > 500:
            score_reward = 2  # 不鼓励跑到最前面吃分
        score_reward = self.score_reward_rate * score_reward
        reward += score_reward

        # 计算reward power部分
        power_reward = 0
        delta_power = self.state['power'][0] - last_state['power'][0]
        if 0 < delta_power <= 10:  # 增power小于10 自己捡到的
            power_reward = 2
        elif delta_power > 10:  # 放大或者清空弹幕
            power_reward = 1  # 4
        reward += power_reward

        # 计算reward 无敌部分
        if self.dead_inv_frames > 0:  # 处于无敌帧内减reward
            reward += -2
            self.dead_inv_frames -= 1

        # 计算reward x无敌部分
        if self.x_inv_frames > 0:
            reward += -0.33
            self.x_inv_frames -= 1

        # 计算reward 触发线上惩罚
        if self.state['player'][1] < 130:  # 处于ItemGetBorderLine上
            reward += -2

        # 测试部分 增加的
        # self.score_list.append(self.state['score'][0] - last_state['score'][0])
        # self.power_list.append(self.state['power'][0] - last_state['power'][0])
        # print(self.state['player'][0] - last_state['player'][0],
        #       self.state['player'][1] - last_state['player'][1])

        # observation->state  reward->int  done->bool  info->dict
        return self.state, reward, done, {}

    def reset(self):
        # 游戏失败后重置游戏的操作
        print('---env.reset() is called---')
        # 重置变量
        self.step_count = 0
        self.dead_inv_frames = 0
        self.x_inv_frames = 0
        self.score_reward_rate = 1
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

        # '%d %d %d %d' print('%d %d %d %d' % (max(self.score_list), min(self.score_list), max(self.power_list),
        # min(self.power_list))) print('%.2f %.2f' % (sum(self.score_list) / len(self.score_list),
        # sum(self.power_list) / len(self.power_list)))
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
        # self.f.close()  # 测试文件
        return None


if __name__ == "__main__":
    time.sleep(3)
