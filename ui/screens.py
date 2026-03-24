# =========================
# ui/screens.py
# =========================
import pygame

def draw_game_over(screen):
    font = pygame.font.SysFont(None, 60)
    text = font.render("GAME OVER", True, (255,0,0))
    screen.blit(text, (200,300))
