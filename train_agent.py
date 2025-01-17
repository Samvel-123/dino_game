from stable_baselines3 import DQN
from stable_baselines3.common.env_util import make_vec_env
import imageio
from stable_baselines3.common.callbacks import BaseCallback
import numpy as np
from env import DinoGame
import gymnasium as gym
import pygame

# Tool to track the learning progress
class RewardLoggerCallback(BaseCallback):
    def __init__(self):
        super(RewardLoggerCallback, self).__init__()
        self.rewards = []

    def _on_step(self) -> bool:
        # Record the reward of the current step
        self.rewards.append(self.locals["rewards"])
        return True

           # Գրանցում ենք միջավայրը Gym-ում
gym.envs.registration.register(
    id='DinoGame-v0',
    entry_point='__main__:DinoGame',
)

# TODO: Think back to the Q-Learning notebook. How can we initialize the environment?
env = gym.make("DinoGame")

# Set up the DQN model
model = DQN("MlpPolicy", env, verbose=1, learning_rate=0.0001, buffer_size=100000, batch_size=32)

# TODO: Try some timesteps. How long does 10 steps take. 100? 1000? Then finally try 100000.
timesteps = 800000

# Training the model
reward_callback = RewardLoggerCallback()
model.learn(total_timesteps=timesteps, callback=reward_callback)

# Step 5: Save the model
model_path = "game"
model.save(model_path)

# Visualize the trained model
env = gym.make("DinoGame") ## Was wrong; was originally env.make
obs, _ = env.reset()

frames = []

# Run the game through our learned policy
for _ in range(1000000):
    # Get our action from our learned policy
    action, _ = model.predict(obs, deterministic=True)

    # TODO: How can we take a step using our action?
    obs, reward, done, truncated, info = env.step(action)

    # Render the current state to a Pygame surface and capture it as a frame
    screen = env.render()
    frame = pygame.surfarray.array3d(screen)
    frame = frame.swapaxes(0, 1)
    frames.append(frame)

    if done:
        break

# Save the frames as a GIF
gif_path = "game.gif"
imageio.mimsave(gif_path, frames, fps=60)

# Output the GIF in Colab
from IPython.display import Image
Image(filename=gif_path)