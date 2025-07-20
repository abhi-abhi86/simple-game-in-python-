import pygame
import random

# Initialize Pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Simple Car Game")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

# Player car properties
player_car_width = 50
player_car_height = 80
player_car_x = (SCREEN_WIDTH / 2) - (player_car_width / 2)
player_car_y = SCREEN_HEIGHT - player_car_height - 20
player_car_speed = 5

# Obstacle properties
obstacle_width = 50
obstacle_height = 80
obstacle_speed = 7
obstacles = []

# Game loop variables
running = True
clock = pygame.time.Clock()
score = 0
font = pygame.font.Font(None, 36)

def draw_player_car(x, y):
    pygame.draw.rect(screen, BLACK, (x, y, player_car_width, player_car_height))

def draw_obstacle(x, y):
    pygame.draw.rect(screen, RED, (x, y, obstacle_width, obstacle_height))

def game_over_screen():
    game_over_text = font.render("Game Over! Score: " + str(score), True, BLACK)
    restart_text = font.render("Press 'R' to Restart or 'Q' to Quit", True, BLACK)
    screen.blit(game_over_text, (SCREEN_WIDTH / 2 - game_over_text.get_width() / 2, SCREEN_HEIGHT / 2 - 50))
    screen.blit(restart_text, (SCREEN_WIDTH / 2 - restart_text.get_width() / 2, SCREEN_HEIGHT / 2 + 10))
    pygame.display.update()

    waiting_for_input = True
    while waiting_for_input:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    return True  # Restart game
                elif event.key == pygame.K_q:
                    pygame.quit()
                    quit()
        clock.tick(15) # Limit frame rate while waiting for input

# Main game loop
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and player_car_x > 0:
        player_car_x -= player_car_speed
    if keys[pygame.K_RIGHT] and player_car_x < SCREEN_WIDTH - player_car_width:
        player_car_x += player_car_speed

    # Add new obstacles
    if random.randrange(0, 100) < 5:  # Adjust frequency of obstacles
        obstacles.append({"x": random.randrange(0, SCREEN_WIDTH - obstacle_width), "y": -obstacle_height})

    # Move and remove obstacles
    for obstacle in obstacles:
        obstacle["y"] += obstacle_speed
        if obstacle["y"] > SCREEN_HEIGHT:
            obstacles.remove(obstacle)
            score += 1

    # Collision detection
    player_rect = pygame.Rect(player_car_x, player_car_y, player_car_width, player_car_height)
    for obstacle in obstacles:
        obstacle_rect = pygame.Rect(obstacle["x"], obstacle["y"], obstacle_width, obstacle_height)
        if player_rect.colliderect(obstacle_rect):
            if game_over_screen():
                # Reset game state for restart
                player_car_x = (SCREEN_WIDTH / 2) - (player_car_width / 2)
                obstacles = []
                score = 0
            else:
                running = False # Quit game

    # Drawing
    screen.fill(WHITE)
    draw_player_car(player_car_x, player_car_y)
    for obstacle in obstacles:
        draw_obstacle(obstacle["x"], obstacle["y"])

    # Display score
    score_text = font.render("Score: " + str(score), True, BLACK)
    screen.blit(score_text, (10, 10))

    pygame.display.update()
    clock.tick(60)

pygame.quit()

