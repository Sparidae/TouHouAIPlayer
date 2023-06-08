import torch

# 配置文件 存储参数

# TouHouEnv环境参数，规定了数据大小，必要情况下（如内存不足）可修改数量，但可能会面临信息丢失导致的模型效果一般
MAX_POWERS = 300  # 2000
MAX_ENEMY = 30  # 100
MAX_BULLET = 500  # 2000
MAX_LASER = 50  # 250

# TouHouEnv 控制SendInput的输入间隔
PRESS_INTERVAL = 0.01

# TouHouEnv
MAX_DEAD_INV_FRAME = 40  # 死亡无敌帧step
MAX_X_INV_FRAME = 30  # x无敌帧step

# Reward
DEAD_INV_PUNISH = -2  # 死亡无敌惩罚
X_INV_PUNISH = -0.33  # x无敌惩罚
X_INSTANT_PUNISH = -10  # x的即时惩罚
MOVE_REWARD = 2  # 移动奖励
DEAD_PUNISH = -300  # 失去生命惩罚
OBTAIN_LIFE_REWARD = 300  # 获得生命奖励
WALL_PUNISH = -10  # 撞墙的惩罚
MAX_SCORE_REWARD_RATE = 3  # 最高SCORE-reward倍率
SCORE_INCREASE_1 = 2  # 增分小于500部分
SCORE_INCREASE_2 = 1  # 大于500部分
POWER_INCREASE_1 = 2  # 增小于10
POWER_INCREASE_2 = 1  # 增加大于10
BORDER_LINE_PUNISH = -6  # 处于边界线上的代价

# DQN模型HyperParameters
DQN_learning_rate = 0.0005  # *learning_rate参数是一个浮点数，表示学习率。它用于控制权重更新的速度。默认为1e-4
DQN_buffer_size = 20_000  # *一个整数，表示回放缓存的大小。它用于存储先前的观测和动作，以便在训练期间进行回放 默认为1_000_000
DQN_learning_starts = 100  # *一个整数，表示在开始训练之前需要填充回放缓存的时间步数 默认50_000
DQN_batch_size = 128  # *表示每个训练步骤中使用的样本数 32
DQN_tau = 1.0  # 软更新系数（"Polyak update"，介于0和1之间），默认为1，用于硬更新。
DQN_gamma = 0.99  # 表示折扣因子。它用于计算未来奖励的折现值。默认为0.99。越高可能越难训练
DQN_train_freq = 4  # 每隔 train_step 个 step 更新一次模型
DQN_gradient_steps = 1  # 每次rollout 需要多少个梯度step
DQN_target_update_interval = 250  # *每隔target_update_interval环境step更新目标网络。
DQN_exploration_fraction = 0.4  # 在整个训练期中，探索率降低的部分
DQN_exploration_initial_eps = 0.15  # 随机行动概率的初始值
DQN_exploration_final_eps = 0.05  # 随机行动概率的最终值
DQN_max_grad_norm = 10  # 梯度剪裁的最高值
DQN_stats_window_size = 100  # 展开记录的窗口大小
DQN_tensorboard_log = './log/tensorboard/'  # *创建tensorboard log
DQN_policy_kwargs = dict(activation_fn=torch.nn.Tanh, net_arch=[128, 128, 64, 64, 32])  ## * 创建时传递给policy的额外参数
DQN_device = 'cuda:0'  # gpu训练
DQN_verbose = 2  # 0无1正常2调试
# DQN训练评估
TotalTimeSteps = 20_000
EvalEpisodes = 10
