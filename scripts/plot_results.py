import numpy as np
import matplotlib.pyplot as plt
import os

LOG_DIR = "logs"
OUT_DIR = "plots"
os.makedirs(OUT_DIR, exist_ok=True)

episode_rewards = np.load(f"{LOG_DIR}/episode_rewards.npy")
eval_episodes = np.load(f"{LOG_DIR}/eval_episodes.npy")
eval_rewards = np.load(f"{LOG_DIR}/eval_rewards.npy")
losses = np.load(f"{LOG_DIR}/losses.npy")

plt.style.use("seaborn-v0_8-darkgrid")


def rolling_avg(data, window):
    if len(data) < window:
        return data
    return np.convolve(data, np.ones(window) / window, mode="valid")


# --- 1. Courbe d'apprentissage (reward brut + moyenne glissante) ---
window = min(200, max(10, len(episode_rewards) // 10))
avg = rolling_avg(episode_rewards, window)

plt.figure(figsize=(10, 5))
plt.plot(episode_rewards, alpha=0.25, color="steelblue", label="Reward par épisode")
plt.plot(range(window - 1, len(episode_rewards)), avg, color="navy", linewidth=2,
         label=f"Moyenne glissante ({window} ép.)")
plt.title("Courbe d'apprentissage - RL-DinoChrome")
plt.xlabel("Épisode")
plt.ylabel("Reward total")
plt.legend()
plt.tight_layout()
plt.savefig(f"{OUT_DIR}/learning_curve.png", dpi=150)
plt.close()

# --- 2. Progression du score d'évaluation (agent sans exploration) ---
plt.figure(figsize=(10, 5))
plt.plot(eval_episodes, eval_rewards, marker="o", color="darkorange", linewidth=2)
plt.title("Score d'évaluation au fil de l'entraînement")
plt.xlabel("Épisode")
plt.ylabel("Score moyen (10 épisodes, greedy)")
plt.tight_layout()
plt.savefig(f"{OUT_DIR}/eval_progress.png", dpi=150)
plt.close()

# --- 3. Courbe de loss ---
loss_window = min(200, max(10, len(losses) // 10))
loss_avg = rolling_avg(losses, loss_window)

plt.figure(figsize=(10, 5))
plt.plot(losses, alpha=0.2, color="firebrick", label="Loss brute")
plt.plot(range(loss_window - 1, len(losses)), loss_avg, color="darkred", linewidth=2,
         label=f"Moyenne glissante ({loss_window})")
plt.title("Évolution de la loss (Double DQN)")
plt.xlabel("Step d'entraînement")
plt.ylabel("MSE Loss")
plt.yscale("log")
plt.legend()
plt.tight_layout()
plt.savefig(f"{OUT_DIR}/loss_curve.png", dpi=150)
plt.close()

# --- 4. Distribution des rewards (avant vs après un seuil, ex: début/fin) ---
half = len(episode_rewards) // 2
plt.figure(figsize=(10, 5))
plt.hist(episode_rewards[:half], bins=30, alpha=0.6, label="Première moitié", color="lightcoral")
plt.hist(episode_rewards[half:], bins=30, alpha=0.6, label="Seconde moitié", color="mediumseagreen")
plt.title("Distribution des rewards : début vs fin d'entraînement")
plt.xlabel("Reward total de l'épisode")
plt.ylabel("Nombre d'épisodes")
plt.legend()
plt.tight_layout()
plt.savefig(f"{OUT_DIR}/reward_distribution.png", dpi=150)
plt.close()

print(f"Graphiques sauvegardés dans {OUT_DIR}/")