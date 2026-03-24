# =========================
# data/settings.py
# =========================
import pygame

WIDTH, HEIGHT = 800, 700
FPS = 60

# COLORS
WHITE = (255, 255, 255)
BLUE = (50, 150, 255)
ORANGE = (255, 165, 0)
PURPLE = (128, 0, 128)
BROWN = (165, 42, 42)
BLACK = (0, 0, 0)
GREEN = (50, 200, 50)
DARK_GREEN = (0, 100, 0)
GOLD = (255, 215, 0)
RED = (200, 0, 0)
GRAY = (150, 150, 150)
YELLOW = (230, 230, 0)

# Globalne varijable
shape_options = ["SQUARE", "CIRCLE", "TRIANGLE"]
color_options = [BLUE, ORANGE, PURPLE, BROWN]
color_names = ["BLUE", "ORANGE", "PURPLE", "BROWN"]
current_shape_idx = 0
current_color_idx = 0

lives = 5
death_timer = 0
death_reason = ""
total_time_second = 180
final_time_display = ""
trail_positions = []
particles = []

# Fisics
player = pygame.Rect(100, HEIGHT - 150, 50, 50)
gravity = 0.5
jump_strength = 14
on_ground = False
on_platform = None
current_rotate = 0
scroll = 0
finish_line = pygame.Rect(0, 0, 0, 0)
all_platforms = []
spikes = []
projectiles = []
last_projectile_time = 0
projectiles_to_fire = 0
next_shot_delay = 200
last_shot_time = 0
