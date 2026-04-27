import pygame
import math

pygame.init()

screen = pygame.display.set_mode((640, 480))
pygame.display.set_caption("Paint App - Shapes Extension")

clock = pygame.time.Clock()

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
GRAY = (200, 200, 200)

screen.fill(WHITE)

tool = "draw"
color = BLACK

drawing = False
start_pos = (0, 0)
last_pos = None

font = pygame.font.SysFont(None, 20)

# UI buttons (tools)
buttons = {
    "rect": pygame.Rect(10, 10, 90, 30),
    "square": pygame.Rect(110, 10, 90, 30),
    "circle": pygame.Rect(210, 10, 90, 30),
    "tri_right": pygame.Rect(310, 10, 110, 30),
    "tri_equil": pygame.Rect(430, 10, 110, 30),
    "rhombus": pygame.Rect(550, 10, 80, 30),
    "draw": pygame.Rect(10, 50, 90, 30),
    "eraser": pygame.Rect(110, 50, 90, 30),
}

# Color palette
colors = {
    "black": pygame.Rect(10, 90, 30, 30),
    "red": pygame.Rect(50, 90, 30, 30),
    "green": pygame.Rect(90, 90, 30, 30),
    "blue": pygame.Rect(130, 90, 30, 30),
}


def draw_ui():
    """Draw buttons and UI"""
    for name, rect in buttons.items():
        pygame.draw.rect(screen, GRAY, rect)
        text = font.render(name, True, BLACK)
        screen.blit(text, (rect.x + 5, rect.y + 7))

    pygame.draw.rect(screen, BLACK, colors["black"])
    pygame.draw.rect(screen, RED, colors["red"])
    pygame.draw.rect(screen, GREEN, colors["green"])
    pygame.draw.rect(screen, BLUE, colors["blue"])


running = True

while running:
    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

        # Mouse press
        if event.type == pygame.MOUSEBUTTONDOWN:
            mx, my = event.pos

            # tool selection
            for name, rect in buttons.items():
                if rect.collidepoint(mx, my):
                    tool = name

            # color selection
            if colors["black"].collidepoint(mx, my):
                color = BLACK
            elif colors["red"].collidepoint(mx, my):
                color = RED
            elif colors["green"].collidepoint(mx, my):
                color = GREEN
            elif colors["blue"].collidepoint(mx, my):
                color = BLUE

            # start drawing only in canvas area
            if my > 130:
                drawing = True
                start_pos = event.pos
                last_pos = event.pos

        # Mouse release → finalize shapes
        if event.type == pygame.MOUSEBUTTONUP:
            if drawing:
                drawing = False
                end_pos = event.pos
                last_pos = None

                x1, y1 = start_pos
                x2, y2 = end_pos

                # RECTANGLE
                if tool == "rect":
                    pygame.draw.rect(
                        screen,
                        color,
                        pygame.Rect(min(x1, x2), min(y1, y2),
                                    abs(x1 - x2), abs(y1 - y2)),
                        2
                    )

                # SQUARE (force equal sides)
                elif tool == "square":
                    side = min(abs(x2 - x1), abs(y2 - y1))
                    pygame.draw.rect(
                        screen,
                        color,
                        pygame.Rect(x1, y1, side, side),
                        2
                    )

                # CIRCLE
                elif tool == "circle":
                    radius = int(math.hypot(x2 - x1, y2 - y1))
                    pygame.draw.circle(screen, color, start_pos, radius, 2)

                # RIGHT TRIANGLE
                elif tool == "tri_right":
                    points = [(x1, y1), (x1, y2), (x2, y2)]
                    pygame.draw.polygon(screen, color, points, 2)

                # EQUILATERAL TRIANGLE
                elif tool == "tri_equil":
                    base_mid_x = (x1 + x2) // 2
                    height = int(abs(x2 - x1) * math.sqrt(3) / 2)

                    points = [
                        (x1, y2),
                        (x2, y2),
                        (base_mid_x, y2 - height)
                    ]
                    pygame.draw.polygon(screen, color, points, 2)

                # RHOMBUS (diamond shape)
                elif tool == "rhombus":
                    cx = (x1 + x2) // 2
                    cy = (y1 + y2) // 2

                    dx = abs(x2 - x1) // 2
                    dy = abs(y2 - y1) // 2

                    points = [
                        (cx, cy - dy),
                        (cx + dx, cy),
                        (cx, cy + dy),
                        (cx - dx, cy)
                    ]
                    pygame.draw.polygon(screen, color, points, 2)

        # Free drawing / eraser
        if event.type == pygame.MOUSEMOTION:
            if drawing and tool == "draw":
                if last_pos:
                    pygame.draw.line(screen, color, last_pos, event.pos, 3)
                last_pos = event.pos

            elif drawing and tool == "eraser":
                if last_pos:
                    pygame.draw.line(screen, WHITE, last_pos, event.pos, 12)
                last_pos = event.pos

    draw_ui()
    pygame.display.flip()
    clock.tick(60)

pygame.quit()