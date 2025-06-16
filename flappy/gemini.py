import pygame
import random

# --- Constants ---
SCREEN_WIDTH = 288
SCREEN_HEIGHT = 512
FPS = 60

BIRD_X = 50 # Bird's fixed X position

GRAVITY = 0.5
JUMP_STRENGTH = -8

PIPE_WIDTH = 52
PIPE_GAP = 100 # Gap between top and bottom pipe
PIPE_SPEED = 3

BIRD_SIZE = 24 # Size for our square bird

# --- Colors ---
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
SKY_BLUE = (135, 206, 235) # Background color
BIRD_YELLOW = (255, 255, 0)
PIPE_GREEN = (0, 128, 0)
GROUND_BROWN = (222, 184, 135)

# --- Initialize Pygame ---
pygame.init()
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Flappy Bird (No Images)")
CLOCK = pygame.time.Clock()

# --- Game Variables ---
bird_y = SCREEN_HEIGHT / 2
bird_velocity = 0
score = 0
game_state = 'start' # 'start', 'playing', 'game_over'

pipes = [] # List to store pipe objects

# --- Helper Functions / Classes ---

class Bird:
    def __init__(self):
        # We'll draw a rectangle for the bird
        self.rect = pygame.Rect(BIRD_X, SCREEN_HEIGHT / 2 - BIRD_SIZE / 2, BIRD_SIZE, BIRD_SIZE)
        self.velocity = 0
        self.gravity = GRAVITY
        self.jump_strength = JUMP_STRENGTH

    def jump(self):
        self.velocity = self.jump_strength

    def update(self):
        self.velocity += self.gravity
        self.rect.y += self.velocity
        # Basic boundary check for bird (can be improved for game over)
        if self.rect.top < 0:
            self.rect.top = 0
            self.velocity = 0
        if self.rect.bottom > SCREEN_HEIGHT: # Hitting ground
            self.rect.bottom = SCREEN_HEIGHT
            self.velocity = 0 # In a real game, this would be a game over condition


    def draw(self, screen):
        pygame.draw.rect(screen, BIRD_YELLOW, self.rect) # Draw yellow rectangle for bird

class Pipe:
    def __init__(self, x):
        self.x = x
        self.gap_y = random.randint(150, SCREEN_HEIGHT - 150 - PIPE_GAP) # Y-coord of the gap's top
        # Top pipe rect: from top of screen to gap_y
        self.top_rect = pygame.Rect(self.x, 0, PIPE_WIDTH, self.gap_y)
        # Bottom pipe rect: from gap_y + PIPE_GAP to bottom of screen
        self.bottom_rect = pygame.Rect(self.x, self.gap_y + PIPE_GAP, PIPE_WIDTH, SCREEN_HEIGHT - (self.gap_y + PIPE_GAP))
        self.passed = False # To track if the bird has passed this pipe for scoring

    def move(self):
        self.x -= PIPE_SPEED
        self.top_rect.x = self.x
        self.bottom_rect.x = self.x

    def draw(self, screen):
        pygame.draw.rect(screen, PIPE_GREEN, self.top_rect) # Draw green rectangle for top pipe
        pygame.draw.rect(screen, PIPE_GREEN, self.bottom_rect) # Draw green rectangle for bottom pipe

    def check_collision(self, bird_rect):
        return bird_rect.colliderect(self.top_rect) or bird_rect.colliderect(self.bottom_rect)

    def is_offscreen(self):
        return self.x + PIPE_WIDTH < 0

def draw_text(text, font, color, surface, x, y):
    textobj = font.render(text, True, color)
    textrect = textobj.get_rect(center=(x, y))
    surface.blit(textobj, textrect)

# --- Game Objects ---
bird = Bird()
game_font = pygame.font.Font(None, 40) # Default font, size 40

# --- Game Loop ---
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if game_state == 'start':
                    game_state = 'playing'
                    bird = Bird() # Reset bird position
                    pipes = [] # Clear pipes
                    score = 0
                elif game_state == 'playing':
                    bird.jump()
                elif game_state == 'game_over':
                    game_state = 'start' # Allow restarting by pressing space

    # --- Game Logic ---
    if game_state == 'playing':
        bird.update()

        # Generate pipes
        if not pipes or pipes[-1].x < SCREEN_WIDTH - 200: # Generate new pipe if last one is far enough
            pipes.append(Pipe(SCREEN_WIDTH))

        # Move and remove pipes
        for pipe in pipes:
            pipe.move()
            if pipe.is_offscreen():
                pipes.remove(pipe)

            # Collision detection
            if pipe.check_collision(bird.rect):
                game_state = 'game_over'

            # Scoring
            if bird.rect.left > pipe.top_rect.right and not pipe.passed:
                score += 1
                pipe.passed = True

        # Check for bird hitting ground (game over)
        if bird.rect.bottom >= SCREEN_HEIGHT:
            game_state = 'game_over'


    # --- Drawing ---
    SCREEN.fill(SKY_BLUE) # Fill background with a color

    for pipe in pipes:
        pipe.draw(SCREEN)

    bird.draw(SCREEN)

    # Draw the ground (optional, but good for visual consistency)
    pygame.draw.rect(SCREEN, GROUND_BROWN, (0, SCREEN_HEIGHT - 20, SCREEN_WIDTH, 20))


    draw_text(f"Score: {score}", game_font, WHITE, SCREEN, SCREEN_WIDTH // 2, 50)

    if game_state == 'start':
        draw_text("Press SPACE to Start", game_font, WHITE, SCREEN, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
    elif game_state == 'game_over':
        draw_text("Game Over!", game_font, WHITE, SCREEN, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 20)
        draw_text(f"Final Score: {score}", game_font, WHITE, SCREEN, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 20)
        draw_text("Press SPACE to Restart", game_font, WHITE, SCREEN, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 60)


    pygame.display.flip()
    CLOCK.tick(FPS)

pygame.quit()