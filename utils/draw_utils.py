import pygame

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
