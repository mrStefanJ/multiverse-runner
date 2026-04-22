# =========================
# systems/player.py
# =========================
import data.settings as settings
import data.assets as assets
import pygame

class Player:
    def __init__(self):
        self.rect = pygame.Rect(100, settings.HEIGHT - 150, 50, 50)
        self.velocity_y = 0
        self.on_ground = False
        self.on_platform = None
        self.current_rotate = 0
        self.target_rotate = 0
        self.trail_positions = []

        # NOVO: Brojač skokova
        self.jump_count = 0
        self.max_jumps = 2  # 1 za običan, 2 za dupli

    def jump(self, shape):
        # Proveravamo da li igrač ima preostalih skokova
        if self.on_ground or self.jump_count < self.max_jumps:
            # Ako skače sa zemlje, to je prvi skok. Ako je u vazduhu, jump_count se povećava.
            self.velocity_y = -settings.jump_strength
            self.on_platform = None
            self.on_ground = False  # Čim skoči, više nije na zemlji
            self.jump_count += 1

            if assets.jump_sound: assets.jump_sound.play()

            keys = pygame.key.get_pressed()
            rot_amount = 360 if shape == "TRIANGLE" else 180

            if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
                self.target_rotate -= rot_amount
            elif keys[pygame.K_LEFT] or keys[pygame.K_a]:
                self.target_rotate += rot_amount
            else:
                self.target_rotate -= rot_amount

    def move(self, keys, all_platforms, spikes, projectiles, scroll):
        # Gravitacija
        self.velocity_y += settings.gravity
        self.rect.y += self.velocity_y

        # Privremeno postavljamo na False, provera kolizije će to popraviti ako treba
        was_on_ground = self.on_ground
        self.on_ground = False

        # Kolizija po Y osi
        for p in all_platforms:
            r = p[0] if isinstance(p, list) else p
            if self.rect.colliderect(r):
                if self.velocity_y > 0:  # Pada na platformu
                    self.rect.bottom = r.top
                    self.velocity_y = 0
                    self.on_ground = True
                    self.jump_count = 0  # RESETUJEMO SKOKOVE KADA DOTAKNE ZEMLJU
                    if isinstance(p, list): self.on_platform = p
                elif self.velocity_y < 0:  # Udara glavom odozdo
                    self.rect.top = r.bottom
                    self.velocity_y = 0

        # Horizontalno kretanje
        dx = 0
        if keys[pygame.K_LEFT] or keys[pygame.K_a]: dx = -5
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]: dx = 5

        self.rect.x += dx
        if self.rect.left < scroll: self.rect.left = scroll

        # Kolizija po X osi
        for p in all_platforms:
            r = p[0] if isinstance(p, list) else p
            if self.rect.colliderect(r):
                if dx > 0: self.rect.right = r.left
                if dx < 0: self.rect.left = r.right

        # Ažuriranje senke
        self.trail_positions.append((self.rect.centerx, self.rect.centery, self.current_rotate))
        if len(self.trail_positions) > 8:
            self.trail_positions.pop(0)

        # Glatka rotacija (približavanje target_rotate vrednosti)
        if self.current_rotate < self.target_rotate:
            self.current_rotate += 10
        elif self.current_rotate > self.target_rotate:
            self.current_rotate -= 10
