import pygame
import math
import random

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
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
ORANGE = (255, 165, 0)

# Player properties
player_x = 400
player_y = 300
player_speed = 3
player_angle = 0
PLAYER_RADIUS = 10

# Enemy properties
enemies = []
ENEMY_SPEED = 1
MAX_ENEMIES = 5
ENEMY_SPAWN_RATE = 120  # Frames between enemy spawns
ENEMY_RADIUS = 10

# Hostage properties
hostages = []
MAX_HOSTAGES = 3
HOSTAGE_SPAWN_RATE = 300  # Frames between hostage spawns
HOSTAGE_RADIUS = 8

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

# Score system
score = 0
BULLET_KILL_SCORE = 10
LIGHT_RAY_KILL_SCORE = 20
HOSTAGE_RESCUE_SCORE = 50

# Font for score display
font = pygame.font.Font(None, 36)

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

def spawn_enemy():
    side = random.choice(['top', 'bottom', 'left', 'right'])
    if side == 'top':
        x = random.randint(0, WIDTH)
        y = 0
    elif side == 'bottom':
        x = random.randint(0, WIDTH)
        y = HEIGHT
    elif side == 'left':
        x = 0
        y = random.randint(0, HEIGHT)
    else:
        x = WIDTH
        y = random.randint(0, HEIGHT)
    enemies.append([x, y])

def spawn_hostage():
    x = random.randint(HOSTAGE_RADIUS, WIDTH - HOSTAGE_RADIUS)
    y = random.randint(HOSTAGE_RADIUS, HEIGHT - HOSTAGE_RADIUS)
    hostages.append([x, y])

# Game loop
clock = pygame.time.Clock()
running = True
space_pressed = False
spawn_counter = 0
hostage_spawn_counter = 0

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

    # Keep player within screen bounds
    player_x = max(PLAYER_RADIUS, min(WIDTH - PLAYER_RADIUS, player_x))
    player_y = max(PLAYER_RADIUS, min(HEIGHT - PLAYER_RADIUS, player_y))

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

    # Update enemy positions
    for enemy in enemies:
        dx = player_x - enemy[0]
        dy = player_y - enemy[1]
        dist = math.hypot(dx, dy)
        if dist != 0:
            enemy[0] += (dx / dist) * ENEMY_SPEED
            enemy[1] += (dy / dist) * ENEMY_SPEED

    # Spawn enemies
    spawn_counter += 1
    if spawn_counter >= ENEMY_SPAWN_RATE and len(enemies) < MAX_ENEMIES:
        spawn_enemy()
        spawn_counter = 0

    # Spawn hostages
    hostage_spawn_counter += 1
    if hostage_spawn_counter >= HOSTAGE_SPAWN_RATE and len(hostages) < MAX_HOSTAGES:
        spawn_hostage()
        hostage_spawn_counter = 0

    # Check for collisions
    for bullet in bullets[:]:
        for enemy in enemies[:]:
            if math.hypot(bullet[0] - enemy[0], bullet[1] - enemy[1]) < ENEMY_RADIUS + 3:
                bullets.remove(bullet)
                enemies.remove(enemy)
                score += BULLET_KILL_SCORE
                break

    for ray in light_rays[:]:
        for enemy in enemies[:]:
            if math.hypot(ray[0] - enemy[0], ray[1] - enemy[1]) < ENEMY_RADIUS + 5:
                enemies.remove(enemy)
                score += LIGHT_RAY_KILL_SCORE
                break

    # Check for hostage rescue
    for hostage in hostages[:]:
        if math.hypot(player_x - hostage[0], player_y - hostage[1]) < PLAYER_RADIUS + HOSTAGE_RADIUS:
            hostages.remove(hostage)
            score += HOSTAGE_RESCUE_SCORE

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
    pygame.draw.circle(window, WHITE, (int(player_x), int(player_y)), PLAYER_RADIUS)
    
    # Draw bullets
    for bullet in bullets:
        pygame.draw.circle(window, RED, (int(bullet[0]), int(bullet[1])), 3)

    # Draw light rays
    for ray in light_rays:
        start_pos = (int(ray[0]), int(ray[1]))
        end_pos = (int(ray[0] + math.cos(ray[2]) * 50), int(ray[1] + math.sin(ray[2]) * 50))
        pygame.draw.line(window, YELLOW, start_pos, end_pos, 2)

    # Draw enemies
    for enemy in enemies:
        pygame.draw.circle(window, GREEN, (int(enemy[0]), int(enemy[1])), ENEMY_RADIUS)

    # Draw hostages
    for hostage in hostages:
        pygame.draw.circle(window, ORANGE, (int(hostage[0]), int(hostage[1])), HOSTAGE_RADIUS)

    # Draw score bar
    pygame.draw.rect(window, BLUE, (10, 10, 200, 30))
    score_text = font.render(f"Score: {score}", True, WHITE)
    window.blit(score_text, (20, 15))

    pygame.display.update()
    clock.tick(60)

pygame.quit()