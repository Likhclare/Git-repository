import pygame

RED = (255, 0, 0)

class Ball:
    def __init__(self, x, y, radius, step, width, height):
        self.x = x
        self.y = y
        self.radius = radius
        self.step = step
        self.width = width
        self.height = height

    def move(self, key):
        if key == pygame.K_LEFT:
            self.x = max(self.radius, self.x - self.step)

        if key == pygame.K_RIGHT:
            self.x = min(self.width - self.radius, self.x + self.step)

        if key == pygame.K_UP:
            self.y = max(self.radius, self.y - self.step)

        if key == pygame.K_DOWN:
            self.y = min(self.height - self.radius, self.y + self.step)

    def draw(self, screen):
        pygame.draw.circle(screen, RED, (self.x, self.y), self.radius)