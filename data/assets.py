# =========================
# data/assets.py
# =========================
import pygame
import os
import sys
import data.settings as settings

# =========================
# PATH FIX (DEV + BUILD)
# =========================
def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS  # PyInstaller
    except AttributeError:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


# =========================
# GLOBAL ASSETS
# =========================
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

bg_music_path = None


# =========================
# SAFE LOADERS
# =========================
def load_sound(path):
    try:
        return pygame.mixer.Sound(resource_path(path))
    except Exception as e:
        print(f"[ASSETS] Sound load failed: {path} -> {e}")
        return None


def load_image(path, scale=None):
    try:
        img = pygame.image.load(resource_path(path)).convert_alpha()
        if scale:
            img = pygame.transform.scale(img, scale)
        return img
    except Exception as e:
        print(f"[ASSETS] Image load failed: {path} -> {e}")
        return None


# =========================
# MAIN LOAD
# =========================
def load_assets():
    global jump_sound, shoot_sound, boom_sound
    global heart_img, clock_img, finish_img, sky_img, bg_width
    global font_main, font_ui, font_small
    global bg_music_path

    # ---------- FONTS ----------
    font_main = pygame.font.SysFont("Arial", 60, bold=True)
    font_ui = pygame.font.SysFont("Arial", 30, bold=True)
    font_small = pygame.font.SysFont("Arial", 20)

    # ---------- SOUNDS ----------
    jump_sound = load_sound("assets/sounds/jump.wav")
    shoot_sound = load_sound("assets/sounds/shoot.wav")
    boom_sound = load_sound("assets/sounds/boom.wav")

    if jump_sound: jump_sound.set_volume(0.4)
    if shoot_sound: shoot_sound.set_volume(0.4)
    if boom_sound: boom_sound.set_volume(0.4)

    # ---------- MUSIC (SAMO PATH) ----------
    bg_music_path = resource_path("assets/sounds/peaceful-background-sound.mp3")

    # ---------- IMAGES ----------
    heart_img = load_image("assets/images/hearth.png", (30, 30))
    clock_img = load_image("assets/images/timer.png", (30, 30))
    finish_img = load_image("assets/images/flag.png", (50, 100))

    sky_img = load_image("assets/images/sky.png", (settings.WIDTH, settings.HEIGHT))
    if sky_img:
        bg_width = sky_img.get_width()

    print("[ASSETS] Loaded")