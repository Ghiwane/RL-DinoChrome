import matplotlib.pyplot as plt
import numpy as np
import random
import torch
import sys
import os

# 1. Définition de la fonction de seed
def set_seed(seed=42):
    """Fixe la seed pour garantir la reproductibilité de l'entraînement."""
    random.seed(seed)
    os.environ['PYTHONHASHSEED'] = str(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    if torch.cuda.is_available():
        torch.cuda.manual_seed(seed)
        torch.cuda.manual_seed_all(seed)
    torch.backends.cudnn.deterministic = True
    torch.backends.cudnn.benchmark = False

# 2. Application de la seed AVANT de charger tes propres modules
set_seed(42)

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../agent')))
from dqn_agent import DinoAgent

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../dino_env')))
from env import DinoGame

# Create the CartPole (Dino) environment
env = DinoGame()

# Reset the environment to get the first state
state = env.reset()

# Initialize the agent
agent = DinoAgent(5, 3)

# Training settings
episodes = 4000
episode_rewards = []
eval_episodes = []
eval_rewards = []
losses = []

best_eval_reward = -float('inf')
eval_freq = 100  # Evaluate every 100 episodes

print(f"Entraînement sur : {torch.cuda.get_device_name(0) if torch.cuda.is_available() else 'CPU'}")

# Main training loop
for i in range(episodes):
    state = env.reset()
    total_rewards = 0
    final_score = 0
    done = False
    truncated = False

    # Play one full episode
    while not (done or truncated):
        # Choose action (exploration vs exploitation)
        action = agent.choose_action(state)
        
        # Take action in the environment
        next_state, reward, done, truncated, info = env.step(action)
        
        # Save experience in the replay buffer
        agent.buffer.push(state, action, reward, next_state, done)
        
        # Train the neural network on a mini-batch
        loss = agent.train_step()
        if loss is not None:
            losses.append(loss)
        
        # Move to the next state
        state = next_state
        total_rewards += reward  
        final_score = info['score']

    # Reduce exploration rate (epsilon) after each episode
    agent.decay_epsilon()
    episode_rewards.append(total_rewards)
    
    # Evaluate the agent periodically
    if i % eval_freq == 0:
        eval_reward = agent.evaluate(env, n_episodes=10)
        eval_episodes.append(i)
        eval_rewards.append(eval_reward)
        print(f'Episode eval {i} | reward : {eval_reward:.1f}')
        
        # Save the model if it achieves a new best score
        if eval_reward > best_eval_reward:
            best_eval_reward = eval_reward
            torch.save(agent.q_network.state_dict(), "trained_model.pth")
            print(f'New best model saved | reward : ({eval_reward:.1f})')

    # Print training progress every 20 episodes
    if i % 20 == 0:
        print(f'Episode : {i} | Score du jeu : {final_score:.1f} | Reward : {total_rewards} | Current epsilon : {agent.eps}')
        if len(losses) > 0:
            print(f"Loss: {losses[-1]:.4f}")

os.makedirs("logs", exist_ok=True)
np.save("logs/episode_rewards.npy", np.array(episode_rewards))
np.save("logs/eval_episodes.npy", np.array(eval_episodes))
np.save("logs/eval_rewards.npy", np.array(eval_rewards))
np.save("logs/losses.npy", np.array(losses))