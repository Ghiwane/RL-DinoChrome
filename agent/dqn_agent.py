from qnetwork import Qnetwork
from replay_buffer import ReplayBuffer
import torch
import numpy as np
import random
import torch.nn.functional as F

class DinoAgent:
    def __init__(self, state, action):
        self.q_network = Qnetwork(state, action)  # main network qui choisit l'action et apprend
        self.target_network = Qnetwork(state, action)  # target network qui evalue l'action choisit 
        self.target_network.load_state_dict(self.q_network.state_dict()) # on copie les differents poids du main network vers le target network

        self.optimizer = torch.optim.Adam(self.q_network.parameters(), lr=0.0005) # optimizer pour mettre à jour les poids 

        self.buffer = ReplayBuffer(capacity=500000) #replay buffer qui stock les steps passés  

        self.gamma = 0.999
        self.eps = 1.0
        self.eps_min = 0.001
        self.eps_decay = 0.999
        self.batch_size = 64
        self.n_actions = action
        self.n_step = 0
        self.target_update_freq = 10000 
        self.train_nstep = 4   

    def choose_action(self, state):
    # Epsilon-greedy
        rand_nb = np.random.rand()
        if rand_nb < self.eps:
            return random.choice(range(self.n_actions))  # une action random
        else:
            with torch.no_grad():
                state_tensor = torch.FloatTensor(state)
                return self.q_network(state_tensor).argmax().item() # meilleure action prédite

    def train_step(self):
        self.n_step += 1 
        
        # entrainement que tt les 4 steps
        if self.n_step % self.train_nstep == 0:
            # attend qu'il y ai assez de samples dans le buffer
            if len(self.buffer) < self.batch_size:
                return
            
            # Sample un random mini-batch depuis le buffer
            states, actions, rewards, next_states, dones = self.buffer.sample(self.batch_size)

            # Prédit les Q-values pour les states actuels et conserve les actions choisies
            q_values = self.q_network(states)
            selected_q_values = q_values.gather(1, actions)

            # Calcule les Target Q-values en utilisant la logique Double DQN
            with torch.no_grad():
                # 1. Le main network sélectionne la meilleure action pour le next state
                best_actions = self.q_network(next_states).argmax(dim=1, keepdim=True)
                
                # 2. Le target network évalue cette action sélectionnée
                max_next_q = self.target_network(next_states).gather(1, best_actions)
                
                # 3. Calcul de la target de Bellman (met à zéro les rewards futurs si l'épisode est done)
                target = rewards + self.gamma * max_next_q * (1 - dones.float())
            
            # MSE loss entre les Q-values prédites et les targets de Bellman
            loss = F.mse_loss(selected_q_values, target)

            # Met à jour périodiquement les poids du target network
            if self.n_step % self.target_update_freq == 0:
                self.update_target()

            # Backpropagation
            self.optimizer.zero_grad()
            loss.backward()
            torch.nn.utils.clip_grad_norm_(self.q_network.parameters(), max_norm=1.0)
            self.optimizer.step()

            return loss.item()

    def update_target(self):
        # Synchronise les poids du target network avec le main network
        self.target_network.load_state_dict(self.q_network.state_dict())

    def decay_epsilon(self):
        # Décroît l'exploration rate jusqu'à eps_min
        self.eps = max(self.eps_min, self.eps * self.eps_decay)

    def evaluate(self, env, n_episodes=10): # Évalue les performances de l'agent sans exploration (pure exploitation)
        total_rewards = []
        total_steps = []
        for _ in range(n_episodes):
            state = env.reset()
            done = False
            episode_reward = 0
            steps = 0
            while not done:
                with torch.no_grad():
                    state_tensor = torch.FloatTensor(state)
                    action = self.q_network(state_tensor).argmax().item()
                state, reward, done, info = env.step(action)
                episode_reward += reward
                steps += 1
            total_rewards.append(episode_reward)
            total_steps.append(steps)
        print(f"steps moyens: {np.mean(total_steps):.0f}, max: {max(total_steps)}")
        return np.mean(total_rewards)