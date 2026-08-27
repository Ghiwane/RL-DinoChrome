import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), "..", "dino_env"))
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "agent"))

import pygame
import torch
import constants as ct
from env import DinoGame
from renderer import Renderer
from dqn_agent import DinoAgent

MAX_STEPS = 300000  

def main():
    pygame.init()
    screen = pygame.display.set_mode((ct.SCREEN_W, ct.SCREEN_H))
    pygame.display.set_caption("RL-DinoChrome - Demo")
    clock = pygame.time.Clock()
    renderer = Renderer(screen)

    agent = DinoAgent(5, 3)
    agent.q_network.load_state_dict(torch.load("trained_model.pth"))
    agent.q_network.eval()

    env = DinoGame()
    state = env.reset()
    done = False
    steps = 0
    
    running = True
    while running:
        clock.tick(ct.FPS)  # vitesse réelle de jeu, pour bien voir ce qui se passe

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        if not done and steps < MAX_STEPS:
            with torch.no_grad():
                state_tensor = torch.FloatTensor(state)
                action = agent.q_network(state_tensor).argmax().item()

            state, reward, done, info = env.step(action)
            steps += 1

            if steps % 1000 == 0:
                print(f"step {steps} | score {info['score']:.1f} | action {action}")

        renderer.render(env.dino, env.obstacles, env.score, env.speed, done, debug=True)

        if done or steps >= MAX_STEPS:
            print(f"Fin : {steps} steps, score {env.score:.1f}, done={done}")
            running =  False

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()