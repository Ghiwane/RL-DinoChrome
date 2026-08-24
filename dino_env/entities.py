import constants as ct
from enum import Enum, auto
import random

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
        if self.current_state == State.RUNNING :
            self.current_state = State.JUMPING
            self.y_velocity = ct.Y_VELOCITY

        elif self.current_state == State.DUCKING:
            self.current_state = State.RUNNING

    def duck(self, is_ducking: bool):
        if is_ducking:
            if self.current_state == State.RUNNING:
                self.current_state = State.DUCKING

            elif self.current_state == State.JUMPING:
                self.y_velocity=0.0
                self.current_state = State.FAST_FALLING

        else:
            if self.current_state == State.DUCKING:
                self.current_state = State.RUNNING

    def update(self):
        if self.current_state == State.JUMPING:
            self.y_velocity += ct.GRAVITY
            self.dino_y += self.y_velocity

        elif self.current_state == State.FAST_FALLING:
            self.y_velocity += ct.GRAVITY * ct.SPEED_DROP_COEF
            self.dino_y += self.y_velocity
    
        if self.current_state in (State.JUMPING, State.FAST_FALLING):
            if self.dino_y >= ct.DINO_Y:
                self.dino_y = ct.DINO_Y
                self.y_velocity = 0.0
                self.current_state = State.RUNNING

    def get_hitbox(self):
        if self.current_state in (State.RUNNING, State.JUMPING, State.FAST_FALLING):
            return (ct.DINO_X, self.dino_y, 88, 93)

        elif self.current_state == State.DUCKING:
            standing_height = 90
            duck_height = 60
            y_offset = standing_height - duck_height

            y0 = self.dino_y + y_offset
            return (ct.DINO_X, y0, 118, duck_height)

class Obstacle:
    def __init__(self, x, y, width, height, obstacle_type):
        self.X = x
        self.Y = y
        self.width = width
        self.height = height
        self.type = obstacle_type

    def update(self,speed):
        self.X -= speed

    def is_off_screen(self):
        if self.X + self.width < 0:
            return True
        else:
            return False

    def get_hitbox(self):
        return (self.X, self.Y, self.width, self.height)

class Cactus(Obstacle):
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

        super().__init__(
        x = ct.SCREEN_W,
        y = ct.CACTUS_Y,
        width = width,
        height = height,
        obstacle_type = "cactus"
    )

    @classmethod
    def create_random(cls):
        random_variant = random.randint(0, len(cls.VARIANTS) - 1)
        return cls(variant_idx = random_variant)

class Ptero(Obstacle):
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
        ptero_type = random.choice(["P_LOW", "P_MID", "P_HIGH"])
        return cls(obstacle_type=ptero_type)
