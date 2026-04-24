import pygame
import random

pygame.init()

WIDTH, HEIGHT = 600, 600
CELL = 20

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake")

clock = pygame.time.Clock()

# Colors
WHITE = (255,255,255)
GREEN = (0,255,0)
RED = (255,0,0)
BLACK = (0,0,0)

# Snake
snake = [(100,100), (80,100), (60,100)]
direction = (CELL, 0)

# Food
def spawn_food():
    """Generate food not on snake"""
    while True:
        x = random.randrange(0, WIDTH, CELL)
        y = random.randrange(0, HEIGHT, CELL)
        if (x,y) not in snake:
            return (x,y)

food = spawn_food()

# Game variables
score = 0
level = 1
speed = 8

font = pygame.font.SysFont(None, 30)

running = True
while running:
    screen.fill(BLACK)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Controls
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                direction = (0, -CELL)
            elif event.key == pygame.K_DOWN:
                direction = (0, CELL)
            elif event.key == pygame.K_LEFT:
                direction = (-CELL, 0)
            elif event.key == pygame.K_RIGHT:
                direction = (CELL, 0)

    # Move snake
    head = (snake[0][0] + direction[0], snake[0][1] + direction[1])

    # Wall collision
    if (head[0] < 0 or head[0] >= WIDTH or
        head[1] < 0 or head[1] >= HEIGHT):
        running = False

    # Self collision
    if head in snake:
        running = False

    snake.insert(0, head)

    # Eat food
    if head == food:
        score += 1
        food = spawn_food()

        # Level up every 3 points
        if score % 3 == 0:
            level += 1
            speed += 2
    else:
        snake.pop()

    # Draw snake
    for segment in snake:
        pygame.draw.rect(screen, GREEN, (*segment, CELL, CELL))

    # Draw food
    pygame.draw.rect(screen, RED, (*food, CELL, CELL))

    # UI
    text = font.render(f"Score: {score}  Level: {level}", True, WHITE)
    screen.blit(text, (10, 10))

    pygame.display.flip()
    clock.tick(speed)

pygame.quit()