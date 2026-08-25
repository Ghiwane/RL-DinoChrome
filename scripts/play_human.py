import os
import sys

# Ajout du dossier dino_env au chemin de recherche Python
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "dino_env"))

import pygame
import constants as ct
from entities import Dino, State
from game import collision, ObstacleSpawner
from renderer import Renderer


def reset_game():
    """
    Réinitialise toutes les variables d'état du jeu pour démarrer une nouvelle partie.
    """
    dino = Dino()
    obstacles = []
    spawner = ObstacleSpawner()
    score = 0.0
    speed = ct.SPEED
    game_over = False
    return dino, obstacles, spawner, score, speed, game_over


def main():
    # Initialisation de Pygame et création de la fenêtre principale
    pygame.init()
    screen = pygame.display.set_mode((ct.SCREEN_W, ct.SCREEN_H))
    pygame.display.set_caption("RL-DinoChrome")
    clock = pygame.time.Clock()
    renderer = Renderer(screen)

    # Lancement d'une première partie
    dino, obstacles, spawner, score, speed, game_over = reset_game()

    running = True
    debug_mode = False

    # --- BOUCLE PRINCIPALE DE JEU ---
    while running:
        clock.tick(ct.FPS)  # Maintient la fréquence d'affichage à 60 FPS

        # --- GESTION DES EVENEMENTS CLAVIER / QUITTER ---
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.KEYDOWN:
                # Espace ou Flèche Haut : Sauter (ou Rejouer si Game Over)
                if event.key in (pygame.K_SPACE, pygame.K_UP):
                    if game_over:
                        dino, obstacles, spawner, score, speed, game_over = reset_game()
                    else:
                        dino.jump()

                # Flèche Bas enfoncée : S'accroupir ou chute rapide
                elif event.key == pygame.K_DOWN and not game_over:
                    dino.duck(True)

                # Touche F1 : Basculer le mode Debug (affichage des hitboxes)
                elif event.key == pygame.K_F1:
                    debug_mode = not debug_mode

            elif event.type == pygame.KEYUP:
                # Flèche Bas relâchée : Se relever
                if event.key == pygame.K_DOWN and not game_over:
                    dino.duck(False)

        # --- MISE A JOUR DE LA LOGIQUE DU JEU ---
        if not game_over:
            # 1. Mise à jour de la physique et de l'état du Dino
            dino.update()

            # 2. Génération automatique de nouveaux obstacles
            new_obstacle = spawner.update(speed)
            if new_obstacle is not None:
                obstacles.append(new_obstacle)

            # 3. Déplacement des obstacles et suppression de ceux hors écran
            for obs in obstacles:
                obs.update(speed)
            obstacles = [o for o in obstacles if not o.is_off_screen()]

            # 4. Vérification des collisions
            for obs in obstacles:
                if collision(dino, obs):
                    dino.current_state = State.CRASHED
                    game_over = True
                    break

            # 5. Calcul du score et augmentation progressive de la vitesse
            if not game_over:
                score += speed / ct.FPS
                if score > 0 and int(score) % ct.SCORE_PER_SPEEDUP == 0:
                    speed = min(ct.MAX_SPEED, speed + ct.SPEED_INCREMENT * 0.01)

        # --- RENDU GRAPHIQUE ---
        renderer.render(dino, obstacles, score, speed, game_over, debug=debug_mode)

    # Fermeture propre de Pygame à la sortie de la boucle
    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()