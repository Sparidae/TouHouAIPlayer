import os
from stable_baselines3 import DQN
from stable_baselines3.common.evaluation import evaluate_policy
from util.touhouEnv import TouHouEnv
import time
from util.window import activate_window
import pydirectinput

# 读取模型
env = TouHouEnv()  # !!
model_dir = '2023-06-06_18-27m'  # 要查看的模型路径
model_path = os.path.join('model', model_dir, 'TouHouAI')
model = DQN.load(model_path)

# 准备工作
print('---evaluation will start in 2 seconds---')
time.sleep(2)
activate_window()  # 激活窗口
pydirectinput.press('enter')
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
