import pygame.draw

from util import *


class Spellbook:
    def __init__(self, w=8, h=8):
        self.w = 8
        self.h = 8
        self.grid = {}
        self.image = load_image("Spellbook.png")[0]
        self.grid_time = {}
        font = pygame.font.Font("fonts/VINERITC.TTF", 28)
        self.letters = {}
        self.letters_red = {}
        self.letters_green = {}
        for letter in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
            self.letters[letter] = font.render(letter, True, (53, 53, 53))
            self.letters_red[letter] = font.render(letter, True, (200, 0, 0))
            self.letters_green[letter] = font.render(letter, True, (0, 0, 150))
        self.reset()

    def draw(self, surface, t, hoverx, hovery, dx, dy, hoverspell):
        xgrid = round((hoverx - WORD_X) / WORD_SCALE + self.w/2 + .5) - 1
        ygrid = round((hovery - WORD_Y) / WORD_SCALE + self.h / 2 + .5) - 1
        spell_blocks = {}
        valid = False    # Word can be played
        capture = False  # Hide spell on mouse
        if hoverspell and 0 <= xgrid < self.w and 0 <= ygrid < self.h:
            for i, letter in enumerate(hoverspell.name):
                spell_blocks[xgrid + dx * i, ygrid + dy * i] = letter
            valid = self.write(hoverspell.name, xgrid, ygrid, dx, dy, check=True)
            capture = True
        surface.blit(self.image, (GRID_X * 2, 0))
        w, h = WORD_SCALE * 0.8, WORD_SCALE * 0.8,
        rect = pygame.Rect((0, 0, w, h))
        for x in range(self.w):
            for y in range(self.h):
                rect.size = (w, h)
                center = WORD_SCALE * (x - self.w/2 + .5) + WORD_X, WORD_SCALE * (y - self.h/2 + .5) + WORD_Y
                rect.center = center
                if (x, y) in spell_blocks:
                    pygame.draw.rect(surface, (0, 0, 0), rect)
                    rect.size = (w-4, h-4)
                    rect.center = center
                    pygame.draw.rect(surface, (255, 255, 246), rect)
                else:
                    pygame.draw.rect(surface, (255, 255, 246), rect)
                if (x, y) in spell_blocks or self.grid[x, y]:
                    if valid and (x, y) in spell_blocks:  # green
                        letter = self.letters_green[spell_blocks[x, y]]
                    elif (x, y) in spell_blocks:  # red
                        if self.grid[x, y]:
                            letter = self.letters_red[self.grid[x, y]]
                        else:
                            letter = self.letters_red[spell_blocks[x, y]]
                    else:
                        letter = self.letters[self.grid[x, y]]
                        letter.set_alpha(self.grid_time[x, y] / MAX_WORDS * 255)
                    rect.size = (letter.get_width(), letter.get_height())
                    rect.center = center
                    rect.y += 4
                    surface.blit(letter, rect)
        return capture

    def write(self, word, x, y, dx=0, dy=0, check=False):
        n = 0
        for i, letter in enumerate(word.upper()):
            xi, yi = x + dx * i, y + dy * i
            if (xi, yi) not in self.grid:
                return False
            if check:
                if self.grid[xi, yi]:
                    if self.grid[xi, yi] != letter:
                        return False
                else:
                    n += 1
            else:
                self.grid[xi, yi] = letter
                self.grid_time[xi, yi] = MAX_WORDS + 1
        if not check:
            self.tick()
        return n != 0

    def reset(self):
        for x in range(self.w):
            for y in range(self.h):
                self.grid[x, y] = None

    def click(self, x, y, dx, dy, spell):
        xgrid = round((x - WORD_X) / WORD_SCALE + self.w / 2 + .5) - 1
        ygrid = round((y - WORD_Y) / WORD_SCALE + self.h / 2 + .5) - 1
        if self.write(spell.name, xgrid, ygrid, dx, dy, check=True):
            self.write(spell.name, xgrid, ygrid, dx, dy)
            return True
        elif 0 <= xgrid <= self.h and 0 <= ygrid < self.h:
            play_sound("Invalid.wav", 0.05)
        return False

    def tick(self):
        for k, v in self.grid_time.items():
            self.grid_time[k] = max(0, v - 1)
            if v - 1 == 0:
                self.grid[k] = None
