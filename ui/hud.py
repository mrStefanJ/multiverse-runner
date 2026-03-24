# =========================
# ui/hud.py
# =========================
import pygame

def draw_hud(screen, lives, level):
    font = pygame.font.SysFont(None, 30)
    screen.blit(font.render(f"Lives: {lives}", True, (255,255,255)), (10,10))
    screen.blit(font.render(f"Level: {level}", True, (255,255,255)), (10,40))
