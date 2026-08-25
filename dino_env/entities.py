import constants as ct
from enum import Enum, auto
import random

# États possibles du dinosaure
class State(Enum):
    RUNNING = auto()
    JUMPING = auto()
    DUCKING = auto()
    FAST_FALLING = auto()
    CRASHED = auto()


class Dino:
    def __init__(self, initial_state = State.RUNNING):
        self.dino_y = ct.DINO_Y
        self.dino_x = ct.DINO_X
        self.current_state = initial_state
        self.y_velocity = 0.0

    def jump(self):
        # Le saut n'est déclenché que depuis l'état de course
        if self.current_state == State.RUNNING :
            self.current_state = State.JUMPING
            self.y_velocity = ct.Y_VELOCITY

        # Si le joueur saute pendant qu'il se baisse, il se relève simplement
        elif self.current_state == State.DUCKING:
            self.current_state = State.RUNNING

    def duck(self, is_ducking: bool):
        if is_ducking:
            if self.current_state == State.RUNNING:
                self.current_state = State.DUCKING

            # En l'air, appuyer sur BAS force une chute rapide (FAST_FALLING)
            elif self.current_state == State.JUMPING:
                self.y_velocity = 0.0
                self.current_state = State.FAST_FALLING

        else:
            # Relâcher la touche BAS fait repasser le dino en mode course s'il était accroupi
            if self.current_state == State.DUCKING:
                self.current_state = State.RUNNING

    def update(self):
        # Applique la gravité selon le mode de chute (saut classique ou chute rapide)
        if self.current_state == State.JUMPING:
            self.y_velocity += ct.GRAVITY
            self.dino_y += self.y_velocity

        elif self.current_state == State.FAST_FALLING:
            self.y_velocity += ct.GRAVITY * ct.SPEED_DROP_COEF
            self.dino_y += self.y_velocity
    
        # Détection du réatterrissage sur le sol
        if self.current_state in (State.JUMPING, State.FAST_FALLING):
            if self.dino_y >= ct.DINO_Y:
                self.dino_y = ct.DINO_Y
                self.y_velocity = 0.0
                self.current_state = State.RUNNING

    def get_hitbox(self):
        # Hitbox standard pour les positions debout / en l'air
        if self.current_state in (State.RUNNING, State.JUMPING, State.FAST_FALLING, State.CRASHED):
            return (ct.DINO_X, self.dino_y, ct.DINO_RUNNING_W, ct.DINO_RUNNING_H)

        # Hitbox ajustée quand le dino est accroupi : conserve l'ancrage bas
        elif self.current_state == State.DUCKING:
            y_offset = ct.DINO_RUNNING_H - ct.DINO_DUCKING_H

            y0 = self.dino_y + y_offset
            return (ct.DINO_X, y0, ct.DINO_DUCKING_W, ct.DINO_DUCKING_H)

class Obstacle:
    def __init__(self, x, y, width, height, obstacle_type):
        self.X = x
        self.Y = y
        self.width = width
        self.height = height
        self.type = obstacle_type

    def update(self, speed):
        # Déplacement vers la gauche selon la vitesse du jeu
        self.X -= speed

    def is_off_screen(self):
        # Vérifie si l'obstacle est totalement sorti de l'écran à gauche
        if self.X + self.width < 0:
            return True
        else:
            return False

    def get_hitbox(self):
        return (self.X, self.Y, self.width, self.height)

class Cactus(Obstacle):
    # Liste des dimensions (hauteur, largeur) pour chaque variante de cactus
    VARIANTS = [
        (ct.BIGCACTUS_H, ct.BIGCACTUS1_W),
        (ct.BIGCACTUS_H, ct.BIGCACTUS2_W),
        (ct.BIGCACTUS_H, ct.BIGCACTUS3_W),
        (ct.BIGCACTUS_H, ct.BIGCACTUS4_W),

        (ct.SMALLCACTUS_H, ct.SMALLCACTUS1_W),
        (ct.SMALLCACTUS_H, ct.SMALLCACTUS2_W),
        (ct.SMALLCACTUS_H, ct.SMALLCACTUS3_W),
    ]

    def __init__(self, variant_idx):

        self.variant_index = variant_idx
        height, width = self.VARIANTS[variant_idx]

        # Ancrage Y du cactus aligné sur le sol avec décalage visuel (+10)
        super().__init__(
            x = ct.SCREEN_W,
            y = ct.GROUND_Y - height + 10,
            width = width,
            height = height,
            obstacle_type = "cactus"
        )

    @classmethod
    def create_random(cls):
        # Sélectionne une variante de cactus aléatoire dans la liste VARIANTS
        random_variant = random.randint(0, len(cls.VARIANTS) - 1)
        return cls(variant_idx = random_variant)

class Ptero(Obstacle):
    # Différentes hauteurs de vol pour le ptérodactyle
    HEIGHTS_BY_TYPE = {
        "P_LOW":  ct.PTERO_Y_LOW,
        "P_MID":  ct.PTERO_Y_MID,
        "P_HIGH": ct.PTERO_Y_HIGH
    }

    def __init__(self, obstacle_type, width = ct.PTERO_W, height = ct.PTERO_H):
        y_position = self.HEIGHTS_BY_TYPE.get(obstacle_type, self.HEIGHTS_BY_TYPE["P_MID"])
        super().__init__(
                x = ct.SCREEN_W,
                y = y_position,
                width = width,
                height = height,
                obstacle_type = obstacle_type
            )

    @classmethod
    def create_random(cls):
        # Choisit aléatoirement la hauteur d'apparition du ptérodactyle
        ptero_type = random.choice(["P_LOW", "P_MID", "P_HIGH"])
        return cls(obstacle_type=ptero_type)