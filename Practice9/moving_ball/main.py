import pygame
from ball import Ball

pygame.init()

WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))

WHITE = (255, 255, 255)

ball = Ball(WIDTH // 2, HEIGHT // 2, 25, 20, WIDTH, HEIGHT)

clock = pygame.time.Clock()

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            ball.move(event.key)

    screen.fill(WHITE)
    ball.draw(screen)
    pygame.display.flip()
    clock.tick(60)

pygame.quit()