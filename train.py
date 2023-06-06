import os
import time
import torch.nn
from stable_baselines3 import DQN
from stable_baselines3.common.evaluation import evaluate_policy
import pydirectinput
from util.touhou2D import TouHouEnv
from util.window import activate_window
from util.helpers import get_timestr

model = None
mean_reward = -1_000
mean_reward_prev = -1_000_000
std_reward = 0
std_reward_prev = 0
policy_kwargs = dict(activation_fn=torch.nn.Tanh, net_arch=[256, 256])

# 是否需要保存模型和日志小开关 测试不需要输出时可用False
to_file = True

# 引入环境
env = TouHouEnv()
time_str = get_timestr()
model_path = os.path.join('model', time_str, 'TouHouAI').replace("\\", "/")  # 相对路径
buffer_path = os.path.join('model', time_str, 'TouHouAI_buffer').replace("\\", "/")
print('model_path:', model_path)

# Loop Start
while mean_reward > mean_reward_prev:
    # 当表现比上次训练的好
    if model is None:  # 第一轮训练 创建模型
        # 创建模型 需要调参！4
        model = DQN(policy="MultiInputPolicy",  # 对spaces.dict必须是MultiInputPolicy CnnPolicy
                    env=env,
                    learning_rate=0.0005,  # *learning_rate参数是一个浮点数，表示学习率。它用于控制权重更新的速度。默认为1e-4
                    buffer_size=20_000,  # *一个整数，表示回放缓存的大小。它用于存储先前的观测和动作，以便在训练期间进行回放 默认为1_000_000
                    learning_starts=100,  # *一个整数，表示在开始训练之前需要填充回放缓存的时间步数 默认50_000
                    batch_size=64,  # *表示每个训练步骤中使用的样本数 32
                    tau=1.0,  # 软更新系
                    # 数（"Polyak update"，介于0和1之间），默认为1，用于硬更新。
                    gamma=0.99,  # 表示折扣因子。它用于计算未来奖励的折现值。默认为0.99。越高可能越难训练
                    train_freq=4,  # 每隔 train_step 个 step 更新一次模型
                    gradient_steps=1,  # 每次rollout 需要多少个梯度step
                    target_update_interval=250,  # *每隔target_update_interval环境step更新 目标网络。
                    exploration_fraction=0.4,  # 在整个训练期中，探索率降低部分的占比
                    exploration_initial_eps=0.15,  # 随机行动概率的初始值
                    exploration_final_eps=0.05,  # 随机行动概率的最终值
                    max_grad_norm=10,  # 梯度剪裁的最高值
                    stats_window_size=100,  # 展开记录的窗口大小
                    tensorboard_log='./log/tensorboard/'if to_file else None,  # *创建tensorboard log
                    policy_kwargs=policy_kwargs,  # * 创建时传递给policy的额外参数
                    device='cuda:0',  # gpu训练
                    verbose=1)
    else:  # 第二轮之后的训练
        model = DQN.load(model_path, env=env, print_system_info=True)
        model.load_replay_buffer(buffer_path)

    # 准备工作
    if not to_file:
        print('---Warning:Model&Log will not be saved---')
    print('---Training will start in 2 seconds---')
    time.sleep(2)
    activate_window()  # 激活窗口
    pydirectinput.press('enter')
    pydirectinput.keyDown('z')
    pydirectinput.keyDown('ctrl')  # 尝试是否管用能跳过剧情

    # 训练 total_timesteps 表示采样的数量 即训练使用的state的数量
    model.learn(total_timesteps=20_000)

    # 模型评估evaluate
    # n_eval_episodes 表示测试回合的总数，用于计算模型的平均奖励和标准偏差。默认值为10
    mean_reward_prev, std_reward_prev = mean_reward, std_reward
    mean_reward, std_reward = evaluate_policy(model, env, n_eval_episodes=10, render=False)
    print(mean_reward, std_reward)  # 多step中reward的平均值和标准差

    # 判断是否更优优则存储
    if mean_reward > mean_reward_prev and to_file:
        model.save(model_path)
        model.save_replay_buffer(buffer_path)
        env = model.get_env()

    # 释放按键
    pydirectinput.keyUp('z')
    pydirectinput.keyUp('ctrl')

    if not to_file:
        break

# LoopEnd
env.close()

