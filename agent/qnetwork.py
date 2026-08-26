import torch.nn as nn

class Qnetwork(nn.Module):
    def __init__(self, state, action):
        super().__init__()

        self.net = nn.Sequential(
            nn.Linear(state, 128),  # Couche d'entrée (dimension de l'état)
            nn.ReLU(),              # Fonction d'activation
            nn.Linear(128, 128),    # Couche cachée
            nn.ReLU(),
            nn.Linear(128, 128),    # Couche cachée
            nn.ReLU(),
            nn.Linear(128, action)  # Couche de sortie (valeur Q pour chaque action)
        )

    def forward(self, X): 
        # Propagation avant : retourne les valeurs Q prédites pour un état d'entrée X donné
        return self.net(X)