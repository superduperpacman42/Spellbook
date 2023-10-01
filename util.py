import math
import os
import sys

import pygame

from constants import *

images = {}
audio = {}


def load_image(name, number=1, angle=0, scale=PIXEL_RATIO, flip=False):
    """ Loads an image or list of images """
    nameF = name
    if flip:
        nameF = name + "Flip"
    if nameF in images:
        return images[nameF]
    path = 'images/'
    sheet = pygame.image.load(path + name)
    sheet = pygame.transform.scale(sheet, [scale * sheet.get_width(), scale * sheet.get_height()])
    img = []
    w = sheet.get_width() / number
    h = sheet.get_height()
    for i in range(number):
        img.append(sheet.subsurface((w * i, 0, w, h)))
        img[i] = pygame.transform.rotate(img[i], angle)
        img[i] = pygame.transform.flip(img[i], flip, False)
    images[nameF] = img
    return img


def play_music(name):
    """ Plays the given background track """
    path = 'audio/'
    pygame.mixer.music.load(path + name)
    pygame.mixer.music.play(-1)


def stop_music():
    """ Stops the current background track """
    pygame.mixer.music.stop()


def set_volume(val):
    """ Scale volume 0 to 1 """
    pygame.mixer.music.set_volume(val)


def play_sound(name, play=True, volume=1):
    """ Plays the given sound effect """
    if name in audio:
        sound = audio[name]
    else:
        path = 'audio/'
        sound = pygame.mixer.Sound(path + name)
        sound.set_volume(volume)
        audio[name] = sound
    if play:
        sound.play()
    else:
        sound.stop()


def bounds(pose, w, h):
    return -w / 2 < pose.x < w / 2 and -h / 2 < pose.y < h / 2


def skew_grid(x, y, x0=0, y0=0, scale_factor=False):
    """ Skew coordinates relative to grid """
    f = GRID_SCALE
    d = GRID_SCALE
    dy = GRID_SCALE * 2.5
    if scale_factor:
        return d / ((y - dy) * GRID_SKEW + d)
    x = f * x/((y-dy) * GRID_SKEW + d) + x0
    y = f * (y-dy)/((y-dy) * GRID_SKEW + d) + y0 + dy - 120
    return x, y
