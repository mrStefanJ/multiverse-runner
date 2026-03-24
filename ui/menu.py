# =========================
# ui/menu.py
# =========================
import pygame

def draw_menu(screen):
    font = pygame.font.SysFont(None, 60)
    text = font.render("PRESS ENTER", True, (255,255,255))
    screen.blit(text, (200,300))

