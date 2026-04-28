import pygame
import sys
import random
import time
import json
import os
from db import Database

# --- Инициализация и константы ---
pygame.init()
WIDTH, HEIGHT = 800, 600
CELL = 20
SET_FILE = "settings.json"

# Цвета
BLACK = (20, 20, 20)
WHITE = (255, 255, 255)
RED = (213, 50, 80)
GREEN = (0, 255, 0)
BLUE = (50, 153, 213)
YELLOW = (255, 215, 0)
GRAY = (100, 100, 100)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Pro: TSIS4 Edition")
clock = pygame.time.Clock()

# --- Класс Кнопки ---
class Button:
    def __init__(self, x, y, w, h, text, color, hover_color):
        self.rect = pygame.Rect(x, y, w, h)
        self.text = text
        self.color = color
        self.hover_color = hover_color
        self.font = pygame.font.SysFont("Verdana", 20)

    def draw(self, surface):
        mouse_pos = pygame.mouse.get_pos()
        color = self.hover_color if self.rect.collidepoint(mouse_pos) else self.color
        pygame.draw.rect(surface, color, self.rect, border_radius=5)
        text_surf = self.font.render(self.text, True, WHITE)
        text_rect = text_surf.get_rect(center=self.rect.center)
        surface.blit(text_surf, text_rect)

    def is_clicked(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            return self.rect.collidepoint(event.pos)
        return False

# --- Основной класс игры ---
class SnakeGame:
    def __init__(self):
        self.db = Database()
        self.load_settings()
        self.font = pygame.font.SysFont("Verdana", 24)
        self.state = "MENU"
        self.username = "Alihan"
        self.reset_game_vars()

    def load_settings(self):
        if os.path.exists(SET_FILE):
            with open(SET_FILE, "r") as f:
                data = json.load(f)
                self.settings = {
                    "color": tuple(data.get("color", GREEN)),
                    "grid": data.get("grid", True),
                    "sound": data.get("sound", True)
                }
        else:
            self.settings = {"color": GREEN, "grid": True, "sound": True}

    def save_settings(self):
        with open(SET_FILE, "w") as f:
            json.dump({"color": list(self.settings["color"]), "grid": self.settings["grid"], "sound": self.settings["sound"]}, f)

    def reset_game_vars(self):
        self.snake = [(100, 100), (80, 100), (60, 100)]
        self.direction = (CELL, 0)
        self.score = 0
        self.level = 1
        self.speed = 8
        self.spawn_food()
        self.personal_best = self.db.get_personal_best(self.username)

    def spawn_food(self):
        while True:
            x = random.randrange(0, WIDTH, CELL)
            y = random.randrange(0, HEIGHT, CELL)
            if (x, y) not in self.snake:
                f_type = random.choice([{"c": RED, "w": 1}, {"c": YELLOW, "w": 2}, {"c": BLUE, "w": 3}])
                self.food = {"pos": (x, y), "color": f_type["c"], "weight": f_type["w"], "time": time.time()}
                break

    def draw_text(self, txt, col, x, y, center=False):
        surf = self.font.render(txt, True, col)
        rect = surf.get_rect(center=(x, y)) if center else surf.get_rect(topleft=(x, y))
        screen.blit(surf, rect)

    # --- ЭКРАНЫ ---
    def main_menu(self, events):
        self.draw_text("SNAKE PRO", GREEN, WIDTH//2, 100, True)
        buttons = [
            Button(300, 200, 200, 50, "PLAY", GREEN, (0, 200, 0)),
            Button(300, 270, 200, 50, "LEADERBOARD", BLUE, (0, 100, 200)),
            Button(300, 340, 200, 50, "SETTINGS", GRAY, (150, 150, 150)),
            Button(300, 410, 200, 50, "QUIT", RED, (150, 0, 0))
        ]
        for b in buttons:
            b.draw(screen)
            for e in events:
                if b.is_clicked(e):
                    if b.text == "PLAY": self.state = "PLAYING"; self.reset_game_vars()
                    if b.text == "LEADERBOARD": self.state = "LEADERBOARD"
                    if b.text == "SETTINGS": self.state = "SETTINGS"
                    if b.text == "QUIT": pygame.quit(); sys.exit()

    def settings_screen(self, events):
        self.draw_text("SETTINGS", WHITE, WIDTH//2, 80, True)
        b_grid = Button(300, 180, 200, 45, f"GRID: {'ON' if self.settings['grid'] else 'OFF'}", GRAY, WHITE)
        b_sound = Button(300, 240, 200, 45, f"SOUND: {'ON' if self.settings['sound'] else 'OFF'}", GRAY, WHITE)
        b_color = Button(300, 300, 200, 45, "SNAKE COLOR", self.settings["color"], WHITE)
        b_back = Button(300, 420, 200, 50, "SAVE & BACK", GREEN, (0, 200, 0))

        for b in [b_grid, b_sound, b_color, b_back]:
            b.draw(screen)
            for e in events:
                if b.is_clicked(e):
                    if "GRID" in b.text: self.settings["grid"] = not self.settings["grid"]
                    if "SOUND" in b.text: self.settings["sound"] = not self.settings["sound"]
                    if "COLOR" in b.text: self.settings["color"] = random.choice([GREEN, BLUE, YELLOW, WHITE])
                    if b.text == "SAVE & BACK": self.save_settings(); self.state = "MENU"

    def leaderboard_screen(self, events):
        self.draw_text("TOP 10 LEADERBOARD", YELLOW, WIDTH//2, 60, True)
        data = self.db.get_top_10()
        headers = ["Rank", "Username", "Score", "Lvl", "Date"]
        for i, h in enumerate(headers):
            self.draw_text(h, GRAY, 100 + i*135, 120)

        for i, row in enumerate(data):
            self.draw_text(str(i+1), WHITE, 100, 160 + i*35)
            self.draw_text(str(row[0]), WHITE, 235, 160 + i*35)
            self.draw_text(str(row[1]), GREEN, 370, 160 + i*35)

        b_back = Button(300, 520, 200, 45, "BACK", RED, WHITE)
        b_back.draw(screen)
        for e in events:
            if b_back.is_clicked(e): self.state = "MENU"

    def game_over_screen(self, events):
        self.draw_text("GAME OVER", RED, WIDTH//2, 100, True)
        self.draw_text(f"Score: {self.score}  Level: {self.level}", WHITE, WIDTH//2, 160, True)
        self.draw_text(f"Personal Best: {self.personal_best}", YELLOW, WIDTH//2, 200, True)

        b_retry = Button(300, 300, 200, 50, "RETRY", GREEN, WHITE)
        b_menu = Button(300, 370, 200, 50, "MAIN MENU", BLUE, WHITE)
        
        for b in [b_retry, b_menu]:
            b.draw(screen)
            for e in events:
                if b.is_clicked(e):
                    if b.text == "RETRY": self.state = "PLAYING"; self.reset_game_vars()
                    if b.text == "MAIN MENU": self.state = "MENU"

    def game_loop(self, events):
        # Отрисовка сетки
        if self.settings["grid"]:
            for x in range(0, WIDTH, CELL): pygame.draw.line(screen, (40,40,40), (x,0), (x,HEIGHT))
            for y in range(0, HEIGHT, CELL): pygame.draw.line(screen, (40,40,40), (0,y), (WIDTH,y))

        for e in events:
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_UP and self.direction != (0, CELL): self.direction = (0, -CELL)
                elif e.key == pygame.K_DOWN and self.direction != (0, -CELL): self.direction = (0, CELL)
                elif e.key == pygame.K_LEFT and self.direction != (CELL, 0): self.direction = (-CELL, 0)
                elif e.key == pygame.K_RIGHT and self.direction != (-CELL, 0): self.direction = (CELL, 0)

        # Движение
        head = (self.snake[0][0] + self.direction[0], self.snake[0][1] + self.direction[1])
        if (head[0] < 0 or head[0] >= WIDTH or head[1] < 0 or head[1] >= HEIGHT or head in self.snake):
            self.db.save_result(self.username, self.score, self.level)
            self.state = "GAME_OVER"; return

        self.snake.insert(0, head)
        if head == self.food["pos"]:
            self.score += self.food["weight"]
            if self.score % 5 == 0: self.level += 1; self.speed += 1
            self.spawn_food()
        else:
            if time.time() - self.food["time"] > 5: self.spawn_food()
            self.snake.pop()

        # Рисование
        pygame.draw.rect(screen, self.food["color"], (*self.food["pos"], CELL, CELL))
        for i, part in enumerate(self.snake):
            color = WHITE if i == 0 else self.settings["color"]
            pygame.draw.rect(screen, color, (*part, CELL-1, CELL-1))
        self.draw_text(f"Score: {self.score} Lvl: {self.level}", WHITE, 10, 10)

    def run(self):
        while True:
            screen.fill(BLACK)
            events = pygame.event.get()
            for e in events:
                if e.type == pygame.QUIT: pygame.quit(); sys.exit()

            if self.state == "MENU": self.main_menu(events)
            elif self.state == "SETTINGS": self.settings_screen(events)
            elif self.state == "LEADERBOARD": self.leaderboard_screen(events)
            elif self.state == "PLAYING": self.game_loop(events)
            elif self.state == "GAME_OVER": self.game_over_screen(events)

            pygame.display.flip()
            clock.tick(self.speed if self.state == "PLAYING" else 30)

if __name__ == "__main__":
    SnakeGame().run()