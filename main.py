import random
from systems.player_system import Player
from data.highscore import *
from data.settings import *
import data.assets as assets
import pygame


pygame.init()
pygame.mixer.init()
assets.load_assets()

# SCREEN
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Multiverse Runner")

clock = pygame.time.Clock()

game_state = "MENU"
player_shape = shape_options[current_shape_idx]
player_color = color_options[current_color_idx]
current_level_num = 1
menu_selection = 0
pause_start_ticks = 0
start_ticks = 0

player_obj = Player()
high_score = load_highscore()

# --- NOVO: Funkcija za crtanje neona ---
def draw_neon_rect(surf, color, rect, width=2):
    # Crta osnovni pravougaonik i nekoliko svetlijih okvira oko njega za glow efekat
    for i in range(3, 0, -1):
        alpha = 100 // i
        s = pygame.Surface((rect.width + i*2, rect.height + i*2), pygame.SRCALPHA)
        pygame.draw.rect(s, (*color, alpha), (0, 0, rect.width + i*2, rect.height + i*2), border_radius=5)
        surf.blit(s, (rect.x - i, rect.y - i))
    pygame.draw.rect(surf, color, rect, border_radius=2)

def draw_player_shape(color, size, shape_type, angle, alpha=255):
    temp_surf = pygame.Surface((size, size), pygame.SRCALPHA)
    draw_color = (*color, alpha) if len(color) == 3 else color
    if shape_type == "SQUARE":
        pygame.draw.rect(temp_surf, draw_color, (0, 0, size, size))
    elif shape_type == "CIRCLE":
        pygame.draw.circle(temp_surf, draw_color, (size // 2, size // 2), size // 2)
    elif shape_type == "TRIANGLE":
        pygame.draw.polygon(temp_surf, draw_color, [(size // 2, 0), (0, size), (size, size)])
    return pygame.transform.rotate(temp_surf, angle)

def create_explosion(x, y, color):
    global particles
    for _ in range(30):
        vel_x = random.uniform(-8, 8)
        vel_y = random.uniform(-8, 8)
        size = random.randint(4, 12)
        particles.append([x, y, vel_x, vel_y, size, 255, color])

def reset_game(full_reset=False):
    global player_obj, scroll, game_state, all_platforms, finish_line, lives, start_ticks, spikes, projectiles, current_level_num, particles, death_timer, last_projectile_time

    pygame.mixer.music.play(-1)
    last_projectile_time = pygame.time.get_ticks()
    player_obj = Player()
    scroll = 0
    death_timer = 0
    particles = []
    start_ticks = pygame.time.get_ticks()

    if full_reset:
        lives = 5
        current_level_num = 1
        game_state = "PLAYING"

    all_platforms = []
    spikes = []
    projectiles = []
    level_width = 8000
    current_x = 0
    ground_widths = [150, 300, 500]
    while current_x < level_width:
        p_w = random.choice(ground_widths)
        gap = random.randint(110, 210)
        all_platforms.append(pygame.Rect(current_x, HEIGHT - 40, p_w, 40)) # Malo deblje platforme
        if current_level_num in [4, 5, 6, 10] and current_x > 500:
            if p_w > 250:
                spikes.append(pygame.Rect(current_x + random.randint(50, p_w - 50), HEIGHT - 60, 30, 20))
        current_x += p_w + gap

    air_widths = [80, 120, 160]
    for _ in range(25):
        v_w = random.choice(air_widths)
        v_x = random.randint(400, level_width - 400)
        v_y = random.randint(200, 450)
        plat_rect = pygame.Rect(v_x, v_y, v_w, 25)
        speed = random.choice([-3, -2, 2, 3]) if current_level_num >= 7 else 0
        all_platforms.append([plat_rect, speed, v_x, 150])

    finish_line = pygame.Rect(level_width, HEIGHT - 150, 50, 150)

def die(reason="SPIKE"):
    global lives, game_state, death_timer, death_reason, boom_sound, current_level_num
    if game_state == "PLAYING":
        create_explosion(player_obj.rect.centerx, player_obj.rect.centery, player_color)
        pygame.mixer.music.stop()
        if assets.boom_sound:
            assets.boom_sound.play()
        lives -= 1
        death_timer = pygame.time.get_ticks()
        if lives <= 0:
            save_highscore(current_level_num, "DEAD")
        game_state = "EXPLODING"

def move_player(keys):
    global scroll, game_state, projectiles, final_time_display, last_projectile_time, particles

    if game_state == "EXPLODING":
        if pygame.time.get_ticks() - death_timer > 1500:
            if lives > 0:
                reset_game(False)
                game_state = "PLAYING"
            else:
                game_state = "GAMEOVER"
        return
    # da se igrac rotira kada dodje do cilja
    if game_state == "LEVEL_WIN":
        player_obj.current_rotate += 20
        return

    if game_state != "PLAYING": return

    if current_level_num >= 7:
        now = pygame.time.get_ticks()
        if now - last_projectile_time > 1800:
            proj_y = random.randint(200,HEIGHT - 100)
            projectiles.append(pygame.Rect(scroll + WIDTH + 50, proj_y, 40, 20))
            # pustanje zvuka
            if assets.shoot_sound:
                assets.shoot_sound.play()
            last_projectile_time = now

    for a in projectiles[:]:
        a.x -= 8
        if a.colliderect(player_obj.rect):
            die()
            if a in projectiles: projectiles.remove(a)
        elif a.right < scroll:
            projectiles.remove(a)

    for p in all_platforms:
        if isinstance(p, list) and p[1] != 0:
            p[0].x += p[1]
            if abs(p[0].x - p[2]) > p[3]: p[1] *= -1
            if player_obj.on_platform == p:
                player_obj.rect.x += p[1]

    player_obj.move(keys, all_platforms, spikes, projectiles, scroll)

    # --- NOVO: Particle trail (prašina dok trči) ---
    if player_obj.on_platform and abs(player_obj.velocity_y) > 0.1:
        if random.random() > 0.7:
            particles.append([player_obj.rect.centerx, player_obj.rect.bottom, random.uniform(-1, 1), random.uniform(-1, 0), random.randint(2, 5), 150, GRAY])

    if player_obj.rect.top > HEIGHT:
        die("PIT")
        return

    for s in spikes:
        if player_obj.rect.colliderect(s): die()

    if player_obj.rect.colliderect(finish_line):
        elapsed_seconds = (pygame.time.get_ticks() - start_ticks) // 1000
        save_if_best(current_level_num, elapsed_seconds)
        final_time_display = f"{elapsed_seconds // 60:02}:{elapsed_seconds % 60:02}"
        game_state = "LEVEL_WIN"

    if player_obj.rect.centerx > WIDTH // 2 + scroll:
        scroll = player_obj.rect.centerx - WIDTH // 2

def draw():
    global game_state, menu_selection, particles, death_timer, high_score
    screen.fill((10, 10, 30))

    if game_state in ["PLAYING", "LEVEL_WIN", "EXIT_PROMPT", "WIN", "EXPLODING"]:
        if assets.sky_img:
            bg_offset_x = -(scroll * 0.6 % assets.bg_width)
            screen.blit(assets.sky_img, (bg_offset_x, 0))
            screen.blit(assets.sky_img, (bg_offset_x + assets.bg_width, 0))

    # --- GLAVNI MENIJI (Overlay ekrani) ---
    if game_state == "MENU":
        overlay = pygame.Surface((WIDTH, HEIGHT))
        overlay.fill(BLACK)
        overlay.set_alpha(200)
        screen.blit(overlay, (0, 0))
        title = assets.font_main.render("MULTIVERSE RUNNER", True, GOLD)
        screen.blit(title, (WIDTH // 2 - 280, 80))
        hs_text = assets.font_ui.render(f"BEST LEVEL: {high_score}", True, BLUE)
        screen.blit(hs_text, (WIDTH // 2 - 90, 160))

        options = ["START GAME", f"CUSTOMIZE: {player_shape}/{color_names[current_color_idx]}", "CONTROLS", "BEST TIME",
                   "HISTORY", "EXIT"]
        for i, text in enumerate(options):
            color = WHITE if menu_selection == i else GRAY
            txt = assets.font_ui.render(text, True, color)
            tx, ty = WIDTH // 2 - 180, 220 + i * 65
            screen.blit(txt, (tx, ty))
            if i == 1:
                help_txt = assets.font_small.render("Use Left/Right for Shape, Enter for Color", True, GRAY)
                screen.blit(help_txt, (tx, ty + 35))
            if menu_selection == i:
                pygame.draw.polygon(screen, player_color, [(tx - 40, ty + 10), (tx - 40, ty + 30), (tx - 20, ty + 20)])

        preview = draw_player_shape(player_color, 80, player_shape, pygame.time.get_ticks() // 10)
        screen.blit(preview, (WIDTH - 150, 250))

    elif game_state == "CONTROLS":
        overlay = pygame.Surface((WIDTH, HEIGHT))
        overlay.fill(BLACK)
        overlay.set_alpha(200)
        screen.blit(overlay, (0, 0))
        title = assets.font_main.render("CONTROLS", True, GOLD)
        screen.blit(title, (WIDTH // 2 - 150, 80))
        ctrls = ["W/UP/SPACE - Jump/Double Jump", "A/LEFT - Move Left", "D/RIGHT - Move Right", "ESC - Back"]
        for i, line in enumerate(ctrls):
            screen.blit(assets.font_ui.render(line, True, WHITE), (WIDTH // 2 - 180, 220 + i * 50))
        screen.blit(assets.font_ui.render("Press ESC to Back", True, BLUE), (WIDTH // 2 - 120, HEIGHT - 80))

    elif game_state == "BEST TIME":
        overlay = pygame.Surface((WIDTH, HEIGHT))
        overlay.fill(BLACK)
        overlay.set_alpha(230)
        screen.blit(overlay, (0, 0))
        title_surf = assets.font_main.render("PERSONAL RECORDS", True, GOLD)
        screen.blit(title_surf, (WIDTH // 2 - title_surf.get_width() // 2, 50))

        best_times = load_best_times()
        start_y, row_height, column_gap = 180, 70, 350
        left_margin = (WIDTH // 2) - 250

        total_seconds = 0 # za sabiranje vremena

        for lvl in range(1, 11):
            lvl_str = str(lvl)
            time_val = best_times.get(lvl_str)

            if time_val:
                total_seconds += time_val  # Dodajemo u ukupno vreme
                display_time = f"{time_val // 60:02}:{time_val % 60:02}"
                color = GREEN
            else:
                display_time = "--:--"
                color = GRAY

            rec_text = assets.font_ui.render(f"Lvl {lvl:02}: {display_time}", True, color)
            col_idx, row_idx = (0 if lvl <= 5 else 1), (lvl - 1) % 5
            screen.blit(rec_text, (left_margin + col_idx * column_gap, start_y + row_idx * row_height))

        total_text = f"TOTAL MULTIVERSE TIME: {total_seconds // 60:02}:{total_seconds % 60:02}"
        # Ako nije pređen nijedan nivo, pišemo 00:00 ili ostavljamo prazno
        total_surf = assets.font_ui.render(total_text, True, GOLD)
        screen.blit(total_surf, (WIDTH // 2 - total_surf.get_width() // 2, start_y + 5 * row_height + 20))

        exit_surf = assets.font_ui.render("Press ESC to Back", True, BLUE)
        screen.blit(exit_surf, (WIDTH // 2 - exit_surf.get_width() // 2, HEIGHT - 70))


    elif game_state == "HISTORY":
        overlay = pygame.Surface((WIDTH, HEIGHT))
        overlay.fill(BLACK)
        overlay.set_alpha(230)  # Isti nivo zatamnjenja kao u BEST TIME
        screen.blit(overlay, (0, 0))
        # Centriran naslov
        title_surf = assets.font_main.render("LAST ATTEMPTS", True, GOLD)
        screen.blit(title_surf, (WIDTH // 2 - title_surf.get_width() // 2, 50))
        history = get_score_history()
        start_y = 160
        row_height = 50

        for i, entry in enumerate(history):
            # Boje prilagođene tvom stilu:
            # Zelena za COMPLETE, Crvena za DEAD, Svetlo plava za ostalo
            if "COMPLETE" in entry:
                color = GREEN
            elif "DEAD" in entry:
                color = RED
            else:
                color = WHITE  # Ili GRAY
            # Renderovanje teksta istorije
            entry_surf = assets.font_ui.render(entry, True, color)
            # Centriranje svakog reda
            screen.blit(entry_surf, (WIDTH // 2 - entry_surf.get_width() // 2, start_y + i * row_height))

        # Dugme za povratak centrirano na dnu
        exit_surf = assets.font_ui.render("Press ESC to Back", True, BLUE)
        screen.blit(exit_surf, (WIDTH // 2 - exit_surf.get_width() // 2, HEIGHT - 70))

    else:
        # --- IGRA (PLATFORME, ŠILJCI, PROJEKTILI) ---
        for p in all_platforms:
            r = p[0].copy() if isinstance(p, list) else p.copy()
            r.x -= scroll
            # Koristimo neon stil za platforme
            p_color = YELLOW if (isinstance(p, list) and p[1] != 0) else (50, 255, 50)
            # Ako imaš funkciju draw_neon_rect, pozovi je ovde. Ako ne, običan rect:
            pygame.draw.rect(screen, p_color, r, border_radius=3)

        for s in spikes:
            sc = s.copy()
            sc.x -= scroll
            pygame.draw.polygon(screen, RED, [sc.bottomleft, sc.midtop, sc.bottomright])

        for a in projectiles:
            ac = a.copy()
            ac.x -= scroll
            pygame.draw.rect(screen, BLACK, ac)

        # Finish line
        if assets.finish_img:
            img_h = assets.finish_img.get_height()
            screen.blit(assets.finish_img, (finish_line.x - scroll, HEIGHT - 40 - img_h))
        else:
            f = finish_line.copy()
            f.x -= scroll
            pygame.draw.rect(screen, GOLD, f)

        # Čestice (Particles)
        for p in particles[:]:
            p[0] += p[2]
            p[1] += p[3]
            p[5] -= 5
            if p[5] <= 0:
                particles.remove(p)
            else:
                s = pygame.Surface((p[4], p[4]), pygame.SRCALPHA)
                s.fill((*p[6], p[5]))
                screen.blit(s, (p[0] - scroll, p[1]))

        # --- IGRAČ I TRAIL ---
        if game_state in ["PLAYING", "LEVEL_WIN", "EXIT_PROMPT", "WIN"]:
            for i, pos in enumerate(player_obj.trail_positions):
                t = draw_player_shape(player_color, 50, player_shape, pos[2], (i + 1) * 25)
                screen.blit(t, t.get_rect(center=(pos[0] - scroll, pos[1])).topleft)

            if game_state != "EXPLODING":
                p_img = draw_player_shape(player_color, 50, player_shape, player_obj.current_rotate)
                screen.blit(p_img,
                            p_img.get_rect(center=(player_obj.rect.centerx - scroll, player_obj.rect.centery)).topleft)

        # --- UI (Srca, Level, Sat) ---
        if assets.heart_img:
            screen.blit(assets.heart_img, (20, 25))
            screen.blit(assets.font_ui.render(f"{lives}", True, RED), (60, 20))

        # Level text - bela boja se bolje vidi na tamnom
        screen.blit(assets.font_ui.render(f"LVL {current_level_num}", True, WHITE), (WIDTH // 2 - 40, 20))

        time_ref = pause_start_ticks if game_state == "EXIT_PROMPT" else pygame.time.get_ticks()
        elapsed = (time_ref - start_ticks) // 1000
        t_left = max(0, total_time_second - elapsed)
        disp = final_time_display if game_state == "LEVEL_WIN" else f"{t_left // 60:02}:{t_left % 60:02}"

        if assets.clock_img:
            screen.blit(assets.clock_img, (WIDTH - 180, 25))
            screen.blit(assets.font_ui.render(disp, True, WHITE), (WIDTH - 140, 20))

        # --- OVERLAY STANJA (EXIT, WIN, GAMEOVER) ---
        if game_state == "EXIT_PROMPT":
            overlay = pygame.Surface((WIDTH, HEIGHT))
            overlay.fill(BLACK)
            overlay.set_alpha(150)
            screen.blit(overlay, (0, 0))
            # pygame.draw.rect(screen, WHITE, (WIDTH // 2 - 200, HEIGHT // 2 - 100, 400, 200), border_radius=15)
            screen.blit(assets.font_ui.render("Exit?", True, WHITE), (WIDTH // 2 - 40, HEIGHT // 2 - 60))
            y_c = RED if menu_selection == 0 else GRAY
            n_c = GREEN if menu_selection == 1 else GRAY
            screen.blit(assets.font_ui.render("YES", True, y_c), (WIDTH // 2 - 100, HEIGHT // 2 + 20))
            screen.blit(assets.font_ui.render("NO", True, n_c), (WIDTH // 2 + 30, HEIGHT // 2 + 20))

        elif game_state == "LEVEL_WIN":
            overlay = pygame.Surface((WIDTH, HEIGHT))
            overlay.fill((0, 100, 0))
            overlay.set_alpha(180)
            screen.blit(overlay, (0, 0))
            screen.blit(assets.font_main.render(f"LEVEL {current_level_num} DONE!", True, WHITE), (WIDTH // 2 - 200, 250))
            screen.blit(assets.font_ui.render("Press ENTER to go to next level", True, WHITE), (WIDTH // 2 - 180, 330))

        elif game_state == "WIN":
            overlay = pygame.Surface((WIDTH, HEIGHT))
            overlay.fill(GOLD)
            overlay.set_alpha(200)
            screen.blit(overlay, (0, 0))
            screen.blit(assets.font_main.render("YOU BEAT THE MULTIVERSE!", True, BLACK), (WIDTH // 2 - 350, 250))
            screen.blit(assets.font_ui.render("Press ENTER for Menu", True, BLACK), (WIDTH // 2 - 150, 350))

        elif game_state == "GAMEOVER":
            if assets.sky_img:
                bg_offset_x = -(scroll * 0.6 % assets.bg_width)
                screen.blit(assets.sky_img, (bg_offset_x, 0))
                screen.blit(assets.sky_img, (bg_offset_x + assets.bg_width, 0))

            overlay = pygame.Surface((WIDTH, HEIGHT))
            overlay.fill((10,10,40))
            overlay.set_alpha(160)
            screen.blit(overlay, (0, 0))
            screen.blit(assets.font_main.render("GAME OVER", True, WHITE), (WIDTH // 2 - 160, 250))
            res_c = GREEN if menu_selection == 0 else GRAY
            ext_c = RED if menu_selection == 1 else GRAY
            screen.blit(assets.font_ui.render("RESET", True, res_c), (WIDTH // 2 - 150, 350))
            screen.blit(assets.font_ui.render("EXIT", True, ext_c), (WIDTH // 2 + 50, 350))

    pygame.display.flip()

# Main Loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: running = False
        if event.type == pygame.KEYDOWN:
            if game_state == "MENU":
                if event.key in [pygame.K_UP, pygame.K_w]: menu_selection = (menu_selection - 1) % 6
                if event.key in [pygame.K_DOWN, pygame.K_s]: menu_selection = (menu_selection + 1) % 6
                if menu_selection == 1:
                    if event.key in [pygame.K_RIGHT, pygame.K_d]:
                        current_shape_idx = (current_shape_idx + 1) % 3
                        player_shape = shape_options[current_shape_idx]
                    elif event.key in [pygame.K_LEFT, pygame.K_a]:
                        current_shape_idx = (current_shape_idx - 1) % 3
                        player_shape = shape_options[current_shape_idx]
                if event.key == pygame.K_RETURN:
                    if menu_selection == 0:  # START GAME
                        reset_game(True)
                    elif menu_selection == 1:  # CUSTOMIZE (Color)
                        current_color_idx = (current_color_idx + 1) % 4
                        player_color = color_options[current_color_idx]
                    elif menu_selection == 2:  # CONTROLS
                        game_state = "CONTROLS"
                    elif menu_selection == 3:  # BEST TIME (Ovo je bila greška)
                        game_state = "BEST TIME"
                    elif menu_selection == 4:  # HISTORY
                        game_state = "HISTORY"
                    elif menu_selection == 5:  # EXIT
                        running = False

            elif game_state == "PLAYING":
                if event.key == pygame.K_ESCAPE:
                    game_state = "EXIT_PROMPT"
                    menu_selection = 1
                    pause_start_ticks = pygame.time.get_ticks()
                if event.key in [pygame.K_UP, pygame.K_w, pygame.K_SPACE]:
                    player_obj.jump(player_shape)

            elif game_state == "BEST TIME" and event.key == pygame.K_ESCAPE:
                game_state = "MENU"

            elif game_state == "HISTORY" and event.key == pygame.K_ESCAPE:
                game_state = "MENU"

            elif game_state == "EXIT_PROMPT":
                if event.key in [pygame.K_LEFT, pygame.K_a]: menu_selection = 0
                if event.key in [pygame.K_RIGHT, pygame.K_d]: menu_selection = 1
                if event.key == pygame.K_y or (
                        event.key == pygame.K_RETURN and menu_selection == 0): game_state = "MENU"
                if event.key in [pygame.K_n, pygame.K_ESCAPE] or (event.key == pygame.K_RETURN and menu_selection == 1):
                    start_ticks += (pygame.time.get_ticks() - pause_start_ticks)
                    game_state = "PLAYING"

            elif game_state == "LEVEL_WIN" and event.key == pygame.K_RETURN:
                if current_level_num >= 10:
                    save_highscore(10, "COMPLETE")  # Čuvaj samo kad pređe 10. nivo
                    game_state = "WIN"
                else:
                    current_level_num += 1
                    if current_level_num > high_score: high_score = current_level_num
                    reset_game(False)
                    game_state = "PLAYING"

            elif game_state == "WIN" and event.key == pygame.K_RETURN:
                game_state = "MENU"


            elif game_state == "GAMEOVER":
                # Kretanje kroz meni (RESET ili EXIT)
                if event.key in [pygame.K_LEFT, pygame.K_a]: menu_selection = 0
                if event.key in [pygame.K_RIGHT, pygame.K_d]: menu_selection = 1
                # Akcija
                if event.key == pygame.K_RETURN:
                    if menu_selection == 0:
                        reset_game(True)

                    elif menu_selection == 1:
                        game_state = "MENU"

            elif game_state == "CONTROLS" and event.key == pygame.K_ESCAPE:
                game_state = "MENU"

        if event.type == pygame.KEYUP and game_state == "PLAYING":
            if event.key in [pygame.K_UP, pygame.K_w, pygame.K_SPACE]:
                if player_obj.velocity_y < -4:
                    player_obj.velocity_y = -4

    move_player(pygame.key.get_pressed())
    draw()
    clock.tick(60)

pygame.quit()