import pygame.transform

from util import *
import random


class GridSprite:
    def __init__(self, arena, grid_x, grid_y, image, frames=14):
        self.grid_x, self.grid_y = grid_x, grid_y
        self.x, self.y = grid_x, grid_y
        self.target_x, self.target_y, self.target_sprite = 0, 0, None
        self.image = load_image(image + ".png", number=frames)
        self.name = image
        self.damage = recolor(self.image)
        self.frames = frames
        self.t0 = random.random() * FRAME_RATE * frames
        self.speed = SPEED
        self.delay = 1
        self.turn_count = 0
        self.arena = arena
        self.dead = False
        self.effect = None
        self.effect_end_time = None
        self.effect_t0 = None
        self.hp = 1
        self.score = 1
        arena.grid[self.grid_x, self.grid_y] = self
        if image == "Player":
            self.score = 0
            self.hp = 5
        if image == "Skeleton":
            self.hp = 2
            self.score = 2
        if image == "Bat":
            self.delay = 0
            self.score = 2
        if image == "Troll":
            self.hp = 3
            self.score = 5
            self.delay = 2
        if image == "Spider":
            self.delay = 0
            self.hp = 2
            self.score = 5

    def draw(self, surface, x, y, t):
        if self.name == "Spider" or self.name == "Bat":
            i = int((t - self.t0) * 1000 / FRAME_RATE * 1.5) % len(self.image)
        elif self.name == "Troll":
            i = int((t - self.t0) * 1000 / FRAME_RATE * 0.6) % len(self.image)
        else:
            i = int((t - self.t0) * 1000 / FRAME_RATE) % len(self.image)
        s = skew_grid(GRID_SCALE * self.x, GRID_SCALE * self.y, scale_factor=True)
        xw_, yw = skew_grid(GRID_SCALE * self.x, GRID_SCALE * (self.y + 0.28))
        xw, yw_ = skew_grid(GRID_SCALE * self.x, GRID_SCALE * (self.y + 0.28) - self.image[i].get_height() * .2)
        if self.hp > 0:
            image = pygame.transform.smoothscale(self.image[i], (s*self.image[i].get_width(), s*self.image[i].get_height()))
            surface.blit(image, (xw - x - image.get_width() / 2 + GRID_X, yw - y - image.get_height() + GRID_Y))
        if self.effect:
            if t > self.effect_end_time:
                self.effect = None
                self.effect_end_time = None
                if self.hp <= 0:
                    if not self.dead:
                        self.dead = True
                        self.effect = load_image("Death.png", 16)
                        self.effect_end_time = t + 16 * FRAME_RATE/1000
                        self.effect_t0 = t
                    else:
                        self.destroy()
            else:
                i = int((t - self.effect_t0) * 1000 / FRAME_RATE) % len(self.effect)
                image = pygame.transform.smoothscale(self.effect[i],
                                                     (s * self.effect[i].get_width(), s * self.effect[i].get_height()))
                surface.blit(image, (xw - x - image.get_width() / 2 + GRID_X, yw - y - image.get_height() + GRID_Y))

    def update(self, dt):
        x = self.x % 1
        jump = (x*x - x) * JUMP
        self.x = approach(self.x, self.grid_x + self.target_x, self.speed)
        self.y = approach(self.y, self.grid_y + self.target_y + jump, self.speed)
        if max(abs(self.grid_x + self.target_x - self.x), abs(self.grid_y + self.target_y - self.y)) < 0.5:
            self.target_x = 0
            self.target_y = 0
            if self.target_sprite:
                self.target_sprite.hit()
                self.target_sprite = None

    def attack(self, dx, dy, damage=None):
        self.target_x = dx
        self.target_y = dy
        self.target_sprite = damage

    def hit(self, damage=1):
        self.hp -= damage
        if self.hp > 9:
            self.hp = 9
        self.effect = True
        self.effect_end_time = 0
        if self.name == "Player":
            play_sound("Hurt.wav", 0.05)
            print("OW")

    def move(self, dx, dy):
        self.arena.grid[self.grid_x, self.grid_y] = None
        self.grid_x += dx
        self.grid_y += dy
        self.arena.grid[self.grid_x, self.grid_y] = self

    def destroy(self):
        self.arena.grid[self.grid_x, self.grid_y] = None

    def add_effect(self, name, t):
        frames = 1
        damage = 1
        if name == "Burn":
            duration = 0.5
        self.hit(damage)
        self.effect = load_image(name + ".png", frames)
        self.effect_t0 = t
        self.effect_end_time = t + duration


def approach(x, goal, speed):
    if x > goal + speed:
        return x - speed
    elif x < goal - speed:
        return x + speed
    else:
        return goal


def recolor(animation):
    recolored = []
    for image in animation:
        recolored += [image]
    return recolored
