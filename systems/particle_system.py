# =========================
# systems/particle_system.py
# =========================
import pygame

def create_explosion(x, y, color, particles):
    import random
    for _ in range(30):
        particles.append([x, y, random.uniform(-5,5), random.uniform(-5,5), 255, color])


def update_particles(particles):
    for p in particles[:]:
        p[0] += p[2]
        p[1] += p[3]
        p[4] -= 5
        if p[4] <= 0:
            particles.remove(p)


def draw_particles(screen, particles, scroll):
    for p in particles:
        surf = pygame.Surface((5,5), pygame.SRCALPHA)
        surf.fill((*p[5], p[4]))
        screen.blit(surf, (p[0] - scroll, p[1]))