from collections import deque
import random
import torch
import numpy as np

# Replay memory buffer pour stocker et échantillonner les transitions d'expériences passées
class ReplayBuffer():
    def __init__(self, capacity):
        # File à double entrée (deque) avec capacité fixe (supprime automatiquement les éléments les plus anciens)
        self.buffer = deque(maxlen=capacity)

    def __len__(self):
        # Renvoie le nombre total de transitions stockées
        return len(self.buffer)

    def push(self, state, action, reward, next_state, done):
        # Sauvegarde une transition d'un seul pas de temps dans le buffer
        self.buffer.append((state, action, reward, next_state, done))

    def sample(self, batch_size):
        # Échantillonne aléatoirement un mini-batch de transitions
        batch = random.sample(self.buffer, batch_size)
        
        # Décompresse les éléments du tuple dans des listes séparées
        states, actions, rewards, next_states, dones = zip(*batch)

        # Convertit les tableaux et listes en Float et Long tensors PyTorch
        states = torch.FloatTensor(np.array(states))
        actions = torch.LongTensor(actions).unsqueeze(1)          # Shape: (batch_size, 1)
        rewards = torch.FloatTensor(rewards).unsqueeze(1)        # Shape: (batch_size, 1)
        next_states = torch.FloatTensor(np.array(next_states))
        dones = torch.tensor(dones, dtype=torch.float32).unsqueeze(1)  # Shape: (batch_size, 1)
        
        return states, actions, rewards, next_states, dones