import pygame
import sys
import random
import os

# Инициализация pygame
pygame.init()

# Размеры окна
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Racing Game")

clock = pygame.time.Clock()
FPS = 60

# Цвета
RED = (255, 0, 0)
YELLOW = (255, 215, 0)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Пути к ресурсам
BASE_DIR = os.path.dirname(__file__)
RES_DIR = os.path.join(BASE_DIR, "resources")

# Загрузка изображений
player_img = pygame.image.load(os.path.join(RES_DIR, "main.jpg")).convert_alpha()
player_img = pygame.transform.rotate(player_img, 90)
player_img = pygame.transform.scale(player_img, (60, 80))

enemy_img = pygame.image.load(os.path.join(RES_DIR, "main.jpg")).convert_alpha()
enemy_img = pygame.transform.scale(enemy_img, (80, 60))
enemy_img = pygame.transform.rotate(enemy_img, 270)

road_img = pygame.image.load(os.path.join(RES_DIR, "road1.png")).convert()
road_img = pygame.transform.scale(road_img, (SCREEN_WIDTH, SCREEN_HEIGHT))

# Игрок
player = player_img.get_rect()
player.x = 170
player.y = 500

# Враг (появляется сверху)
enemy = enemy_img.get_rect()
enemy.x = random.randint(40, 350)
enemy.y = -100

# ---------- МОНЕТЫ С ВЕСОМ ----------
coins = []
for i in range(5):
    coin = {
        "rect": pygame.Rect(random.randint(40, 350), random.randint(-600, 0), 20, 20),
        "value": random.choice([1, 2, 5])  # вес монеты
    }
    coins.append(coin)

# Движение дороги
road_y1 = 0
road_y2 = -SCREEN_HEIGHT

# Скорости
speed = 5            # скорость дороги
enemy_speed = speed + 3  # враг быстрее дороги

# Счёт
score = 0
coins_collected = 0
N = 10  # каждые N монет враг ускоряется

font = pygame.font.SysFont("Verdana", 20)
game_over = False

# Таймер увеличения скорости дороги
INC_SPEED = pygame.USEREVENT + 1
pygame.time.set_timer(INC_SPEED, 2000)

# Функция вывода текста
def draw_text(text, x, y, color=BLACK):
    img = font.render(text, True, color)
    screen.blit(img, (x, y))


# Главный цикл
while True:
    clock.tick(FPS)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        # Постепенно ускоряем дорогу
        if event.type == INC_SPEED:
            speed += 0.5

    if not game_over:

        # Движение дороги вниз
        road_y1 += speed
        road_y2 += speed

        if road_y1 >= SCREEN_HEIGHT:
            road_y1 = -SCREEN_HEIGHT
        if road_y2 >= SCREEN_HEIGHT:
            road_y2 = -SCREEN_HEIGHT

        # Управление игроком
        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT] and player.x > 0:
            player.x -= 5
        if keys[pygame.K_RIGHT] and player.x < SCREEN_WIDTH - player.width:
            player.x += 5
        if keys[pygame.K_UP] and player.y > 0:
            player.y -= 5
        if keys[pygame.K_DOWN] and player.y < SCREEN_HEIGHT - player.height:
            player.y += 5

        # 🔥 ВРАГ ДВИЖЕТСЯ ВНИЗ БЫСТРЕЕ ДОРОГИ
        enemy_speed = speed + 3
        enemy.y += enemy_speed

        # Если враг вышел вниз — появляется сверху
        if enemy.y > SCREEN_HEIGHT:
            enemy.y = -100
            enemy.x = random.randint(40, 350)

        # Проверка столкновения
        if player.colliderect(enemy):
            game_over = True

        # ---------- МОНЕТЫ ----------
        for coin in coins:
            coin["rect"].y += speed

            # Переспавн монеты
            if coin["rect"].y > SCREEN_HEIGHT:
                coin["rect"].y = random.randint(-600, 0)
                coin["rect"].x = random.randint(40, 350)
                coin["value"] = random.choice([1, 2, 5])

            # Сбор монеты
            if player.colliderect(coin["rect"]):
                score += coin["value"]
                coins_collected += 1

                # Увеличение скорости врага каждые N монет
                if coins_collected % N == 0:
                    enemy_speed += 1

                coin["rect"].y = random.randint(-600, 0)
                coin["rect"].x = random.randint(40, 350)
                coin["value"] = random.choice([1, 2, 5])

        # Отрисовка
        screen.blit(road_img, (0, road_y1))
        screen.blit(road_img, (0, road_y2))

        screen.blit(player_img, player)
        screen.blit(enemy_img, enemy)

        # Рисуем монеты (разные цвета = разные веса)
        for coin in coins:
            if coin["value"] == 1:
                color = YELLOW
            elif coin["value"] == 2:
                color = GREEN
            else:
                color = BLUE

            pygame.draw.circle(screen, color, coin["rect"].center, 10)

        # UI
        draw_text(f"Score: {score}", 10, 10)
        draw_text(f"Coins: {coins_collected}", 10, 35)
        draw_text(f"Speed: {speed:.1f}", 10, 60)

    else:
        draw_text("GAME OVER", 130, 250, RED)
        draw_text(f"Score: {score}", 150, 300)

    pygame.display.update()