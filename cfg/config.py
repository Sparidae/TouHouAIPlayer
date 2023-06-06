# 配置文件 存储参数

# 数据参数，规定了数据大小
MAX_POWERS = 2000  # 2000
MAX_ENEMY = 100  # 100
MAX_BULLET = 2000  # 2000
MAX_LASER = 250  # 250

# TouHou2D 控制SendInput的输入间隔
PRESS_INTERVAL = 0.02

# Reward
WALL_PUNISH = -6
MAX_SCORE_REWARD_RATE = 3 # 最高SCORE-reward倍率

# DQN模型参数
DQN_learning_rate = 0.0001  # *learning_rate参数是一个浮点数，表示学习率。它用于控制权重更新的速度。默认为1e-4
DQN_buffer_size = 10_000  # *一个整数，表示回放缓存的大小。它用于存储先前的观测和动作，以便在训练期间进行回放 默认为1_000_000
DQN_learning_starts = 10  # *一个整数，表示在开始训练之前需要填充回放缓存的时间步数 默认50_000
DQN_batch_size = 16  # *表示每个训练步骤中使用的样本数 32
DQN_tau = 1.0  # 软更新系数（"Polyak update"，介于0和1之间），默认为1，用于硬更新。
DQN_gamma = 0.99  # 表示折扣因子。它用于计算未来奖励的折现值。默认为0.99。越高可能越难训练
DQN_train_freq = 4  # 每隔 train_step 个 step 更新一次模型
DQN_gradient_steps = 1  # 每次rollout 需要多少个梯度step
DQN_optimize_memory_usage = False  # 以更高的复杂度为代价，实现重放缓冲区的内存效率变体默认False Dict不能用
DQN_target_update_interval = 250  # *每隔target_update_interval环境step更新目标网络。
DQN_exploration_fraction = 0.1  # 在整个训练期中，探索率降低的部分
DQN_exploration_initial_eps = 0.1  # 随机行动概率的初始值
DQN_exploration_final_eps = 0.05  # 随机行动概率的最终值
DQN_max_grad_norm = 10  # 梯度剪裁的最高值
DQN_stats_window_size = 100  # 展开记录的窗口大小
DQN_tensorboard_log = './log/tensorboard/'  # *创建tensorboard log
DQN_policy_kwargs = None  # * 创建时传递给policy的额外参数
DQN_device = 'cuda:0'  # gpu训练
DQN_verbose = 1
