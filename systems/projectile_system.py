# =========================
# systems/projectile_system.py
# =========================
import pygame

def update_projectiles(projectiles, player, game):
    for p in projectiles[:]:
        p.x -= 5
        if p.colliderect(player.rect):
            game.lives -= 1
            projectiles.remove(p)


def draw_projectiles(screen, projectiles, scroll):
    for p in projectiles:
        pygame.draw.rect(screen, (255,0,0), (p.x - scroll, p.y, p.width, p.height))
