import pygame
import math

# Initialize Pygame
pygame.init()

# Set up the game window
WIDTH = 800
HEIGHT = 600
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Rapture Rescuer: Checkpoint Charlie Siege")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

# Player properties
player_x = 400
player_y = 300
player_speed = 3
player_angle = 0

# Enemy properties
enemies = []

# Bullet properties
bullets = []
BULLET_SPEED = 10

# Light ray properties
light_rays = []
LIGHT_RAY_SPEED = 15
LIGHT_RAY_DURATION = 30  # frames

# Isometric grid
TILE_WIDTH = 64
TILE_HEIGHT = 32

def iso_to_screen(x, y):
    screen_x = (x - y) * (TILE_WIDTH // 2)
    screen_y = (x + y) * (TILE_HEIGHT // 2)
    return screen_x + WIDTH // 2, screen_y

def draw_tile(x, y, color):
    points = [
        iso_to_screen(x, y),
        iso_to_screen(x + 1, y),
        iso_to_screen(x + 1, y + 1),
        iso_to_screen(x, y + 1)
    ]
    pygame.draw.polygon(window, color, points)

# Game loop
clock = pygame.time.Clock()
running = True
space_pressed = False

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left mouse button
                mouse_x, mouse_y = pygame.mouse.get_pos()
                angle = math.atan2(mouse_y - player_y, mouse_x - player_x)
                bullets.append([player_x, player_y, angle])
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                space_pressed = True
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_SPACE:
                space_pressed = False

    keys = pygame.key.get_pressed()
    
    # Player movement
    if keys[pygame.K_w]:
        player_y -= player_speed
    if keys[pygame.K_s]:
        player_y += player_speed
    if keys[pygame.K_a]:
        player_x -= player_speed
    if keys[pygame.K_d]:
        player_x += player_speed

    # Shoot light ray
    if space_pressed:
        mouse_x, mouse_y = pygame.mouse.get_pos()
        angle = math.atan2(mouse_y - player_y, mouse_x - player_x)
        light_rays.append([player_x, player_y, angle, LIGHT_RAY_DURATION])

    # Update bullet positions
    for bullet in bullets:
        bullet[0] += math.cos(bullet[2]) * BULLET_SPEED
        bullet[1] += math.sin(bullet[2]) * BULLET_SPEED

    # Update light ray positions
    for ray in light_rays:
        ray[0] += math.cos(ray[2]) * LIGHT_RAY_SPEED
        ray[1] += math.sin(ray[2]) * LIGHT_RAY_SPEED
        ray[3] -= 1  # Decrease duration

    # Remove bullets and light rays that are off-screen or expired
    bullets = [b for b in bullets if 0 <= b[0] < WIDTH and 0 <= b[1] < HEIGHT]
    light_rays = [r for r in light_rays if 0 <= r[0] < WIDTH and 0 <= r[1] < HEIGHT and r[3] > 0]

    # Draw everything
    window.fill(BLACK)
    
    # Draw isometric grid
    for x in range(-5, 6):
        for y in range(-5, 6):
            draw_tile(x, y, (50, 50, 50))
    
    # Draw player
    pygame.draw.circle(window, WHITE, (int(player_x), int(player_y)), 10)
    
    # Draw bullets
    for bullet in bullets:
        pygame.draw.circle(window, RED, (int(bullet[0]), int(bullet[1])), 3)

    # Draw light rays
    for ray in light_rays:
        start_pos = (int(ray[0]), int(ray[1]))
        end_pos = (int(ray[0] + math.cos(ray[2]) * 50), int(ray[1] + math.sin(ray[2]) * 50))
        pygame.draw.line(window, YELLOW, start_pos, end_pos, 2)

    pygame.display.update()
    clock.tick(60)

pygame.quit()