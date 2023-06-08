from typing import Dict, List, Tuple, Type, Union
import numpy as np
import gym
import torch as th
from gym import spaces
from stable_baselines3.common.torch_layers import BaseFeaturesExtractor
from torch import nn
import torch
from stable_baselines3.common.preprocessing import get_flattened_obs_dim, is_image_space
from stable_baselines3.common.type_aliases import TensorDict
from stable_baselines3.common.utils import get_device


class CustomCNN(BaseFeaturesExtractor):
    """

    对stable-baselines中的cnn模型参数进行了修改，简化了cnn网络来降低计算量
    具体地，减少一层卷积，并降低了最后一层的参数，降低了features_dim

    使用：
    policy_kwargs = dict(
    features_extractor_class=CustomCNN,
    features_extractor_kwargs=dict(features_dim=128),
)

    :param observation_space:
    :param features_dim: Number of features extracted.
        This corresponds to the number of unit for the last layer.
    :param normalized_image: Whether to assume that the image is already normalized
        or not (this disables dtype and bounds checks): when True, it only checks that
        the space is a Box and has 3 dimensions.
        Otherwise, it checks that it has expected dtype (uint8) and bounds (values in [0, 255]).
    """

    def __init__(
        self,
        observation_space: spaces.Box,
        features_dim: int = 256,  # 512
        normalized_image: bool = False,
    ) -> None:
        super().__init__(observation_space, features_dim)
        # We assume CxHxW images (channels first)
        # Re-ordering will be done by pre-preprocessing or wrapper
        assert is_image_space(observation_space, check_channels=False, normalized_image=normalized_image), (
            "You should use NatureCNN "
            f"only with images not with {observation_space}\n"
            "(you are probably using `CnnPolicy` instead of `MlpPolicy` or `MultiInputPolicy`)\n"
            "If you are using a custom environment,\n"
            "please check it using our env checker:\n"
            "https://stable-baselines3.readthedocs.io/en/master/common/env_checker.html.\n"
            "If you are using `VecNormalize` or already normalized channel-first images "
            "you should pass `normalize_images=False`: \n"
            "https://stable-baselines3.readthedocs.io/en/master/guide/custom_env.html"
        )
        n_input_channels = observation_space.shape[0]
        self.cnn = nn.Sequential(
            nn.Conv2d(n_input_channels, 16, kernel_size=4, stride=2, padding=0),
            nn.ReLU(),
            # nn.Conv2d(32, 64, kernel_size=4, stride=2, padding=0),
            # nn.ReLU(),
            # nn.Conv2d(64, 64, kernel_size=3, stride=1, padding=0),
            # nn.ReLU(),
            nn.Conv2d(16, 32, kernel_size=3, stride=1, padding=0),  # new add
            nn.ReLU(),
            nn.Flatten(),
        )

        # Compute shape by doing one forward pass
        with th.no_grad():
            n_flatten = self.cnn(th.as_tensor(observation_space.sample()[None]).float()).shape[1]

        self.linear = nn.Sequential(nn.Linear(n_flatten, features_dim), nn.ReLU())

    def forward(self, observations: th.Tensor) -> th.Tensor:
        # observations = torch.tensor([obs.sample() for obs in observations], dtype=torch.float32)
        return self.linear(self.cnn(observations))
