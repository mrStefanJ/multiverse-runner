# =========================
# systems/level_system.py
# =========================
import pygame
import random
from Games.platform2d.data.settings import HEIGHT

def generate_level(level):
    platforms = []
    spikes = []

    x = 0
    while x < 3000:
        width = random.randint(100, 300)
        platforms.append(pygame.Rect(x, HEIGHT - 40, width, 40))
        x += width + random.randint(100, 200)

    finish = pygame.Rect(x, HEIGHT - 150, 50, 150)
    return platforms, spikes, finish
