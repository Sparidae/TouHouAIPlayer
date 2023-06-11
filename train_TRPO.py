from sb3_contrib import TRPO
import os
import time
import torch.nn
from stable_baselines3 import PPO
from stable_baselines3.common.evaluation import evaluate_policy
import pydirectinput
from game_env.touhou_env import TouHouEnv
from game_env.touhou_img_env import TouHouImageEnv
from game_env.touhou_dist_env import TouHouDistEnv
from util.window import activate_window
from util.helpers import *
from util.CustomCNN import CustomCNN

# 是否需要保存模型和日志小开关 测试不需要输出时可用False
to_file = True
has_trained_before = False
env_choice = 3

# 引入环境
env = TouHouEnv() if env_choice == 1 else TouHouImageEnv() if env_choice == 2 else TouHouDistEnv()
time_str = get_timestr()
model_path = os.path.join('model', time_str, 'TouHouAI').replace("\\", "/")  # 相对路径
buffer_path = os.path.join('model', time_str, 'TouHouAI_buffer').replace("\\", "/")
print('model_path:', model_path)
model = None
mean_reward = -100_000
mean_reward_prev = -1_000_000
std_reward = 0
std_reward_prev = 0
policy_kwargs = dict(
    features_extractor_class=CustomCNN,
    features_extractor_kwargs=dict(features_dim=512),
) if env_choice == 2 else dict(activation_fn=torch.nn.Tanh, net_arch=[256, 256, 256])
policy_kwargs = None

model = TRPO(policy="CnnPolicy" if env_choice in [2, 3] else "MultiInputPolicy",
             env=env,
             learning_rate=1e-3,  # *learning_rate参数是一个浮点数，表示学习率。它用于控制权重更新的速度。默认为1e-4
             batch_size=128,  # *表示每个训练步骤中使用的样本数 128
             n_steps=2048,  # 每次更新时运行每个环境的步数，即回合缓冲区大小是n_steps * n_envs，其中n_envs是并行运行的环境数。
             # 注意：n_steps * n_envs必须大于1（因为需要进行优势归一化）。
             gamma=0.99,  # 表示折扣因子。它用于计算未来奖励的折现值。默认为0.99。越高可能越难训练
             gae_lambda=0.95,  # 广义优势估计（GAE）中偏差与方差的权衡因子
             normalize_advantage=True,  # 是否对优势进行归一化
             use_sde=False,  # 是否使用广义状态相关探索（gSDE）而不是动作噪声探索（默认值为False）
             sde_sample_freq=-1,  # 使用gSDE时每n步采样一个新的噪声矩阵。默认值为-1（仅在回合开始时采样）
             stats_window_size=100,  # 回合记录日志的窗口大小，指定要平均报告的成功率、平均回合长度和平均奖励的回合数。
             tensorboard_log='./log/tensorboard/' if to_file else None,  # *创建tensorboard log
             policy_kwargs=policy_kwargs,  # * 创建时传递给policy的额外参数
             device='cuda:0',  # gpu训练
             verbose=1)

if not to_file:
    print('---Warning:Model&Log will not be saved---')
print('---Training will start in 2 seconds---')
time.sleep(2)
activate_window()  # 激活窗口
if has_trained_before:
    env.reset()
else:
    pydirectinput.press('enter')
    has_trained_before = True
pydirectinput.keyDown('z')
pydirectinput.keyDown('ctrl')  # 尝试是否管用能跳过剧情

# 训练 total_timesteps 表示采样的数量 即训练使用的state的数量
model.learn(total_timesteps=65536, tb_log_name='TRPO' + get_short_timestr())

# 模型评估evaluate
# n_eval_episodes 表示测试回合的总数，用于计算模型的平均奖励和标准偏差。默认值为10
mean_reward_prev, std_reward_prev = mean_reward, std_reward
mean_reward, std_reward = evaluate_policy(model, env, n_eval_episodes=10, render=False)
print(mean_reward, std_reward)  # 多step中reward的平均值和标准差
