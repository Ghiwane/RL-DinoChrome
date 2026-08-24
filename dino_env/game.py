import pygame

def collision(dino, obstacle):
    dino_box = dino.get_hitbox()
    obstacle_box = obstacle.get_hitbox()
    dino_rect = pygame.Rect(dino_box)
    obstacle_rect = pygame.Rect(obstacle_box)

    tolerant_dino_box = dino_rect.inflate(-20, -20)
    tolerant_obstacle_box = obstacle_rect.inflate(-20, -20)

    return tolerant_dino_box.colliderect(tolerant_obstacle_box)