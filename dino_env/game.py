import pygame
import random
import constants as ct
from entities import Cactus, Ptero

def collision(dino, obstacle):
    """
    Détecte l'intersection entre le dino et un obstacle.
    Utilise une tolérance (.inflate(-10, -10)) pour réduire les hitboxes de 10px 
    afin de pardonner les frôlements légers et rendre la jouabilité plus fluide.
    """
    dino_box = dino.get_hitbox()
    obstacle_box = obstacle.get_hitbox()
    dino_rect = pygame.Rect(dino_box)
    obstacle_rect = pygame.Rect(obstacle_box)

    # Réduction de 5 pixels sur chaque bord (total -10px en largeur et hauteur)
    tolerant_dino_box = dino_rect.inflate(-10, -10)
    tolerant_obstacle_box = obstacle_rect.inflate(-10, -10)

    return tolerant_dino_box.colliderect(tolerant_obstacle_box)


class ObstacleSpawner:
    """
    Gère le timing et le choix des obstacles.
    Raisonne en FRAMES (temps), pas en pixels : le temps de réaction
    du joueur pour esquiver ne dépend pas de la vitesse au sol.
    C'est cette logique qui deviendra la dynamique de l'env RL en J3.
    """

    def __init__(self):
        self.last_type = None
        self.frames_until_spawn = self._new_interval(ct.SPEED)

    def _new_interval(self, speed):
        """
        Calcule un intervalle d'apparition aléatoire (en nombre de frames) 
        qui se rétrécit progressivement à mesure que la vitesse du jeu augmente.
        """
        # Calcul de la progression de vitesse entre 0.0 et 1.0
        progress = (speed - ct.SPEED) / (ct.MAX_SPEED - ct.SPEED)
        progress = max(0.0, min(1.0, progress))
        tightening = 1.0 - 0.3 * progress  # Réduction progressive jusqu'à -30% d'intervalle à vitesse max

        min_f = int(ct.SPAWN_MIN_FRAMES * tightening)
        max_f = int(ct.SPAWN_MAX_FRAMES * tightening)
        return random.randint(min_f, max_f)

    def _pick_obstacle(self):
        """
        Sélectionne le type d'obstacle (Cactus ou Ptérodactyle).
        """
        if random.random() < 0.65:
            obstacle = Cactus.create_random()
            self.last_type = "cactus"
        else:
            obstacle = Ptero.create_random()
            self.last_type = "ptero"
        return obstacle

    def update(self, speed):
        """
        Décrémente le compteur de frames à chaque mise à jour.
        Renvoie une nouvelle instance d'obstacle lorsque le décompte atteint zéro.
        """
        self.frames_until_spawn -= 1
        if self.frames_until_spawn <= 0:
            self.frames_until_spawn = self._new_interval(speed)
            return self._pick_obstacle()
        return None