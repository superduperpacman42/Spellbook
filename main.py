import random

from spell_queue import SpellQueue
from util import *
import pygame

from arena import Arena
from grid_sprite import GridSprite, approach
from spellbook import Spellbook
import asyncio


class Game:

    def reset(self, respawn=False):
        """ Resets the game state """
        self.t = 0
        self.sprites = []
        self.arena.reset()
        self.spellbook.reset()
        self.queue.reset()
        self.player = GridSprite(self.arena, 0, 0, "Player")
        self.sprites.append(self.player)
        self.next_wave_time = None
        self.wave = 1
        pygame.mixer.music.set_volume(0.4)

        self.score = 0
        self.dx, self.dy = 1, 0
        self.spell = None
        self.your_turn = True
        self.spawn()
        self.rotated = 0
        for i in range(2):
            self.wave = 3
            self.advance_enemies()

    def ui(self, surface):
        """ Draws the user interface overlay """
        for i in range(self.player.hp):
            surface.blit(self.health_img, (i * self.health_img.get_width() + 10, 10))
        surface.blit(self.score_box, (0, GRID_Y*2 - self.score_box.get_height()))
        score = self.score_font.render(str(self.score * 100), True, (53, 53, 53))
        surface.blit(score, (self.score_box.get_width() - score.get_width() - 30,
                             GRID_Y*2 - score.get_height() + 10))
        i = 1 if self.t % 1 > 0.5 else 0
        if i == 1:
            if self.rotated == 0:
                help = self.help_font.render("Select a spell to cast", True, (53, 53, 53))
                surface.blit(help, (GRID_X * 2 - help.get_width() - 80, GRID_Y * 2 - help.get_height() - 5))
            elif self.rotated == 1:
                help = self.help_font.render("Right click to rotate!", True, (53, 53, 53))
                surface.blit(help, (GRID_X * 2 - help.get_width() - 80, GRID_Y * 2 - help.get_height() - 5))
            elif self.rotated == 2:
                help = self.help_font.render("Write it in your spellbook!", True, (53, 53, 53))
                surface.blit(help, (GRID_X * 2 - help.get_width() - 30, GRID_Y * 2 - help.get_height() - 5))

        if self.player.dead and not self.player.effect:
            pygame.mixer.music.set_volume(0.2)
            x, y = pygame.mouse.get_pos()
            i = 1 if self.t % 1 > 0.5 else 0
            score = self.end_font.render(str(self.score * 100), True, (53, 53, 53))
            if abs(x - GRID_X) < self.game_over[i].get_width() / 2 and abs(y - GRID_Y) < self.game_over[
                i].get_height() / 2:
                surface.blit(self.game_over_hover[i], (GRID_X - self.game_over[i].get_width() / 2,
                                                       GRID_Y - self.game_over[i].get_height() / 2))
            else:
                surface.blit(self.game_over[i], (GRID_X - self.game_over[i].get_width() / 2,
                                                 GRID_Y - self.game_over[i].get_height() / 2))
            surface.blit(score, (GRID_X - score.get_width() / 2,
                                 GRID_Y - score.get_height() / 2 + 75))

    def update(self, dt, keys):
        """ Updates the game by a timestep and redraws graphics """
        self.t += dt / 1000
        if not self.your_turn and self.arena.n_effects == 0:
            self.advance_enemies()
            self.your_turn = True
        x, y = pygame.mouse.get_pos()
        if self.next_wave_time and self.t > self.next_wave_time:
            self.next_wave_time = None
            self.advance_enemies()
        surface = pygame.Surface((WIDTH, HEIGHT))
        surface.fill((255, 229, 178))
        self.arena.draw(surface, 0, 0, self.t)
        capture = self.spellbook.draw(surface, self.t, x, y, self.dx, self.dy, self.spell)
        for sprite in self.sprites:
            sprite.update(dt)
            if sprite.hp <= 0 and not sprite.effect:
                self.sprites.remove(sprite)
                self.score += sprite.score
        hover = self.queue.draw(surface, x, y, self.t)
        if hover:
            self.arena.update_image(None if hover == "None" else hover)
        if self.spell and not capture:
            self.spell.draw(surface, x, y, self.t, self.dx, self.dy)
        self.ui(surface)
        self.screen.blit(surface, (0, 0))

    def advance_enemies(self):
        self.sprites.sort(key=lambda e: max(abs(e.x), abs(e.y)))
        moved = False
        for sprite in self.sprites:
            if sprite is not self.player and not sprite.dead:
                d = max(abs(sprite.grid_x), abs(sprite.grid_y))
                if d > self.wave:  # wait your turn
                    self.wave += 1
                    self.next_wave_time = self.t + .3 if moved else self.t
                    return
                if d < self.wave:  # already moved
                    continue
                if sprite.turn_count < sprite.delay:
                    sprite.turn_count += 1
                    continue
                moved = True
                sprite.turn_count = 0
                x_goal, y_goal = sprite.grid_x, sprite.grid_y
                x_goal = approach(sprite.grid_x, 0, 1)
                y_goal = approach(sprite.grid_y, 0, 1)
                if (x_goal, y_goal) in self.arena.grid and self.arena.grid[x_goal, y_goal] and (x_goal or y_goal):
                    if abs(sprite.grid_x) > abs(sprite.grid_y):
                        y_goal = sprite.grid_y
                    if abs(sprite.grid_x) < abs(sprite.grid_y):
                        x_goal = sprite.grid_x
                if x_goal == 0 and y_goal == 0:
                    sprite.attack(x_goal - sprite.grid_x, y_goal - sprite.grid_y, damage=self.player)
                elif (x_goal, y_goal) not in self.arena.grid or not self.arena.grid[x_goal, y_goal] or \
                        self.arena.grid[x_goal, y_goal].dead:
                    sprite.move(x_goal - sprite.grid_x, y_goal - sprite.grid_y)
                else:
                    sprite.attack(x_goal - sprite.grid_x, y_goal - sprite.grid_y)
        self.wave = 1
        self.spawn()
        self.next_wave_time = None

    def spawn(self):
        x = [-3, -2, -1, 0, 1, 2, 3, 3, 3, 3, 3, 3, 2, 1, 0, -1, -2, -3, -3, -3, -3, -3, -3]
        y = [3, 3, 3, 3, 3, 3, 2, 1, 0, -1, -2, -3, -3, -3, -3, -3, -3, -3, -2, -1, 0, 1, 2]
        pos = list(zip(x, y))
        random.shuffle(pos)
        rates = [1, 0, 0, 0, 0]  # average spawns per round

        if self.score > 5:
            rates = [2, 0, 0, 0, 0]
        if self.score > 10:
            rates = [1.5, 0.5, 0, 0, 0]
        if self.score > 20:
            rates = [2, 0.5, 0, 0, 0]
        if self.score > 30:
            rates = [1.5, 0.25, 0.25, 0, 0]
        if self.score > 40:
            rates = [3, 0, 0, 0, 0]
        if self.score > 50:
            rates = [2, 0.25, 0.25, 0, 0]
        if self.score > 60:
            rates = [1, 0.5, 0, 0.25, 0]
        if self.score > 80:
            rates = [4, 0, 0, 0, 0]
        if self.score > 100:
            rates = [0, 1.5, 1.5, 0, 0]
        if self.score > 120:
            rates = [0.5, 0.5, 0.5, 0.25, 0.25]
        if self.score > 150:
            rates = [1, 0.5, 0.5, 0.25, 0.25]
        total = sum(rates) / len(x)
        if self.score > 150:
            total *= (1 + (self.score - 150) / 100)
        count = 0
        for x, y in pos:
            if not ((x, y) in self.arena.grid and self.arena.grid[x, y]):
                if random.random() < total or count < 1:  # min spawns per round
                    enemy = random.choices(["Blob", "Bat", "Skeleton", "Spider", "Troll"], k=1, weights=rates)[0]
                    self.sprites.append(GridSprite(self.arena, x, y, enemy))
                    count += 1
                    if count >= sum(rates):  # max spawns per round
                        break

    def key_pressed(self, key):
        """ Respond to a key press event """
        if key == pygame.K_RETURN:
            if self.player.dead:
                self.reset()

    def mouse_pressed(self, pos, button):
        if self.player.dead:
            x, y = pos
            if abs(x - GRID_X) < self.game_over[0].get_width() / 2 and \
                    abs(y - GRID_Y) < self.game_over[0].get_height() / 2:
                self.reset()
                play_sound("Place.wav", 0.01)
            return
        if button == 1:
            if self.your_turn and not self.next_wave_time and self.spell and \
                    self.spellbook.click(pos[0], pos[1], self.dx, self.dy, self.spell):
                self.spell.activate(self.arena, self.t)
                if self.rotated == 2:
                    self.rotated = 3
                self.spell = None
                self.your_turn = False
                self.queue.refresh(self.t)
            else:
                self.spell = self.queue.click(pos[0], pos[1])
                if self.spell and self.spell != "Pass" and self.rotated == 0:
                    self.rotated = 1
                if self.spell == "Pass":
                    self.spell = None
                    self.your_turn = False
                    self.spellbook.tick()
                    play_sound("Place.wav", 0.01)
            self.arena.update_image(self.spell)
        elif button == 3:
            d = ((1, 0), (1, 1), (0, 1), (-1, 1), (-1, 0), (-1, -1), (0, -1), (1, -1))
            if self.rotated == 1 and self.spell:
                self.rotated = 2
            self.dx, self.dy = d[(d.index((self.dx, self.dy)) + 1) % len(d)]

    ################################################################################

    def __init__(self, name):
        """ Initialize the game """
        self.pause = False
        pygame.init()
        os.environ['SDL_VIDEO_WINDOW_POS'] = '0, 30'
        pygame.display.set_caption(name)
        self.full_screen = False
        if not self.full_screen:
            self.screen = pygame.display.set_mode([WIDTH, HEIGHT])
        else:
            self.screen = pygame.display.set_mode([WIDTH, HEIGHT], pygame.FULLSCREEN)
        pygame.mixer.init(frequency=22050, size=-16, channels=2, buffer=512)
        pygame.mixer.music.set_volume(0.4)
        play_music("Spellbook.wav")
        self.health_img = load_image("Health.png", 1)[0]
        self.game_over = load_image("GameOver.png", 2)
        self.score_box = load_image("Scorebox.png", 1)[0]
        self.game_over_hover = load_image("GameOverSelected.png", 2)
        self.end_font = pygame.font.Font("fonts/VINERITC.TTF", 84)
        self.score_font = pygame.font.Font("fonts/VINERITC.TTF", 40)
        self.help_font = pygame.font.Font("fonts/VINERITC.TTF", 32)

        self.arena = Arena()
        self.spellbook = Spellbook()
        self.queue = SpellQueue()
        self.t = 0
        self.sprites = []
        self.player = None
        self.score = 0
        self.next_wave_time = None
        self.wave = 1
        self.rotated = False
        self.spell = None
        self.dx, self.dy = 0, 0
        self.your_turn = False

        self.reset()
        asyncio.run(self.run())

    async def run(self):
        """ Iteratively call update """
        clock = pygame.time.Clock()
        self.pause = False
        while not self.pause:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    self.key_pressed(event.key)
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.mouse_pressed(event.pos, event.button)
                if event.type == pygame.QUIT:
                    pygame.display.quit()
                    sys.exit()
            dt = clock.tick(TIME_STEP)
            self.update(dt, pygame.key.get_pressed())
            pygame.display.update()
            await asyncio.sleep(0)


if __name__ == '__main__':
    game = Game("Spellbook")
