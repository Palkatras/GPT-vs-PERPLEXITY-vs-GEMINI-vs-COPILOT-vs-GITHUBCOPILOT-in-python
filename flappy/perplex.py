import pygame
import random

pygame.init()
screen = pygame.display.set_mode((500, 800))
clock = pygame.time.Clock()

# Bird variables
bird_x, bird_y = 100, 400
bird_vel = 0
gravity = 0.5
flap_power = -10

# Pipe variables
pipe_width = 80
pipe_gap = 200
pipe_x = 500
pipe_height = random.randint(150, 600)

score = 0
running = True

while running:
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            bird_vel = flap_power

    bird_vel += gravity
    bird_y += bird_vel

    pipe_x -= 5
    if pipe_x < -pipe_width:
        pipe_x = 500
        pipe_height = random.randint(150, 600)
        score += 1

    # Collision detection (simplified)
    if bird_y > 800 or bird_y < 0 or (pipe_x < bird_x < pipe_x + pipe_width and not (pipe_height < bird_y < pipe_height + pipe_gap)):
        running = False

    screen.fill((135, 206, 235))  # Sky blue
    pygame.draw.rect(screen, (0, 255, 0), (pipe_x, 0, pipe_width, pipe_height))
    pygame.draw.rect(screen, (0, 255, 0), (pipe_x, pipe_height + pipe_gap, pipe_width, 800))
    pygame.draw.circle(screen, (255, 255, 0), (bird_x, int(bird_y)), 20)
    pygame.display.flip()

pygame.quit()
  