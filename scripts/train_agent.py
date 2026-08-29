import matplotlib.pyplot as plt
import numpy as np
import random
import torch
import sys
import os

# 1. def of the seed function
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

# 2. apply the seed
set_seed(42)

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../agent')))
from dqn_agent import DinoAgent

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../dino_env')))
from env import DinoGame

# Create the Dino environment
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

collect_freq = 25
collect_step = 20000
collect_rewards =  []
old_eps = 1

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
            print(f'New best model saved | reward : ({eval_reward:.1f})\n')

    # Print training progress every 20 episodes
    if i % 10 == 0:
        print(f'\nEpisode : {i} | Score du jeu : {final_score:.1f} | Reward : {total_rewards} | Current epsilon : {agent.eps}')
        if len(losses) > 0:
            print(f"Loss: {losses[-1]:.4f}")

    if i % collect_freq == 0:
        state = env.reset()
        old_eps = agent.eps
        agent.eps = 0
        step = 0
        done = False
        truncated = False
        total_rewards = 0

        agent.collect_network.load_state_dict(torch.load("trained_model.pth"))

        while not (done or truncated):
            step+=1

            action = agent.choose_action(state, agent.collect_network)
            next_state, reward, done, truncated, info = env.step(action)
            agent.buffer.push(state, action, reward, next_state, done)

            loss = agent.train_step()
            if loss is not None:
                losses.append(loss)

            state = next_state
            total_rewards += reward  
            final_score = info['score']

            if step >= collect_step:
                truncated = True

        collect_rewards.append(total_rewards)
        agent.eps = old_eps
        print(f'\n---> COLLECT Episode {i} | Score : {final_score:.1f} | Collect reward : {total_rewards}\n')
        

os.makedirs("logs", exist_ok=True)
np.save("logs/episode_rewards.npy", np.array(episode_rewards))
np.save("logs/collect_rewards.npy", np.array(collect_rewards))
np.save("logs/eval_episodes.npy", np.array(eval_episodes))
np.save("logs/eval_rewards.npy", np.array(eval_rewards))
np.save("logs/losses.npy", np.array(losses))