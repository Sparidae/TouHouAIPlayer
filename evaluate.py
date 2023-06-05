from stable_baselines3 import DQN
from stable_baselines3.common.evaluation import evaluate_policy
from util.touhou2D import TouHouEnv
import time
from util.window import activate_window
import pydirectinput

# 读取模型
env = TouHouEnv()  # !!
model = DQN.load("model/6.5 20wtstp 0.2-0.1/TouhouAI.pkl")

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

