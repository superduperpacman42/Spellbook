import pygame

from util import *

class Arena:
    def __init__(self):
        """ Draws grid centered on w/2, h/2 """
        self.grid = {}
        self.effectGrid = {}
        arena = load_image("Arena.png", number=1)[0]
        self.torch = load_image("Torch.png", 6)
        self.big_torch = [pygame.transform.smoothscale(img, (img.get_width()*1.2, img.get_height()*1.3)) for img in self.torch]

        self.w, self.h = arena.get_width(), arena.get_height()
        self.image = pygame.Surface((self.w, self.h))
        self.image.fill((0, 255, 255))
        self.image.blit(arena, (0, 0))
        self.image.set_colorkey((0, 255, 255))
        self.update_image(None)
        self.n_effects = 0

    def draw(self, surface, x, y, t):
        surface.blit(self.image, (GRID_X - self.w/2, GRID_Y - self.h/2))
        i = int(t * 1000 / FRAME_RATE) % len(self.torch)
        i2 = int(t * 1000 / FRAME_RATE + 2) % len(self.torch)
        i3 = int(t * 1000 / FRAME_RATE + 4) % len(self.torch)
        surface.blit(self.big_torch[i], (8, 80))
        surface.blit(self.torch[i2], (200, 15))
        surface.blit(self.torch[i3], (460, 15))
        keys = list(self.grid.keys()) + list(self.effectGrid.keys())
        keys.sort(key=lambda x: x[1])
        prev = []
        self.n_effects = 0
        for key in keys:
            if key in prev:
                continue
            prev += [key]
            if key in self.grid and self.grid[key]:
                self.grid[key].draw(surface, x, y, t)
            if key in self.effectGrid and self.effectGrid[key]:
                self.n_effects += 1
                self.effectGrid[key].draw(surface, key[0], key[1], t)
                if self.effectGrid[key].done:
                    self.effectGrid[key] = None

    def reset(self):
        self.grid = {}
        n_effects = 0
        self.update_image(None)

    def update_image(self, spell):
        squares, effect = (), None
        if spell and spell != "Pass":
            squares, effect = spell.get_effect()
        s1 = GRID_SCALE * 0.4
        s2 = GRID_SCALE * 0.3
        for x in range(-2, 3):
            for y in range(-2, 3):
                color = (163, 112, 42)
                if (x, y) in squares:
                    if effect == "Heal" or effect == "Heal2" or effect == "Heal3" or \
                            (effect == "Vampire" and x == 0 and y == 0):
                        color = (50, 150, 50)
                    else:   # damage
                        color = (200, 0, 0)
                x0 = GRID_SCALE * x
                y0 = GRID_SCALE * y
                p1 = skew_grid(x0-s1, y0-s1, self.w/2, self.h/2)
                p2 = skew_grid(x0+s1, y0-s1, self.w/2, self.h/2)
                p3 = skew_grid(x0+s1, y0+s1, self.w/2, self.h/2)
                p4 = skew_grid(x0-s1, y0+s1, self.w/2, self.h/2)
                pygame.draw.polygon(self.image, color, (p1, p2, p3, p4))
                p1 = skew_grid(x0-s2, y0-s2, self.w/2, self.h/2)
                p2 = skew_grid(x0+s2, y0-s2, self.w/2, self.h/2)
                p3 = skew_grid(x0+s2, y0+s2, self.w/2, self.h/2)
                p4 = skew_grid(x0-s2, y0+s2, self.w/2, self.h/2)
                pygame.draw.polygon(self.image, (0, 255, 255), (p1, p2, p3, p4))
