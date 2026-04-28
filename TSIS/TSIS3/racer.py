import pygame
import random
import os
import json
import sys

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
os.chdir(BASE_DIR)

ASSETS_DIR = os.path.join(BASE_DIR, "assets")
LEADERBOARD_FILE = os.path.join(BASE_DIR, "leaderboard.json")
SETTINGS_FILE = os.path.join(BASE_DIR, "settings.json")

pygame.init()
WIDTH, HEIGHT = 400, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Racer Pro: TSIS3 Fixed Paths")

clock = pygame.time.Clock()
FPS = 60

RED, GREEN, BLUE = (255, 0, 0), (0, 255, 0), (0, 0, 255)
BLACK, WHITE, GRAY = (0, 0, 0), (255, 255, 255), (150, 150, 150)

font = pygame.font.SysFont("Verdana", 20)
big_font = pygame.font.SysFont("Verdana", 40)

def load_json(path, default):
    if not os.path.exists(path):
        with open(path, "w", encoding="utf-8") as f:
            json.dump(default, f, indent=4)
        return default

    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return default


def save_json(path, data):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)


game_settings = load_json(SETTINGS_FILE, {"difficulty": "Medium"})

def get_asset(name, size, rot=0):
    path = os.path.join(ASSETS_DIR, name)
    try:
        img = pygame.image.load(path).convert_alpha()
        if rot:
            img = pygame.transform.rotate(img, rot)
        return pygame.transform.scale(img, size)
    except:
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

class Button:
    def __init__(self, text, x, y, w, h, color):
        self.rect = pygame.Rect(x, y, w, h)
        self.text = text
        self.color = color

    def draw(self):
        pygame.draw.rect(screen, self.color, self.rect, border_radius=10)
        t = font.render(self.text, True, WHITE)
        screen.blit(
            t,
            (
                self.rect.centerx - t.get_width() // 2,
                self.rect.centery - t.get_height() // 2,
            ),
        )

    def clicked(self, pos):
        return self.rect.collidepoint(pos)


def draw_text(text, x, y, color=BLACK, big=False):
    f = big_font if big else font
    img = f.render(str(text), True, color)
    screen.blit(img, (x, y))

def show_leaderboard():
    while True:
        screen.fill(WHITE)
        data = load_json(LEADERBOARD_FILE, [])
        data = sorted(data, key=lambda x: x["score"], reverse=True)[:10]

        draw_text("TOP 10", 150, 50, BLACK, True)

        y = 130
        for i, d in enumerate(data):
            draw_text(f"{i+1}. {d['name']} {d['score']} ({d['dist']}m)", 80, y)
            y += 30

        back = Button("BACK", 125, 500, 150, 40, GRAY)
        back.draw()

        pygame.display.flip()

        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if e.type == pygame.MOUSEBUTTONDOWN:
                if back.clicked(e.pos):
                    return

def input_name():
    name = ""
    while True:
        screen.fill((220, 220, 220))
        draw_text("ENTER NAME:", 120, 200)
        draw_text(name + "|", 140, 260, BLUE)
        draw_text("ENTER to start", 120, 350, GRAY)

        pygame.display.flip()

        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_RETURN and name.strip():
                    return name
                elif e.key == pygame.K_BACKSPACE:
                    name = name[:-1]
                elif e.unicode.isalnum() and len(name) < 10:
                    name += e.unicode

def game_loop(name):
    base_speed = {"Easy": 3, "Medium": 4.5, "Hard": 6}.get(
        game_settings["difficulty"], 4.5
    )

    speed = base_speed
    score = 0
    dist = 0

    player = player_img.get_rect(center=(200, 500))
    enemy = enemy_img.get_rect(center=(200, -100))

    obstacles = []
    boosts = []

    nitro_end = 0
    stun_end = 0
    shield = False

    road_y1 = 0
    road_y2 = -HEIGHT

    running = True

    while running:
        now = pygame.time.get_ticks()

        # SPEED
        cur_speed = speed
        if nitro_end > now:
            cur_speed *= 1.6
        if stun_end > now:
            cur_speed = 0

        dist += cur_speed / 10

        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # CONTROL
        keys = pygame.key.get_pressed()
        if stun_end < now:
            if keys[pygame.K_LEFT]:
                player.x -= 5
            if keys[pygame.K_RIGHT]:
                player.x += 5

        # SPAWN
        if random.randint(1, 60) == 1:
            x = random.randint(50, 350)
            t = random.choice(["oil", "wall", "nitro", "shield", "repair"])

            if t in ["oil", "wall"]:
                rect = (oil_img if t == "oil" else wall_img).get_rect(center=(x, -50))
                obstacles.append({"type": t, "rect": rect})
            else:
                rect = nitro_img.get_rect(center=(x, -50))
                boosts.append({"type": t, "rect": rect})

        # ENEMY
        enemy.y += cur_speed + 1.5
        if enemy.y > HEIGHT:
            enemy.y = -100
            enemy.x = random.randint(50, 350)
            score += 10

        if player.colliderect(enemy):
            if shield:
                shield = False
                enemy.y = -200
            else:
                running = False

        # OBSTACLES
        for o in obstacles[:]:
            o["rect"].y += cur_speed

            if player.colliderect(o["rect"]):
                if o["type"] == "wall":
                    stun_end = now + 3000
                obstacles.remove(o)

            elif o["rect"].y > HEIGHT:
                obstacles.remove(o)

        # BOOSTS
        for b in boosts[:]:
            b["rect"].y += cur_speed

            if player.colliderect(b["rect"]):
                if b["type"] == "nitro":
                    nitro_end = now + 3000
                elif b["type"] == "shield":
                    shield = True
                elif b["type"] == "repair":
                    obstacles = [o for o in obstacles if o["type"] != "wall"]

                boosts.remove(b)

        # DRAW
        road_y1 += cur_speed
        road_y2 += cur_speed

        if road_y1 > HEIGHT:
            road_y1 = -HEIGHT
        if road_y2 > HEIGHT:
            road_y2 = -HEIGHT

        screen.blit(road_img, (0, road_y1))
        screen.blit(road_img, (0, road_y2))

        for o in obstacles:
            screen.blit(oil_img if o["type"] == "oil" else wall_img, o["rect"])

        for b in boosts:
            img = {"nitro": nitro_img, "shield": shield_img, "repair": repair_img}[b["type"]]
            screen.blit(img, b["rect"])

        screen.blit(player_img, player)
        screen.blit(enemy_img, enemy)

        draw_text(f"Score: {score}", 10, 10)
        draw_text(f"Dist: {int(dist)}", 10, 35)

        pygame.display.flip()
        clock.tick(FPS)

    # SAVE SCORE
    lb = load_json(LEADERBOARD_FILE, [])
    lb.append({"name": name, "score": score, "dist": int(dist)})
    save_json(LEADERBOARD_FILE, lb)

def menu():
    name = input_name()

    while True:
        screen.fill((240, 240, 240))

        draw_text(f"Player: {name}", 20, 20, BLUE)

        play = Button("PLAY", 100, 150, 200, 50, GREEN)
        lead = Button("LEADERBOARD", 100, 230, 200, 50, BLUE)
        quitb = Button("QUIT", 100, 310, 200, 50, RED)

        play.draw()
        lead.draw()
        quitb.draw()

        pygame.display.flip()

        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if e.type == pygame.MOUSEBUTTONDOWN:
                if play.clicked(e.pos):
                    game_loop(name)
                if lead.clicked(e.pos):
                    show_leaderboard()
                if quitb.clicked(e.pos):
                    pygame.quit()
                    sys.exit()


if __name__ == "__main__":
    menu()