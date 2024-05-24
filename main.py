import pygame
import random

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
CELL_SIZE = 20
INITIAL_FPS = 10
FONT_SIZE = 35
GAME_OVER_FONT_SIZE = 48
DELAY_AFTER_GAME_OVER = 2000
COLOR_BLACK = (0, 0, 0)
COLOR_WHITE = (255, 255, 255)
COLOR_GREEN = (0, 255, 0)
COLOR_RED = (255, 0, 0)

# Initialize the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Snake Game")

clock = pygame.time.Clock()

class Snake:
    def __init__(self):
        self.head = [SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2]
        self.body = [self.head[:]]
        self.direction = 'RIGHT'
        self.change_to = self.direction
        self.grow_snake = False

    def update(self):
        # Update the direction of the snake
        self.direction = self.change_to

        # Move the snake in the current direction
        if self.direction == 'UP':
            self.head[1] -= CELL_SIZE
        elif self.direction == 'DOWN':
            self.head[1] += CELL_SIZE
        elif self.direction == 'LEFT':
            self.head[0] -= CELL_SIZE
        elif self.direction == 'RIGHT':
            self.head[0] += CELL_SIZE

        # Check if the snake hits the edges of the screen
        if not (0 <= self.head[0] < SCREEN_WIDTH and 0 <= self.head[1] < SCREEN_HEIGHT):
            return False

        # Insert new head position at the beginning of the body list
        self.body.insert(0, list(self.head))

        # Remove the last segment of the snake's body if not growing
        if not self.grow_snake:
            self.body.pop()
        else:
            self.grow_snake = False

        return True

    def grow(self):
        # Set the flag to grow the snake
        self.grow_snake = True

    def draw(self):
        for segment in self.body:
            pygame.draw.rect(screen, COLOR_GREEN, (segment[0], segment[1], CELL_SIZE, CELL_SIZE))

    def check_collision(self):
        # Check if the snake collides with itself
        if self.head in self.body[1:]:
            return True
        return False

class Food:
    def __init__(self):
        self.position = [random.randrange(0, SCREEN_WIDTH // CELL_SIZE) * CELL_SIZE,
                         random.randrange(0, SCREEN_HEIGHT // CELL_SIZE) * CELL_SIZE]

    def spawn(self):
        self.position = [random.randrange(0, SCREEN_WIDTH // CELL_SIZE) * CELL_SIZE,
                         random.randrange(0, SCREEN_HEIGHT // CELL_SIZE) * CELL_SIZE]

    def draw(self):
        pygame.draw.rect(screen, COLOR_RED, (self.position[0], self.position[1], CELL_SIZE, CELL_SIZE))

# Initialize snake, food, and score
snake = Snake()
food = Food()
score = 0

# Font for score
font = pygame.font.SysFont(None, FONT_SIZE)

def show_score():
    score_text = font.render("Score: " + str(score), True, COLOR_BLACK)
    screen.blit(score_text, [0, 0])

# Main game loop
running = True
FPS = INITIAL_FPS
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and snake.direction != 'DOWN':
                snake.change_to = 'UP'
            elif event.key == pygame.K_DOWN and snake.direction != 'UP':
                snake.change_to = 'DOWN'
            elif event.key == pygame.K_LEFT and snake.direction != 'RIGHT':
                snake.change_to = 'LEFT'
            elif event.key == pygame.K_RIGHT and snake.direction != 'LEFT':
                snake.change_to = 'RIGHT'

    # Update snake position
    if not snake.update():
        running = False

    # Check for collision with food
    if snake.head == food.position:
        snake.grow()  # Increase snake length
        food.spawn()  # Spawn new food
        # Increase the game speed (FPS) when snake eats food
        FPS += 1
        # Update score
        score += 1

    # Check for collision with itself
    if snake.check_collision():
        running = False

    # Fill the screen with white
    screen.fill(COLOR_WHITE)

    # Draw snake, food, and score
    snake.draw()
    food.draw()
    show_score()

    # Update the display
    pygame.display.flip()

    # Control the frame rate
    clock.tick(FPS)

# Game over display
font = pygame.font.SysFont(None, GAME_OVER_FONT_SIZE)
game_over_text = font.render("Game Over", True, COLOR_BLACK)
text_rect = game_over_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
screen.blit(game_over_text, text_rect)
pygame.display.flip()

# Delay before quitting
pygame.time.delay(DELAY_AFTER_GAME_OVER)

# Quit Pygame
pygame.quit()