
# STG(弹幕射击游戏)AI

## 环境

== SAVED MODEL SYSTEM INFO ==
- OS: Windows-10-10.0.22631-SP0 10.0.22631
- Python: 3.8.16
- Stable-Baselines3: 1.8.0
- PyTorch: 1.11.0
- GPU Enabled: True
- Numpy: 1.23.5
- Gym: 0.21.0

## 测试

获取数据速度  次/s
训练速度 step/s


## reward思路

放大扣分
死亡扣多
鼓励移动

## 调整模拟点击，加快反应速度

子线程按键
换方法模拟按键

## 待办

- [ ] 调参数 改操作游戏逻辑
- [ ] 找到合适的reward


## 优化方向

- [ ] gamedata部分使用原生numpy数组而非对象以减少开销
- [ ] sendinput()减少输入延迟
- [ ] 使用取色脚本或者图像识别进行正确的游戏重置操作
- [ ] 代码重构 常量整理到文件中

## 查看log信息

```bash
conda activate touhou
tensorboard --logdir .\log\tensorboard\  查看log
```


## 环境安装

```bash
conda create -n touhou python=3.8.16
conda activate touhou

conda install pytorch==1.11.0 torchvision==0.12.0 torchaudio==0.11.0 cudatoolkit=11.3

pip install psutil
pip install pywin32 # 可以不用
pip install pydirectinput 
pip install stable_baselines3
```

## 运行

