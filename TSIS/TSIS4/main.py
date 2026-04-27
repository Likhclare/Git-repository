import pygame
import json
import config as cfg
from db import Database
from game import GameLogic

class SnakeApp:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((cfg.WIDTH, cfg.HEIGHT))
        self.clock = pygame.time.Clock()
        self.db = Database()
        self.font = pygame.font.SysFont("Arial", 24)
        
        # Загрузка настроек
        try:
            with open("settings.json", "r") as f: self.settings = json.load(f)
        except:
            self.settings = {"snake_color": cfg.GREEN, "grid": True}
            
        self.game = GameLogic(self.settings)
        self.state = "MENU"
        self.username = ""

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT: return
                if self.state == "MENU":
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_RETURN and self.username: self.state = "PLAYING"
                        elif event.key == pygame.K_BACKSPACE: self.username = self.username[:-1]
                        else: self.username += event.unicode
                elif self.state == "PLAYING":
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_UP and self.game.direction != (0, cfg.CELL): self.game.direction = (0, -cfg.CELL)
                        if event.key == pygame.K_DOWN and self.game.direction != (0, -cfg.CELL): self.game.direction = (0, cfg.CELL)
                        if event.key == pygame.K_LEFT and self.game.direction != (cfg.CELL, 0): self.game.direction = (-cfg.CELL, 0)
                        if event.key == pygame.K_RIGHT and self.game.direction != (-cfg.CELL, 0): self.game.direction = (cfg.CELL, 0)

            self.screen.fill(cfg.BLACK)
            
            if self.state == "MENU":
                txt = self.font.render(f"Введите имя и Enter: {self.username}", True, cfg.WHITE)
                self.screen.blit(txt, (50, 250))
            
            elif self.state == "PLAYING":
                if self.game.update() == "GAME_OVER":
                    self.db.save_result(self.username, self.game.score, self.game.level)
                    self.state = "MENU"
                    self.game.reset()
                self.game.draw(self.screen)
                
            pygame.display.flip()
            self.clock.tick(self.game.speed)

if __name__ == "__main__":
    SnakeApp().run()