import random
import pygame
import constants as ct
from entities import State, Cactus, Ptero
from assets import load_assets


class Renderer:
    def __init__(self, screen):
        self.screen = screen
        self.assets = load_assets()

        # Gestion des frames d'animation (changement de frame toutes les 6 boucles)
        self.anim_timer = 0
        self.anim_frame = 0

        # Position initiale pour le défilement infini du sol (tiling avec 2 images)
        ground_w = self.assets["ground"].get_width()
        self.ground_x1 = 0
        self.ground_x2 = ground_w

        # Liste des nuages et timer d'apparition
        self.clouds = []
        self.cloud_timer = 60

        self.font = pygame.font.SysFont("consolas", 22, bold=True)

    def _update_animation(self):
        """
        Alterne l'indice de frame (0 ou 1) pour animer la course du dino
        et le battement d'ailes des ptérodactyles.
        """
        self.anim_timer += 1
        if self.anim_timer >= 6:
            self.anim_timer = 0
            self.anim_frame = 1 - self.anim_frame

    def _draw_dino(self, dino):
        """
        Sélectionne le bon sprite selon l'état du dino et l'affiche à l'écran.
        Ancrage bas : aligne le bas du sprite sur le bas de la hitbox.
        """
        if dino.current_state == State.CRASHED:
            sprite = self.assets["dino_dead"]
        elif dino.current_state == State.DUCKING:
            sprite = self.assets["dino_ducking"][self.anim_frame]
        elif dino.current_state in (State.JUMPING, State.FAST_FALLING):
            sprite = self.assets["dino_jumping"]
        else:
            sprite = self.assets["dino_running"][self.anim_frame]

        x, y, w, h = dino.get_hitbox()
        sprite_h = sprite.get_height()
        draw_y = y + h - sprite_h   # Ancrage bas : le bas du sprite colle au bas de la hitbox
        self.screen.blit(sprite, (x, draw_y))

    def _draw_obstacles(self, obstacles):
        """
        Affiche la liste des obstacles (cactus ou ptérodactyles) selon leur position.
        """
        for obs in obstacles:
            if isinstance(obs, Cactus):
                sprite = self.assets["cactus"][obs.variant_index]
            elif isinstance(obs, Ptero):
                sprite = self.assets["ptero"][self.anim_frame]
            else:
                continue
            self.screen.blit(sprite, (obs.X, obs.Y))

    def _draw_ground_scrolling(self, speed):
        """
        Fait défiler horizontalement deux images de sol côte à côte
        et les réinitialise pour créer une illusion de défilement infini.
        """
        ground_img = self.assets["ground"]
        gw = ground_img.get_width()

        self.ground_x1 -= speed
        self.ground_x2 -= speed

        # Réinitialisation de la position dès qu'une image sort de l'écran
        if self.ground_x1 <= -gw:
            self.ground_x1 = self.ground_x2 + gw
        if self.ground_x2 <= -gw:
            self.ground_x2 = self.ground_x1 + gw

        self._draw_ground_frozen()

    def _draw_ground_frozen(self):
        """
        Affiche le sol à ses positions X actuelles (utilisé aussi en Game Over).
        """
        y = int(ct.GROUND_Y) + ct.GROUND_VISUAL_OFFSET
        self.screen.blit(self.assets["ground"], (self.ground_x1, y))
        self.screen.blit(self.assets["ground"], (self.ground_x2, y))

    def _update_clouds(self, speed):
        """
        Gère l'apparition et le déplacement des nuages avec un effet de parallaxe
        (déplacement plus lent que le sol).
        """
        self.cloud_timer -= 1
        if self.cloud_timer <= 0:
            y = random.randint(20, 90)
            self.clouds.append([float(ct.SCREEN_W), y])
            self.cloud_timer = random.randint(90, 200)

        cloud_w = self.assets["cloud"].get_width()
        for cloud in self.clouds:
            cloud[0] -= speed * 0.4   # Parallaxe : 40% de la vitesse du sol
        self.clouds = [c for c in self.clouds if c[0] > -cloud_w]

    def _draw_clouds(self):
        """
        Rendu graphique de tous les nuages actifs.
        """
        for x, y in self.clouds:
            self.screen.blit(self.assets["cloud"], (x, y))

    def _draw_score(self, score):
        """
        Affiche le score formaté sur 5 chiffres (ex: 00125) en haut à droite.
        """
        surf = self.font.render(f"{int(score):05d}", True, (83, 83, 83))
        rect = surf.get_rect(topright=(ct.SCREEN_W - 20, 20))
        self.screen.blit(surf, rect)

    def _draw_game_over(self):
        """
        Affiche l'image Game Over et le message d'invite au centre de l'écran.
        """
        go_img = self.assets["game_over"]
        rect = go_img.get_rect(center=(ct.SCREEN_W // 2, ct.SCREEN_H // 2 - 20))
        self.screen.blit(go_img, rect)

        restart = self.font.render("ESPACE pour rejouer", True, (83, 83, 83))
        restart_rect = restart.get_rect(center=(ct.SCREEN_W // 2, ct.SCREEN_H // 2 + 30))
        self.screen.blit(restart, restart_rect)

    def _draw_hitboxes(self, dino, obstacles):
        """
        Mode Debug (F1) : Dessine les rectangles de collision (hitboxes) du dino (rouge) 
        et des obstacles (bleu).
        """
        dino_box = pygame.Rect(dino.get_hitbox())
        pygame.draw.rect(self.screen, (255, 0, 0), dino_box, 2)

        for obs in obstacles:
            obs_box = pygame.Rect(obs.get_hitbox())
            pygame.draw.rect(self.screen, (0, 120, 255), obs_box, 2)

    def render(self, dino, obstacles, score, speed, game_over, debug=False):
        """
        Boucle principale de rendu : efface l'écran, met à jour le décor et dessine 
        tous les éléments dans l'ordre de profondeur.
        """
        self.screen.fill((247, 247, 247))

        if not game_over:
            self._update_animation()
            self._update_clouds(speed)
            self._draw_ground_scrolling(speed)
        else:
            self._draw_ground_frozen()

        self._draw_clouds()
        self._draw_obstacles(obstacles)
        self._draw_dino(dino)
        self._draw_score(score)
        if game_over:
            self._draw_game_over()
        if debug:
            self._draw_hitboxes(dino, obstacles)
            
        pygame.display.flip()