# STG(弹幕射击游戏)AI

开发中

---

## 介绍

基于强化学习模型训练的弹幕游戏AI，以《东方风神录》为例

## 环境安装

```bash
conda create -n touhou python=3.8.16
conda activate touhou

conda install pytorch==1.11.0 torchvision==0.12.0 torchaudio==0.11.0 cudatoolkit=11.3
conda install numpy 

pip install psutil # 检测进程
pip install pillow # 图像处理
pip install pywin32 # win32api
pip install pydirectinput # 模拟输入
pip install stable_baselines3 # 包含gym
pip install sb3-contrib  
```

## 使用方法

打开th10chs.exe,停留在一步enter即可开始游戏的环境，启动脚本
默认训练为normal->灵梦->前方集中装备

## 查看log信息

```bash
conda activate touhou
tensorboard --logdir .\log\tensorboard\  查看log
```

## 保存的模型环境

== SAVED MODEL SYSTEM INFO ==

- OS: Windows-10-10.0.22631-SP0 10.0.22631
- Python: 3.8.16
- Stable-Baselines3: 1.8.0
- PyTorch: 1.11.0
- GPU Enabled: True
- Numpy: 1.23.5
- Gym: 0.21.0



