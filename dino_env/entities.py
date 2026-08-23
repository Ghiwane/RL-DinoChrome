import constants as ct
from enum import Enum, auto

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
            return (ct.DINO_X, self.dino_y, ct.DINO_X + 88, self.dino_y + 93)

        elif self.current_state == State.DUCKING:
            standing_height = 90
            duck_height = 60
            y_offset = standing_height - duck_height

            y0 = self.dino_y + y_offset
            return (ct.DINO_X, y0, ct.DINO_X + 118, y0 + duck_height)