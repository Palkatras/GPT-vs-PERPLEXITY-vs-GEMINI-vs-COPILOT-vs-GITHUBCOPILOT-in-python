import pygame
import random
import sys

# Initialize
pygame.init()

# Screen
WIDTH = 400
HEIGHT = 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Flappy Bird")

# Clock
clock = pygame.time.Clock()
FPS = 60

# Colors
WHITE = (255, 255, 255)
BLUE = (100, 100, 255)  
GREEN = (0, 200, 0)
RED = (255, 0, 0)

# Bird
bird_x = 100
bird_y = 300
bird_radius = 20
bird_velocity = 0
gravity = 0.5
jump_strength = -10

# Pipes
pipe_width = 60
pipe_gap = 150
pipe_velocity = 3
pipes = []

def create_pipe():
    height = random.randint(100, 400)
    top_rect = pygame.Rect(WIDTH, 0, pipe_width, height)
    bottom_rect = pygame.Rect(WIDTH, height + pipe_gap, pipe_width, HEIGHT)
    return (top_rect, bottom_rect)

# Initial pipes
for i in range(3):
    pipe_x = 300 + i * 200
    pipe_height = random.randint(100, 400)
    pipes.append((pygame.Rect(pipe_x, 0, pipe_width, pipe_height),
                  pygame.Rect(pipe_x, pipe_height + pipe_gap, pipe_width, HEIGHT)))

# Main loop
running = True
while running:
    clock.tick(FPS)
    screen.fill(WHITE)

    # Events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            bird_velocity = jump_strength

    # Bird physics
    bird_velocity += gravity
    bird_y += bird_velocity

    # Bird draw
    pygame.draw.circle(screen, BLUE, (bird_x, int(bird_y)), bird_radius)

    # Move and draw pipes
    for top, bottom in pipes:
        top.x -= pipe_velocity
        bottom.x -= pipe_velocity
        pygame.draw.rect(screen, GREEN, top)
        pygame.draw.rect(screen, GREEN, bottom)

    # Recycle pipes
    if pipes[0][0].x + pipe_width < 0:
        pipes.pop(0)
        new_pipe = create_pipe()
        pipes.append(new_pipe)

    # Collision
    bird_rect = pygame.Rect(bird_x - bird_radius, bird_y - bird_radius, bird_radius * 2, bird_radius * 2)
    for top, bottom in pipes:
        if bird_rect.colliderect(top) or bird_rect.colliderect(bottom):
            print("Game Over!")
            pygame.quit()
            sys.exit()

    # Check if bird is out of screen
    if bird_y > HEIGHT or bird_y < 0:
        print("Game Over!")
        pygame.quit()
        sys.exit()

    pygame.display.update()
