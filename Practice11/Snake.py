import pygame
import random
import time

pygame.init()

# -------------------- НАСТРОЙКИ ЭКРАНА --------------------
WIDTH, HEIGHT = 600, 600
CELL = 20

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake - Weighted Food + Timer")

clock = pygame.time.Clock()

# -------------------- ЦВЕТА --------------------
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)

RED = (255, 0, 0)       # еда 1 очко
YELLOW = (255, 215, 0)  # еда 2 очка
BLUE = (0, 150, 255)    # еда 3 очка

# -------------------- ЗМЕЙКА --------------------
snake = [(100, 100), (80, 100), (60, 100)]
direction = (CELL, 0)

# -------------------- ВИДЫ ЕДЫ --------------------
food_types = [
    {"color": RED, "weight": 1},
    {"color": YELLOW, "weight": 2},
    {"color": BLUE, "weight": 3}
]

FOOD_LIFETIME = 5  # секунды жизни еды

# -------------------- ФУНКЦИЯ СОЗДАНИЯ ЕДЫ --------------------
def spawn_food():
    """Создаёт еду в случайной позиции и случайного типа"""
    while True:
        x = random.randrange(0, WIDTH, CELL)
        y = random.randrange(0, HEIGHT, CELL)

        if (x, y) not in snake:
            food_type = random.choice(food_types)

            return {
                "pos": (x, y),
                "color": food_type["color"],
                "weight": food_type["weight"],
                "spawn_time": time.time()
            }

# первая еда
food = spawn_food()

# -------------------- ИГРОВЫЕ ПЕРЕМЕННЫЕ --------------------
score = 0
level = 1
speed = 8

font = pygame.font.SysFont(None, 30)

running = True

# -------------------- ГЛАВНЫЙ ЦИКЛ --------------------
while running:
    screen.fill(BLACK)

    # -------------------- СОБЫТИЯ --------------------
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # управление змейкой
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                direction = (0, -CELL)
            elif event.key == pygame.K_DOWN:
                direction = (0, CELL)
            elif event.key == pygame.K_LEFT:
                direction = (-CELL, 0)
            elif event.key == pygame.K_RIGHT:
                direction = (CELL, 0)

    # -------------------- ДВИЖЕНИЕ ЗМЕЙКИ --------------------
    head = (
        snake[0][0] + direction[0],
        snake[0][1] + direction[1]
    )

    # столкновение со стеной
    if head[0] < 0 or head[0] >= WIDTH or head[1] < 0 or head[1] >= HEIGHT:
        running = False

    # столкновение с собой
    if head in snake:
        running = False

    snake.insert(0, head)

    # -------------------- ТАЙМЕР ЕДЫ --------------------
    if time.time() - food["spawn_time"] > FOOD_LIFETIME:
        food = spawn_food()

    # -------------------- СЪЕДЕНА ЛИ ЕДА --------------------
    if head == food["pos"]:
        score += food["weight"]  # добавляем очки по весу еды
        food = spawn_food()

        # повышение уровня
        if score % 5 == 0:
            level += 1
            speed += 1
    else:
        snake.pop()

    # -------------------- ОТРИСОВКА ЗМЕЙКИ --------------------
    for part in snake:
        pygame.draw.rect(screen, GREEN, (*part, CELL, CELL))

    # -------------------- ОТРИСОВКА ЕДЫ --------------------
    pygame.draw.rect(screen, food["color"], (*food["pos"], CELL, CELL))

    # -------------------- UI --------------------
    text = font.render(f"Score: {score}  Level: {level}", True, WHITE)
    screen.blit(text, (10, 10))

    pygame.display.flip()
    clock.tick(speed)

pygame.quit()