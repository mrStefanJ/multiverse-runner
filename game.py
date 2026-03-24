# =========================
# game.py
# =========================
import pygame
from Games.platform2d.player import Player
from systems.level_system import generate_level
from systems.particle_system import update_particles, draw_particles, create_explosion
from systems.projectile_system import update_projectiles, draw_projectiles
from ui.menu import draw_menu
from ui.hud import draw_hud
from ui.screens import draw_game_over

class Game:
    def __init__(self):
        self.state = "MENU"
        self.player = Player()
        self.level = 1
        self.lives = 5
        self.scroll = 0
        self.platforms, self.spikes, self.finish = generate_level(self.level)
        self.projectiles = []
        self.particles = []

    def handle_event(self, event):
        if self.state == "MENU":
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                self.state = "PLAYING"

        elif self.state == "PLAYING":
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.player.jump()

    def update(self):
        if self.state != "PLAYING":
            return

        keys = pygame.key.get_pressed()
        self.player.move(keys, self.platforms)

        update_projectiles(self.projectiles, self.player, self)
        update_particles(self.particles)

        if self.player.rect.top > 600:
            self.lives -= 1
            create_explosion(self.player.rect.centerx, self.player.rect.centery, (255,0,0), self.particles)
            if self.lives <= 0:
                self.state = "GAMEOVER"

    def draw(self, screen):
        screen.fill((10,10,30))

        if self.state == "MENU":
            draw_menu(screen)
            return

        if self.state == "GAMEOVER":
            draw_game_over(screen)
            return

        for p in self.platforms:
            pygame.draw.rect(screen, (0,255,0), (p.x - self.scroll, p.y, p.width, p.height))

        draw_projectiles(screen, self.projectiles, self.scroll)
        draw_particles(screen, self.particles, self.scroll)

        self.player.draw(screen, self.scroll)
        draw_hud(screen, self.lives, self.level)