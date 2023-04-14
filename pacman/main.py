import gym
import numpy as np
import matplotlib.pyplot as plt
import torch
import random as r

env = gym.make("MsPacman-v4", render_mode='human')
env.reset()

stepmode = False
phase = 0
counter = 0
for _ in range(10000):
    # env.action_space.n |=> 9
    # env.get_action_meanings() |=> ['NOOP', 'UP', 'RIGHT', 'LEFT', 'DOWN', 'UPRIGHT', 'UPLEFT', 'DOWNRIGHT', 'DOWNLEFT']

    if phase == 0:
        next_state, reward, terminated, truncated, info = env.step(4)
        counter += 1
        if counter == 120:
            phase += 1
            counter = 0
    if phase == 1:
        next_state, reward, terminated, truncated, info = env.step(3)
        counter += 1
        if counter >= 80:
            phase += 1
            counter = 0
    if phase == 2:
        counter += 1
        next_state, reward, terminated, truncated, info = env.step(1)
        if reward == 50:
            phase += 1
            counter = 0
    if phase == 3:
        counter += 1
        input(f'continue {counter}')
        
        next_state, reward, terminated, truncated, info = env.step(0)
        
    env.render()
    print(phase)
    
env.close()