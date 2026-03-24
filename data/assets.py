# =========================
# data/assets.py
# =========================
import pygame
import data.settings as settings

jump_sound = None
shoot_sound = None
boom_sound = None
heart_img = None
clock_img = None
finish_img = None
sky_img = None
bg_width = 0

font_main = None
font_ui = None
font_small = None

def load_assets():
    global jump_sound, shoot_sound, boom_sound
    global heart_img, clock_img, finish_img, sky_img, bg_width
    global font_main, font_ui, font_small

    font_main = pygame.font.SysFont("Arial", 60, bold=True)
    font_ui = pygame.font.SysFont("Arial", 30, bold=True)
    font_small = pygame.font.SysFont("Arial", 20)

    # --- SOUNDS ---
    try:
        jump_sound = pygame.mixer.Sound("assets/sounds/jump.wav")
        shoot_sound = pygame.mixer.Sound("assets/sounds/shoot.wav")
        boom_sound = pygame.mixer.Sound("assets/sounds/boom.wav")

        pygame.mixer.music.load("assets/sounds/peaceful-background-sound.mp3")
        pygame.mixer.music.set_volume(0.5)

        jump_sound.set_volume(0.4)
        shoot_sound.set_volume(0.4)
        boom_sound.set_volume(0.4)

    except (pygame.error, FileNotFoundError) as e:
        print(f"Warning: Problem for sounds -> {e}")

    # --- IMAGES ---
    try:
        heart_img = pygame.image.load("assets/images/hearth.png")
        heart_img = pygame.transform.scale(heart_img, (30, 30))

        clock_img = pygame.image.load("assets/images/timer.png")
        clock_img = pygame.transform.scale(clock_img, (30, 30))

        finish_img = pygame.image.load("assets/images/flag.png")
        finish_img = pygame.transform.scale(finish_img, (50, 100))

        sky_img = pygame.image.load("assets/images/sky.png")
        sky_img = pygame.transform.scale(sky_img, (settings.WIDTH, settings.HEIGHT))
        bg_width = sky_img.get_width()

    except (pygame.error, FileNotFoundError) as e:
        print(f"Upozorenje: Problem sa slikama -> {e}")