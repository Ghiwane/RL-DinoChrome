import numpy as np
import constants as ct
from entities import Dino
from game import ObstacleSpawner, collision

class Action:
    NOTHING = 0
    JUMP = 1
    DUCK = 2

class DinoGame:
    def __init__(self):
        self.reset()

    def reset(self):
        self.dino = Dino()
        self.obstacles = []
        self.spawner = ObstacleSpawner()
        self.score = 0.0
        self.speed = ct.SPEED
        self.done = False

        return self.get_state()

    def get_state(self):
        ahead = [o for o in self.obstacles if o.X + o.width > self.dino.dino_x]
        next_obstacle = min(ahead, key=lambda o: o.X) if ahead else None

        if next_obstacle is not None:
            distance_norm = (next_obstacle.X - self.dino.dino_x) / ct.SCREEN_W
            width_norm = next_obstacle.width / ct.SCREEN_W
            height_norm = next_obstacle.Y / ct.SCREEN_H

        else:
            distance_norm = 1.0
            width_norm = 0.0
            height_norm = 1.0

        speed_norm = self.speed / ct.MAX_SPEED
        velocity_norm = np.clip(self.dino.y_velocity / abs(ct.Y_VELOCITY), -1, 1 ) 

        return np.array([
            distance_norm, 
            width_norm,
            height_norm,
            speed_norm,
            velocity_norm
        ], dtype=np.float32)

    def reward_count(self):
        if self.done:
            return -100
        return 1

    def step(self, action):
        if action == Action.JUMP:
            self.dino.jump()
        elif action == Action.DUCK:
            self.dino.duck(True)
        else:
            self.dino.duck(False)

        self.dino.update()

        new_obs = self.spawner.update(self.speed)
        if new_obs is not None:
            self.obstacles.append(new_obs)

        for obs in self.obstacles:
            obs.update(self.speed)

        self.obstacles = [o for o in self.obstacles if not o.is_off_screen()]

        for obs in self.obstacles:
            if collision(self.dino, obs):
                self.done = True
                break

        if not self.done:
            self.score += self.speed / ct.FPS
            if self.score > 0 and int(self.score) % ct.SCORE_PER_SPEEDUP == 0:
                self.speed = min(ct.MAX_SPEED, self.speed + ct.SPEED_INCREMENT * 0.01)

        if self.score >= 99999:
            self.done = True

        reward = self.reward_count()

        state = self.get_state()

        return state, reward, self.done, {"score" : self.score}