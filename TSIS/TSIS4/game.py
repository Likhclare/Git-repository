import pygame
import random
import config as cfg

class GameLogic:
    def __init__(self, settings):
        self.settings = settings
        self.reset()

    def reset(self):
        self.snake = [(100, 100), (80, 100), (60, 100)]
        self.direction = (cfg.CELL, 0)
        self.score = 0
        self.level = 1
        self.speed = 8
        self.obstacles = []
        self.food = self.spawn_food()
        self.poison = self.spawn_item()
        self.shield = False

    def spawn_item(self):
        while True:
            pos = (random.randrange(0, cfg.WIDTH, cfg.CELL), random.randrange(0, cfg.HEIGHT, cfg.CELL))
            if pos not in self.snake and pos not in self.obstacles:
                return pos

    def spawn_food(self):
        types = [{"color": cfg.RED, "weight": 1}, {"color": cfg.YELLOW, "weight": 2}, {"color": cfg.BLUE, "weight": 3}]
        f = random.choice(types)
        return {"pos": self.spawn_item(), "color": f["color"], "weight": f["weight"]}

    def update(self):
        head = (self.snake[0][0] + self.direction[0], self.snake[0][1] + self.direction[1])
        
        if (head[0] < 0 or head[0] >= cfg.WIDTH or head[1] < 0 or head[1] >= cfg.HEIGHT or 
            head in self.snake or head in self.obstacles):
            return "GAME_OVER"

        self.snake.insert(0, head)

        if head == self.food["pos"]:
            self.score += self.food["weight"]
            self.food = self.spawn_food()
            if self.score // 5 >= self.level:
                self.level += 1
                self.speed += 1
                if self.level >= 3: self.obstacles.append(self.spawn_item())
        elif head == self.poison:
            if len(self.snake) <= 2: return "GAME_OVER"
            self.snake.pop(); self.snake.pop()
            self.poison = self.spawn_item()
        else:
            self.snake.pop()
        return "PLAYING"

    def draw(self, screen):
        for seg in self.snake:
            pygame.draw.rect(screen, self.settings["snake_color"], (*seg, cfg.CELL, cfg.CELL))
        for obs in self.obstacles:
            pygame.draw.rect(screen, cfg.GRAY, (*obs, cfg.CELL, cfg.CELL))
        pygame.draw.rect(screen, self.food["color"], (*self.food["pos"], cfg.CELL, cfg.CELL))
        pygame.draw.rect(screen, cfg.DARK_RED, (*self.poison, cfg.CELL, cfg.CELL))