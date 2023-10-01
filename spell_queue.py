import random

from spell import Spell
from util import *


class SpellQueue:
    def __init__(self):
        self.spells = []
        self.w = WIDTH
        self.h = 150
        self.nx = 5
        self.ny = 1
        self.n = self.nx * self.ny
        self.selected = None
        self.hover = None
        self.image = load_image("Queue.png", 1)[0]
        self.pass_image = load_image("PassButton.png")[0]
        self.pass_image_hover = load_image("PassButtonSelected.png")[0]

    def draw(self, surface, hover_x, hover_y, t):
        hover = self.click(hover_x, hover_y, select=False)
        if hover == "Pass":
            surface.blit(self.pass_image_hover, (PASS_X - self.pass_image.get_width()/2, PASS_Y - self.pass_image.get_height()/2))
        else:
            surface.blit(self.pass_image, (PASS_X - self.pass_image.get_width()/2, PASS_Y - self.pass_image.get_height()/2))
        surface.blit(self.image, (0, GRID_Y * 2))
        for i, spell in enumerate(self.spells):
            x = QUEUE_X - (i - (self.nx-1)/2) * self.w / (self.nx + 1/4)
            y = QUEUE_Y
            active = self.selected == i
            hovering = self.hover == spell
            spell.draw(surface, x, y, t, active=active, hover=hovering)
        if hover != self.hover:
            self.hover = hover
            return self.hover if self.hover else (self.spells[self.selected] if self.selected is not None else "None")

    def reset(self):
        spells = list(SPELLS)
        random.shuffle(spells)
        self.spells = [Spell(s) for s in spells[:5]]

    def click(self, x, y, select=True):
        if abs(x - PASS_X) < self.pass_image.get_width()/2 and abs(y - PASS_Y) < self.pass_image.get_height()/2:
            if select:
                self.selected = None
            return "Pass"
        for i, spell in enumerate(self.spells):
            xs = QUEUE_X - (i - (self.nx - 1) / 2) * self.w / (self.nx + 1 / 2)
            ys = QUEUE_Y
            if 2*abs(x - xs) < self.w / (self.nx + 1/2) and abs(y - ys) < self.h/2:
                if select:
                    self.selected = i
                    play_sound("Place.wav", 0.01)
                return spell
        if select:
            self.selected = None
        return None

    def refresh(self, t):
        spells = list(SPELLS)
        for spell in self.spells:
            for name in spells:
                if spell.name == name:
                    spells.remove(name)
        spell = random.choice(spells)
        self.spells[self.selected] = Spell(spell, t)
        self.selected = None
