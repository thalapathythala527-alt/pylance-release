import pygame
import random

# Initialize
pygame.init()
WIDTH, HEIGHT = 400, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 48)

# Colors
BLUE = (0, 150, 255)
WHITE = (255, 255, 255)
CORAL = (255, 100, 100)

# Fish
fish_img = pygame.Surface((40, 30))
fish_img.fill((255, 200, 0))
fish_rect = fish_img.get_rect(center=(100, HEIGHT//2))
gravity = 0.5
velocity = 0

# Coral obstacles
corals = []
gap = 150
coral_width = 60
coral_speed = 3

def create_coral():
    top_height = random.randint(50, HEIGHT - gap - 50)
    bottom_height = HEIGHT - top_height - gap
    top = pygame.Rect(WIDTH, 0, coral_width, top_height)
    bottom = pygame.Rect(WIDTH, HEIGHT - bottom_height, coral_width, bottom_height)
    return top, bottom

# Game loop
score = 0
running = True
coral_timer = pygame.USEREVENT + 1
pygame.time.set_timer(coral_timer, 1500)

while running:
    screen.fill(BLUE)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            velocity = -8
        if event.type == coral_timer:
            corals.append(create_coral())

    # Fish movement
    velocity += gravity
    fish_rect.y += int(velocity)

    # Draw fish
    screen.blit(fish_img, fish_rect)

    # Move and draw corals
    for top, bottom in corals:
        top.x -= coral_speed
        bottom.x -= coral_speed
        pygame.draw.rect(screen, CORAL, top)
        pygame.draw.rect(screen, CORAL, bottom)

    # Collision
    for top, bottom in corals:
        if fish_rect.colliderect(top) or fish_rect.colliderect(bottom):
            running = False
    if fish_rect.top <= 0 or fish_rect.bottom >= HEIGHT:
        running = False

    # Score
    score_text = font.render(str(score), True, WHITE)
    screen.blit(score_text, (WIDTH//2, 20))

    # Update score
    for top, _ in corals:
        if top.x + coral_width == fish_rect.x:
            score += 1

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
