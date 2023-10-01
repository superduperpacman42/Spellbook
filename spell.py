import pygame

from effect import Effect
from util import *


class Spell:
    def __init__(self, name, t=0):
        self.name = name.upper()
        font = pygame.font.Font("fonts/VINERITC.TTF", 28)
        self.letters = [font.render(letter, True, (53, 53, 53)) for letter in self.name]
        self.text = font.render(self.name, True, (53, 53, 53))
        self.t = t
        self.frame = load_image("SpellFrame.png", 1)[0]
        self.active_frame = load_image("SpellFrameSelected.png", 1)[0]
        self.hover_frame = load_image("SpellFrameHover.png", 1)[0]

    def draw(self, surface, x, y, t, dx=0, dy=0, active=False, hover=False):
        if dx or dy:
            w, h = WORD_SCALE * 0.8, WORD_SCALE * 0.8,
            rect = pygame.Rect((0, 0, w, h))
            for letter in self.letters:
                rect.size = (w, h)
                rect.center = x, y
                pygame.draw.rect(surface, (0, 0, 0), rect)
                rect.size = (w-4, h-4)
                rect.center = x, y
                pygame.draw.rect(surface, (255, 255, 246), rect)
                rect.size = (letter.get_width(), letter.get_height())
                rect.center = x, y + 4
                surface.blit(letter, rect)
                x += dx * WORD_SCALE
                y += dy * WORD_SCALE
        else:
            dy = max(0, 1 - (t - self.t)/.25) * 150
            if active:
                surface.blit(self.active_frame, (x - self.frame.get_width()/2, y - self.frame.get_height()/2 + dy))
            elif hover:
                surface.blit(self.hover_frame, (x - self.frame.get_width()/2, y - self.frame.get_height()/2 + dy))
            else:
                surface.blit(self.frame, (x - self.frame.get_width()/2, y - self.frame.get_height()/2 + dy))
            surface.blit(self.text, (x - self.text.get_width()/2, y - self.text.get_height()/2 + dy))

    def activate(self, arena, t):
        squares, effect = self.get_effect()
        if effect == "Heal" or effect == "Vampire":
            play_sound("Heal.wav", 0.05)
        if effect != "Heal":
            play_sound("Spell.wav", 0.05)

        for square in squares:
            target = None
            if square in arena.grid and arena.grid[square]:
                target = arena.grid[square]
            arena.effectGrid[square] = Effect(effect, t, target)
            arena.n_effects += 1

    def get_effect(self):
        squares = None
        effect = "Slash"
        if self.name == "SMITE":
            effect = "Slash"
            squares = ["00000",
                       "00110",
                       "00010",
                       "00110",
                       "00000"]
        elif self.name == "SLASH":
            effect = "Slash"
            squares = ["00000",
                       "01100",
                       "01000",
                       "01100",
                       "00000"]
        elif self.name == "SWING":
            effect = "Slash"
            squares = ["00000",
                       "00000",
                       "01010",
                       "01110",
                       "00000"]
        elif self.name == "SLICE":
            effect = "Slash"
            squares = ["00000",
                       "01110",
                       "01010",
                       "00000",
                       "00000"]
        elif self.name == "JAB":
            effect = "Slash"
            squares = ["00000",
                       "00000",
                       "00000",
                       "01110",
                       "00000"]
        elif self.name == "STAPLE":
            effect = "Slash"
            squares = ["01110",
                       "01010",
                       "00000",
                       "01010",
                       "01110"]
        elif self.name == "CHOMP":
            effect = "Slash"
            squares = ["11111",
                       "01010",
                       "00000",
                       "01010",
                       "11111"]
        elif self.name == "STAB":
            effect = "Slash"
            squares = ["00100",
                       "01110",
                       "00000",
                       "00000",
                       "00000"]
        elif self.name == "SEVER":
            effect = "Slash"
            squares = ["01110",
                       "01110",
                       "00000",
                       "00000",
                       "00000"]
        elif self.name == "BISECT":
            effect = "Slash"
            squares = ["11011",
                       "11011",
                       "11011",
                       "11011",
                       "11011"]
        elif self.name == "EXECUTE":
            effect = "Slash"
            squares = ["01110",
                       "11111",
                       "11011",
                       "11111",
                       "01110"]
        elif self.name == "VORTEX":
            effect = "Shadow"
            squares = ["00000",
                       "01110",
                       "01010",
                       "01110",
                       "00000"]
        elif self.name == "ZAP":
            effect = "Shock"
            squares = ["00100",
                       "01010",
                       "00000",
                       "00000",
                       "00000"]
        elif self.name == "CHARGE":
            effect = "Shock"
            squares = ["10101",
                       "01010",
                       "10001",
                       "01010",
                       "10101"]
        elif self.name == "JOLT":
            effect = "Shock"
            squares = ["10001",
                       "01010",
                       "00000",
                       "01010",
                       "10001"]
        elif self.name == "THUNDER":
            effect = "Shock"
            squares = ["10001",
                       "11011",
                       "11011",
                       "11011",
                       "10001"]
        elif self.name == "SHOCK":
            effect = "Shock"
            squares = ["10101",
                       "01010",
                       "00000",
                       "01010",
                       "10101"]
        elif self.name == "BURN":
            effect = "Burn"
            squares = ["00000",
                       "00000",
                       "11011",
                       "00000",
                       "00000"]
        elif self.name == "RADIATE":
            effect = "Burn"
            squares = ["10101",
                       "01110",
                       "11011",
                       "01110",
                       "10101"]
        elif self.name == "RAY":
            effect = "Burn"
            squares = ["00100",
                       "00100",
                       "00000",
                       "00000",
                       "00000"]
        elif self.name == "TORCH":
            effect = "Burn"
            squares = ["00000",
                       "01110",
                       "01010",
                       "01110",
                       "00000"]
        elif self.name == "BEAM":
            effect = "Burn"
            squares = ["00100",
                       "00100",
                       "00000",
                       "00100",
                       "00100"]
        elif self.name == "TOAST":
            effect = "Burn"
            squares = ["11011",
                       "11011",
                       "00000",
                       "11011",
                       "11011"]
        elif self.name == "FLAME":
            effect = "Burn"
            squares = ["00000",
                       "00000",
                       "00000",
                       "01110",
                       "11111"]
        elif self.name == "SPARK":
            effect = "Burn"
            squares = ["11000",
                       "11000",
                       "11000",
                       "11000",
                       "11000"]
        elif self.name == "FIREBALL":  # all
            effect = "Burn"
            squares = ["11111",
                       "11111",
                       "11011",
                       "11111",
                       "11111"]
        elif self.name == "DOOM":
            effect = "Shadow"
            squares = ["10101",
                       "00000",
                       "10001",
                       "00000",
                       "10101"]
        elif self.name == "HEX":
            effect = "Shadow"
            squares = ["01000",
                       "00010",
                       "10000",
                       "00001",
                       "10100"]
        elif self.name == "HAUNT":
            effect = "Shadow"
            squares = ["01010",
                       "10101",
                       "01010",
                       "10101",
                       "01010"]
        elif self.name == "CURSE":
            effect = "Shadow"
            squares = ["11111",
                       "10001",
                       "10001",
                       "10001",
                       "11111"]
        elif self.name == "SHADOW":
            effect = "Shadow"
            squares = ["10111",
                       "11101",
                       "01011",
                       "11011",
                       "11110"]
        elif self.name == "SORROW":
            effect = "Shadow"
            squares = ["11011",
                       "11011",
                       "00000",
                       "01110",
                       "10001"]
        elif self.name == "DARKNESS":
            effect = "Shadow"
            squares = ["11111",
                       "11111",
                       "11011",
                       "11111",
                       "11111"]
        elif self.name == "LEECH":
            effect = "Vampire"
            squares = ["00100",
                       "00100",
                       "11111",
                       "00100",
                       "00100"]
        elif self.name == "DEVOUR":
            effect = "Vampire"
            squares = ["11111",
                       "10001",
                       "10101",
                       "10001",
                       "11111"]
        elif self.name == "VAMPIRE":
            effect = "Vampire"
            squares = ["10101",
                       "01110",
                       "11111",
                       "01110",
                       "10101"]
        elif self.name == "CONSUME":
            effect = "Vampire"
            squares = ["11111",
                       "11011",
                       "10101",
                       "11011",
                       "11111"]
        elif self.name == "HUNGER":
            effect = "Vampire"
            squares = ["11111",
                       "00000",
                       "11111",
                       "00000",
                       "11111"]
        elif self.name == "HEAL":
            effect = "Heal"
            squares = ["00000",
                       "00000",
                       "00100",
                       "00000",
                       "00000"]
        elif self.name == "LIFE":
            effect = "Heal"
            squares = ["00000",
                       "00000",
                       "00100",
                       "00000",
                       "00000"]
        elif self.name == "SAVE":
            effect = "Heal"
            squares = ["00000",
                       "00000",
                       "00100",
                       "00000",
                       "00000"]
        elif self.name == "RECOVER":
            effect = "Heal2"
            squares = ["00000",
                       "00000",
                       "00100",
                       "00000",
                       "00000"]
        elif self.name == "REGROWTH":
            effect = "Heal3"
            squares = ["00000",
                       "00000",
                       "00100",
                       "00000",
                       "00000"]
        squares_list = []
        if not squares:
            print("ERROR, not found: ", self.name)
            squares_list, effect
        for x in range(5):
            for y in range(5):
                if squares[y][x] == "1":
                    squares_list.append((x-2, y-2))
        return squares_list, effect
