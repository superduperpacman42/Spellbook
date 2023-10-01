from util import *


class Effect:
    def __init__(self, name, t, target):
        self.name = name
        self.damage = 1
        self.frames = 8
        self.duration = self.frames * FRAME_RATE/1000
        self.done = False
        self.target = target
        if name == "Burn":
            self.frames = 6
            self.duration = 0.25
        if name == "Heal":
            self.damage = -1
        if name == "Heal2":
            self.damage = -2
            name = "Heal"
        if name == "Heal3":
            self.damage = -3
            name = "Heal"
        if name == "Vampire":
            if self.target and self.target.x == 0 and self.target.y == 0:
                self.name = "Heal"
                self.damage = -1
            else:
                self.name = "Shadow"
            name = self.name
        self.animation = load_image(name + ".png", self.frames)
        self.t0 = t

    def start(self, t):
        self.t0 = t

    def draw(self, surface, x, y, t):
        if t > self.t0 + self.duration:
            self.done = True
            if self.target:
                self.target.hit(self.damage)
            return
        i = int((t - self.t0) * 1000 / FRAME_RATE) % len(self.animation)
        s = skew_grid(GRID_SCALE * x, GRID_SCALE * y, scale_factor=True)
        xw_, yw = skew_grid(GRID_SCALE * x, GRID_SCALE * (y + 0.28))
        xw, yw_ = skew_grid(GRID_SCALE * x, GRID_SCALE * (y + 0.28) - self.animation[i].get_height() * .2)
        image = pygame.transform.smoothscale(self.animation[i],
                                             (s * self.animation[i].get_width(), s * self.animation[i].get_height()))
        if self.name == "Heal2":
            surface.blit(image, (xw - x - image.get_width() / 2 + GRID_X - 10, yw - y - image.get_height() + GRID_Y-10))
            surface.blit(image, (xw - x - image.get_width() / 2 + GRID_X + 5, yw - y - image.get_height() + GRID_Y))
        elif self.name == "Heal3":
            surface.blit(image, (xw - x - image.get_width() / 2 + GRID_X - 20, yw - y - image.get_height() + GRID_Y-10))
            surface.blit(image, (xw - x - image.get_width() / 2 + GRID_X + 20, yw - y - image.get_height() + GRID_Y-15))
            surface.blit(image, (xw - x - image.get_width() / 2 + GRID_X, yw - y - image.get_height() + GRID_Y))
        else:
            surface.blit(image, (xw - x - image.get_width() / 2 + GRID_X, yw - y - image.get_height() + GRID_Y))
