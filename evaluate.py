import os
from stable_baselines3 import DQN
from stable_baselines3 import PPO
from game_env.touhou_env import TouHouEnv
from game_env.touhou_dist_env import TouHouDistEnv
import time
from util.window import activate_window
import pydirectinput

# 读取模型
env = TouHouDistEnv()  # !!
model_dir = '2023-06-09_01-49m'  # 要查看的模型路径
model_path = os.path.join('model', model_dir, 'TouHouAI')
# model = DQN.load(model_path)
model = PPO.load(model_path)

# 准备工作
print('---evaluation will start in 2 seconds---')
time.sleep(2)
activate_window()  # 激活窗口
pydirectinput.keyDown('z')

# 评估
state = env.reset()
done = False
score = 0
while not done:  # 运行时运行模型
    action, _ = model.predict(observation=state)
    state, reward, done, info = env.step(action=action)
    score += reward
env.close()

print(score)
