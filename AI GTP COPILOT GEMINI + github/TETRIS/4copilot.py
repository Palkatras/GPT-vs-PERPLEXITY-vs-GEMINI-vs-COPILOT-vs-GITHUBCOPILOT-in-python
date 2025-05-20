import pygame
import random

# Initialize pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 300, 600
GRID_SIZE = 30
COLORS = [(255, 0, 0), (255, 165, 0), (255, 255, 0), (0, 255, 0), 
          (0, 255, 255), (0, 0, 255), (128, 0, 128)]  # Rainbow colors

# Shapes of tetriminos
SHAPES = [
    [(0, 0), (1, 0), (0, 1), (1, 1)],  # O
    [(0, 0), (1, 0), (2, 0), (3, 0)],  # I
    [(0, 0), (0, 1), (1, 1), (2, 1)],  # L
    [(2, 0), (0, 1), (1, 1), (2, 1)],  # J
    [(1, 0), (0, 1), (1, 1), (2, 1)],  # T
    [(0, 0), (1, 0), (1, 1), (2, 1)],  # Z
    [(1, 0), (2, 0), (0, 1), (1, 1)]   # S
]

class Tetrimino:
    def __init__(self):
        self.shape = random.choice(SHAPES)
        self.color = random.choice(COLORS)
        self.x = WIDTH // GRID_SIZE // 2
        self.y = 0

    def move(self, dx, dy):
        self.x += dx
        self.y += dy

    def draw(self, screen):
        for pos in self.shape:
            pygame.draw.rect(screen, self.color, 
                             (self.x * GRID_SIZE + pos[0] * GRID_SIZE, 
                              self.y * GRID_SIZE + pos[1] * GRID_SIZE, 
                              GRID_SIZE, GRID_SIZE))

def main():
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()
    tetrimino = Tetrimino()
    
    running = True
    while running:
        screen.fill((0, 0, 0))
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a:
                    tetrimino.move(-1, 0)
                elif event.key == pygame.K_d:
                    tetrimino.move(1, 0)
                elif event.key == pygame.K_s:
                    tetrimino.move(0, 1)
                elif event.key == pygame.K_w:  
                    pass  # Add rotation logic later

        tetrimino.draw(screen)
        pygame.display.flip()
        clock.tick(10)

    pygame.quit()

if __name__ == "__main__":
    main()
