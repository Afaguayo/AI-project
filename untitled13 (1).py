# -*- coding: utf-8 -*-
"""Untitled13.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1i33As4fagA96cGch8jlNcW1AYRfHu__a
"""

!pip install gym-super-mario-bros nes-py torch torchvision numpy opencv-python matplotlib

import os
import gym
import gym_super_mario_bros
from gym_super_mario_bros.actions import SIMPLE_MOVEMENT
from nes_py.wrappers import JoypadSpace
import numpy as np
import cv2
import torch
import torch.nn as nn
import torch.optim as optim
from collections import deque
import random
import matplotlib.pyplot as plt

# Preprocess frame: resize and grayscale
def preprocess_frame(frame):
    frame = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
    frame = cv2.resize(frame, (84, 84))
    return frame / 255.0  # Normalize pixel values

# Create and preprocess environment
env = gym_super_mario_bros.make("SuperMarioBros-v0")
env = JoypadSpace(env, SIMPLE_MOVEMENT)

# Hyperparameters
EPISODES = 1
MAX_TIMESTEPS = 1000  # Maximum number of time steps per episode
GAMMA = 0.99
EPSILON = 1.0
EPSILON_MIN = 0.1
EPSILON_DECAY = 0.995
LEARNING_RATE = 0.001
MEMORY_SIZE = 2000
BATCH_SIZE = 64

# Deep Q-Network
class DQN(nn.Module):
    def __init__(self, state_shape, action_size):
        super(DQN, self).__init__()
        self.net = nn.Sequential(
            nn.Conv2d(4, 32, kernel_size=8, stride=4),
            nn.ReLU(),
            nn.Conv2d(32, 64, kernel_size=4, stride=2),
            nn.ReLU(),
            nn.Conv2d(64, 64, kernel_size=3, stride=1),
            nn.ReLU(),
            nn.Flatten(),
            nn.Linear(3136, 512),
            nn.ReLU(),
            nn.Linear(512, action_size)
        )

    def forward(self, x):
        return self.net(x)

# Initialize models
state_shape = (4, 84, 84)
action_size = env.action_space.n
model = DQN(state_shape, action_size)
target_model = DQN(state_shape, action_size)
target_model.load_state_dict(model.state_dict())  # Synchronize weights
optimizer = optim.Adam(model.parameters(), lr=LEARNING_RATE)
criterion = nn.MSELoss()

# Replay memory
memory = deque(maxlen=MEMORY_SIZE)

# Epsilon-greedy action selection
def select_action(state, epsilon):
    if np.random.rand() < epsilon:
        return random.randrange(action_size)
    state_tensor = torch.FloatTensor(state).unsqueeze(0)
    with torch.no_grad():
        q_values = model(state_tensor)
    return torch.argmax(q_values).item()

# Replay experience for training
def replay():
    if len(memory) < BATCH_SIZE:
        return
    minibatch = random.sample(memory, BATCH_SIZE)
    states, actions, rewards, next_states, dones = zip(*minibatch)

    states = torch.FloatTensor(states)
    next_states = torch.FloatTensor(next_states)
    actions = torch.LongTensor(actions)
    rewards = torch.FloatTensor(rewards)
    dones = torch.FloatTensor(dones)

    # Compute Q-learning targets
    with torch.no_grad():
        target_q = rewards + (1 - dones) * GAMMA * torch.max(target_model(next_states), dim=1)[0]
    current_q = model(states).gather(1, actions.unsqueeze(1)).squeeze()

    loss = criterion(current_q, target_q)
    optimizer.zero_grad()
    loss.backward()
    optimizer.step()

# Training loop with time step limit and checkpointing
os.makedirs("checkpoints", exist_ok=True)  # Ensure checkpoint directory exists
all_rewards = []

for episode in range(EPISODES):
    state = env.reset()
    state = preprocess_frame(state)
    state = np.stack([state] * 4, axis=0)  # Stack 4 frames
    total_reward = 0
    done = False

    for t in range(MAX_TIMESTEPS):  # Limit the number of steps per episode
        action = select_action(state, EPSILON)
        next_state, reward, done, info = env.step(action)
        next_state = preprocess_frame(next_state)
        next_state = np.append(state[1:], np.expand_dims(next_state, axis=0), axis=0)  # Update stacked state
        memory.append((state, action, reward, next_state, done))
        state = next_state
        total_reward += reward

        replay()  # Train the model

        if done:  # Break if the episode ends naturally
            break

    EPSILON = max(EPSILON_MIN, EPSILON * EPSILON_DECAY)
    all_rewards.append(total_reward)
    print(f"Episode {episode + 1}/{EPISODES}, Reward: {total_reward}, Epsilon: {EPSILON:.2f}")

    # Update target model every 10 episodes
    if episode % 10 == 0:
        target_model.load_state_dict(model.state_dict())

    # Save checkpoint every 50 episodes
    if (episode + 1) % 50 == 0:
        checkpoint_path = f"checkpoints/mario_dqn_episode_{episode + 1}.pth"
        torch.save(model.state_dict(), checkpoint_path)
        print(f"Checkpoint saved: {checkpoint_path}")

# Save the final model
torch.save(model.state_dict(), "mario_dqn_final.pth")
print("Final model saved as mario_dqn_final.pth")

# Plot training rewards
plt.plot(all_rewards)
plt.xlabel("Episode")
plt.ylabel("Reward")
plt.title("Training Rewards")
plt.show()

env.close()

import cv2
import gym
import gym_super_mario_bros
from gym_super_mario_bros.actions import SIMPLE_MOVEMENT
from nes_py.wrappers import JoypadSpace
import numpy as np
import torch
import torch.nn as nn

# Define the DQN model (same as in training)
class DQN(nn.Module):
    def __init__(self, state_shape, action_size):
        super(DQN, self).__init__()
        self.net = nn.Sequential(
            nn.Conv2d(4, 32, kernel_size=8, stride=4),
            nn.ReLU(),
            nn.Conv2d(32, 64, kernel_size=4, stride=2),
            nn.ReLU(),
            nn.Conv2d(64, 64, kernel_size=3, stride=1),
            nn.ReLU(),
            nn.Flatten(),
            nn.Linear(3136, 512),
            nn.ReLU(),
            nn.Linear(512, action_size)
        )

    def forward(self, x):
        return self.net(x)

# Preprocess frame: resize and grayscale
def preprocess_frame(frame):
    frame = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
    frame = cv2.resize(frame, (84, 84))
    return frame / 255.0  # Normalize pixel values

# Load the environment
env = gym_super_mario_bros.make("SuperMarioBros-v0")
env = JoypadSpace(env, SIMPLE_MOVEMENT)

# Set state shape and action size
state_shape = (4, 84, 84)
action_size = env.action_space.n

# Load the trained model
loaded_model = DQN(state_shape, action_size)
loaded_model.load_state_dict(torch.load("mario_dqn_final.pth"))
loaded_model.eval()  # Set the model to evaluation mode

# Initialize OpenCV video writer for MP4
video_filename = "mario_gameplay.mp4"
frame_width = 256  # Standard NES resolution width
frame_height = 240  # Standard NES resolution height
fps = 30  # Frames per second
fourcc = cv2.VideoWriter_fourcc(*"mp4v")  # H.264 codec for MP4
out = cv2.VideoWriter(video_filename, fourcc, fps, (frame_width, frame_height))

# Test the loaded model and save gameplay
for episode in range(1):  # Save video for 1 episode
    state = env.reset()
    state = preprocess_frame(state)
    state = np.stack([state] * 4, axis=0)  # Stack 4 frames
    total_reward = 0
    done = False

    while not done:
        # Render the environment and write each frame to video
        frame = env.render(mode="rgb_array")  # Get RGB frame
        out.write(cv2.cvtColor(frame, cv2.COLOR_RGB2BGR))  # Convert RGB to BGR for OpenCV

        # Convert state to tensor and select the best action
        state_tensor = torch.FloatTensor(state).unsqueeze(0)
        with torch.no_grad():
            action = torch.argmax(loaded_model(state_tensor)).item()

        # Step the environment
        next_state, reward, done, info = env.step(action)
        next_state = preprocess_frame(next_state)
        next_state = np.append(state[1:], np.expand_dims(next_state, axis=0), axis=0)  # Update state stack
        state = next_state
        total_reward += reward

    print(f"Test Episode: Total Reward: {total_reward}")

# Release the video writer and environment
out.release()
env.close()

print(f"Gameplay video saved as {video_filename}")

