import pygame
import random
import os
import json
import sys

# --- ЖЕСТКАЯ ФИКСАЦИЯ РАБОЧЕЙ ДИРЕКТОРИИ ---
# Находим путь к папке, где лежит этот файл main.py
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# Принудительно заставляем Python работать внутри этой папки
os.chdir(BASE_DIR)

# Теперь все пути будут строиться строго внутри BASE_DIR
ASSETS_DIR = os.path.join(BASE_DIR, "assets")
LEADERBOARD_FILE = os.path.join(BASE_DIR, "leaderboard.json")
SETTINGS_FILE = os.path.join(BASE_DIR, "settings.json")

# --- ИНИЦИАЛИЗАЦИЯ PYGAME ---
pygame.init()
WIDTH, HEIGHT = 400, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Racer Pro: TSIS3 Fixed Paths")

clock = pygame.time.Clock()
FPS = 60

# Цвета и шрифты
RED, GREEN, BLUE = (255, 0, 0), (0, 255, 0), (0, 0, 255)
BLACK, WHITE, GRAY = (0, 0, 0), (255, 255, 255), (150, 150, 150)
font = pygame.font.SysFont("Verdana", 20)
big_font = pygame.font.SysFont("Verdana", 40)

# --- РАБОТА С ДАННЫМИ ---
def load_json(path, default):
    if not os.path.exists(path):
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(default, f, indent=4)
        return default
    with open(path, 'r', encoding='utf-8') as f:
        try:
            return json.load(f)
        except:
            return default

def save_json(path, data):
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

# Загружаем настройки (Сложность)
game_settings = load_json(SETTINGS_FILE, {"difficulty": "Medium"})

# --- ЗАГРУЗКА РЕСУРСОВ ---
def get_asset(name, size, rot=0):
    path = os.path.join(ASSETS_DIR, name)
    try:
        img = pygame.image.load(path).convert_alpha()
        if rot: img = pygame.transform.rotate(img, rot)
        return pygame.transform.scale(img, size)
    except:
        # Если картинки нет, создаем цветной прямоугольник
        s = pygame.Surface(size)
        s.fill((random.randint(50, 200), 0, 0))
        return s

road_img = get_asset("road1.png", (WIDTH, HEIGHT))
player_img = get_asset("main.jpg", (60, 80), 90)
enemy_img = get_asset("main.jpg", (80, 60), 270)
oil_img = get_asset("oil.png", (40, 40))
wall_img = get_asset("wall.png", (80, 40))
nitro_img = get_asset("nitro.png", (30, 40))
shield_img = get_asset("shield.png", (40, 40))
repair_img = get_asset("repair.png", (40, 40))

# --- ИНТЕРФЕЙСНЫЕ КЛАССЫ ---
class Button:
    def __init__(self, text, x, y, w, h, color):
        self.rect = pygame.Rect(x, y, w, h)
        self.text, self.color = text, color
    def draw(self, surf):
        pygame.draw.rect(surf, self.color, self.rect, border_radius=10)
        t = font.render(self.text, True, WHITE)
        surf.blit(t, (self.rect.centerx - t.get_width()//2, self.rect.centery - t.get_height()//2))
    def clicked(self, pos): return self.rect.collidepoint(pos)

def draw_text(text, x, y, color=BLACK, is_big=False):
    img = (big_font if is_big else font).render(str(text), True, color)
    screen.blit(img, (x, y))

# --- ЭКРАНЫ ---
def show_leaderboard():
    scores = load_json(LEADERBOARD_FILE, [])
    # Сортировка по очкам
    scores = sorted(scores, key=lambda x: x.get('score', 0), reverse=True)[:10]
    while True:
        screen.fill(WHITE)
        draw_text("TOP 10 SCORES", 80, 50, BLACK, True)
        for i, s in enumerate(scores):
            txt = f"{i+1}. {s['name']} - {s['score']} ({s['dist']}m)"
            draw_text(txt, 60, 130 + i*30)
        btn_back = Button("BACK", 125, 500, 150, 40, GRAY)
        btn_back.draw(screen)
        pygame.display.flip()
        for e in pygame.event.get():
            if e.type == pygame.QUIT: pygame.quit(); sys.exit()
            if e.type == pygame.MOUSEBUTTONDOWN and btn_back.clicked(e.pos): return

def input_name():
    name = ""
    while True:
        screen.fill((210, 210, 210))
        draw_text("Enter Your Name:", 100, 200)
        draw_text(name + "|", 120, 250, BLUE)
        draw_text("Press ENTER to Start", 90, 350, GRAY)
        pygame.display.flip()
        for e in pygame.event.get():
            if e.type == pygame.QUIT: pygame.quit(); sys.exit()
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_RETURN and name.strip(): return name
                elif e.key == pygame.K_BACKSPACE: name = name[:-1]
                else: 
                    if len(name) < 10 and e.unicode.isalnum(): name += e.unicode

# --- ИГРОВОЙ ПРОЦЕСС ---
def game_loop(user_name):
    # Установка начальной скорости в зависимости от настроек
    base_spd = {"Easy": 3.0, "Medium": 4.5, "Hard": 6.0}.get(game_settings["difficulty"], 4.5)
    speed, score, dist = base_spd, 0, 0
    
    player = player_img.get_rect(center=(200, 500))
    enemy = enemy_img.get_rect(center=(random.randint(50, 350), -100))
    
    obstacles, boosts = [], []
    has_shield = False
    nitro_end, stun_end = 0, 0
    road_y1, road_y2 = 0, -HEIGHT

    running = True
    while running:
        now = pygame.time.get_ticks()
        
        # Эффекты скорости
        cur_speed = speed
        if nitro_end > now: cur_speed *= 1.6
        if stun_end > now: cur_speed = 0 # Оглушение
        
        dist += cur_speed / 10
        
        for e in pygame.event.get():
            if e.type == pygame.QUIT: pygame.quit(); sys.exit()

        # Управление (не работает во время оглушения)
        keys = pygame.key.get_pressed()
        if stun_end < now:
            if keys[pygame.K_LEFT] and player.left > 0: player.x -= 6
            if keys[pygame.K_RIGHT] and player.right < WIDTH: player.x += 6

        # Логика спавна (учитывает счет для сложности)
        spawn_chance = max(25, 120 - (score // 10)) 
        if random.randint(1, spawn_chance) == 1:
            x = random.randint(50, 350)
            if abs(x - player.centerx) > 85: # Safe Spawn Logic
                t = random.choice(['oil', 'wall', 'nitro', 'shield', 'repair'])
                rect = (oil_img if t=='oil' else wall_img).get_rect(center=(x, -100))
                if t in ['oil', 'wall']: obstacles.append({'type': t, 'rect': rect})
                else: boosts.append({'type': t, 'rect': rect})

        # Вражеский трафик
        enemy.y += cur_speed + 1.5
        if enemy.y > HEIGHT:
            enemy.y, enemy.x = -100, random.randint(50, 350)
            score += 10 # Очки за обгон

        if player.colliderect(enemy):
            if has_shield: has_shield = False; enemy.y = -200
            else: running = False

        # Обработка объектов
        for o in obstacles[:]:
            o['rect'].y += cur_speed
            if player.colliderect(o['rect']):
                if o['type'] == 'wall': stun_end = now + 1500
                obstacles.remove(o)
            elif o['rect'].y > HEIGHT: obstacles.remove(o)

        for b in boosts[:]:
            b['rect'].y += cur_speed
            if player.colliderect(b['rect']):
                if b['type'] == 'nitro': nitro_end = now + 3000
                elif b['type'] == 'shield': has_shield = True
                elif b['type'] == 'repair': obstacles = [o for o in obstacles if o['type'] != 'wall']
                boosts.remove(b)
            elif b['rect'].y > HEIGHT: boosts.remove(b)

        # Рисование дороги
        road_y1 += cur_speed; road_y2 += cur_speed
        if road_y1 >= HEIGHT: road_y1 = -HEIGHT
        if road_y2 >= HEIGHT: road_y2 = -HEIGHT
        screen.blit(road_img, (0, road_y1)); screen.blit(road_img, (0, road_y2))
        
        for o in obstacles: screen.blit(oil_img if o['type']=='oil' else wall_img, o['rect'])
        for b in boosts:
            img = {"nitro": nitro_img, "shield": shield_img, "repair": repair_img}[b['type']]
            screen.blit(img, b['rect'])
        
        screen.blit(player_img, player)
        if has_shield: pygame.draw.ellipse(screen, BLUE, player.inflate(15,15), 3)
        screen.blit(enemy_img, enemy)

        # Панель статуса
        pygame.draw.rect(screen, WHITE, (0, 0, WIDTH, 45))
        draw_text(f"Score: {score} | Dist: {int(dist)}m", 10, 10)
        if stun_end > now: draw_text("STUNNED!", 150, 50, RED, True)
        
        pygame.display.flip()
        clock.tick(FPS)

    # Сохранение в лидерборд после выхода из цикла (Game Over)
    lb = load_json(LEADERBOARD_FILE, [])
    lb.append({"name": user_name, "score": score, "dist": int(dist)})
    save_json(LEADERBOARD_FILE, lb)

def main_menu():
    # Имя спрашиваем только один раз при запуске
    name = input_name()
    while True:
        screen.fill((240, 240, 240))
        draw_text(f"Driver: {name}", 20, 20, BLUE)
        
        b_play = Button("START GAME", 100, 150, 200, 50, GREEN)
        b_lead = Button("LEADERBOARD", 100, 230, 200, 50, BLUE)
        b_quit = Button("QUIT", 100, 310, 200, 50, RED)
        
        for b in [b_play, b_lead, b_quit]: b.draw(screen)
        pygame.display.flip()
        
        for e in pygame.event.get():
            if e.type == pygame.QUIT: pygame.quit(); sys.exit()
            if e.type == pygame.MOUSEBUTTONDOWN:
                if b_play.clicked(e.pos): game_loop(name)
                if b_lead.clicked(e.pos): show_leaderboard()
                if b_quit.clicked(e.pos): pygame.quit(); sys.exit()

if __name__ == "__main__":
    main_menu()