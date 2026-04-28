import pygame
import math
from datetime import datetime
from tools import (draw_ui, flood_fill, draw_shape_preview, draw_final_shape)

pygame.init()

# Screen setup
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("TSIS 2: Paint - PERFECT Preview (No Ghosts)")
clock = pygame.time.Clock()

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
GRAY = (200, 200, 200)
LIGHT_GRAY = (230, 230, 230)
PREVIEW_COLOR = (128, 128, 255, 120)  # Semi-transparent preview

# Main canvas (persistent drawings)
canvas = pygame.Surface((800, 600))
canvas.fill(WHITE)

screen.blit(canvas, (0, 0))

# Tool states
tool = "pencil"
color = BLACK
brush_size = 2
drawing = False
start_pos = (0, 0)
current_pos = (0, 0)
text_mode = False
text_pos = None
text_input = ""
last_pos = None

# UI definitions (unchanged)
buttons = {
    "pencil": pygame.Rect(10, 10, 80, 30),
    "line": pygame.Rect(100, 10, 80, 30),
    "rect": pygame.Rect(190, 10, 80, 30),
    "circle": pygame.Rect(280, 10, 80, 30),
    "square": pygame.Rect(370, 10, 80, 30),
    "rtri": pygame.Rect(460, 10, 80, 30),
    "etri": pygame.Rect(550, 10, 80, 30),
    "rhombus": pygame.Rect(640, 10, 80, 30),
    "fill": pygame.Rect(10, 50, 80, 30),
    "eraser": pygame.Rect(100, 50, 80, 30),
    "text": pygame.Rect(190, 50, 80, 30),
}

colors_dict = {
    "black": pygame.Rect(10, 90, 30, 30),
    "red": pygame.Rect(50, 90, 30, 30),
    "green": pygame.Rect(90, 90, 30, 30),
    "blue": pygame.Rect(130, 90, 30, 30),
    "white": pygame.Rect(170, 90, 30, 30),
}

brush_sizes = {
    "small": pygame.Rect(10, 130, 60, 25),
    "medium": pygame.Rect(80, 130, 60, 25),
    "large": pygame.Rect(150, 130, 60, 25),
}

font = pygame.font.SysFont(None, 20)
text_font = pygame.font.SysFont(None, 24)

# Main loop
running = True

while running:
    mx, my = pygame.mouse.get_pos()
    
    # Always redraw: canvas -> screen (persistent layer 1)
    screen.blit(canvas, (0, 0))
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_1: brush_size = 2
            elif event.key == pygame.K_2: brush_size = 5
            elif event.key == pygame.K_3: brush_size = 10
            
            elif event.key == pygame.K_s and pygame.key.get_mods() & pygame.KMOD_CTRL:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                pygame.image.save(canvas, f"canvas_{timestamp}.png")
                print(f"Saved: canvas_{timestamp}.png")
            
            if text_mode:
                if event.key == pygame.K_RETURN:
                    if text_input:
                        text_surface = text_font.render(text_input, True, color)
                        canvas.blit(text_surface, text_pos)  # Save to canvas
                    text_mode = False
                    text_input = ""
                elif event.key == pygame.K_ESCAPE:
                    text_mode = False
                    text_input = ""
                else:
                    text_input += event.unicode
        
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if my < 160:  # UI
                for name, rect in buttons.items():
                    if rect.collidepoint(mx, my):
                        tool = name
                        text_mode = False
                
                color_map = {"black": BLACK, "red": RED, "green": GREEN, 
                           "blue": BLUE, "white": WHITE}
                for name, rect in colors_dict.items():
                    if rect.collidepoint(mx, my):
                        color = color_map[name]
                
                size_map = {"small": 2, "medium": 5, "large": 10}
                for name, rect in brush_sizes.items():
                    if rect.collidepoint(mx, my):
                        brush_size = size_map[name]
            else:
                if tool == "fill":
                    flood_fill(canvas, mx, my, color)
                elif tool == "text":
                    text_mode = True
                    text_pos = (mx, my)
                    text_input = ""
                else:
                    drawing = True
                    start_pos = (mx, my)
                    current_pos = (mx, my)
                    last_pos = (mx, my)
        
        elif event.type == pygame.MOUSEBUTTONUP:
            if drawing:
                if tool in ["pencil", "eraser"]:
                    drawing = False
                    last_pos = None
                else:
                    # 🎯 COMMIT TO CANVAS ONLY ON RELEASE
                    draw_final_shape(canvas, tool, start_pos, current_pos, color, brush_size)
                    drawing = False
        
        elif event.type == pygame.MOUSEMOTION:
            if drawing:
                current_pos = (mx, my)
                
                if tool == "pencil":
                    pygame.draw.line(canvas, color, last_pos, current_pos, brush_size)
                elif tool == "eraser":
                    pygame.draw.line(canvas, WHITE, last_pos, current_pos, brush_size)
                
                last_pos = current_pos
    
    # 🖌️ LAYER 2: Live preview (disappears when drawing=False)
    if drawing and tool not in ["pencil", "eraser", "fill", "text"]:
        preview_surf = pygame.Surface((800, 600), pygame.SRCALPHA)
        preview_surf.fill((0, 0, 0, 0))
        draw_shape_preview(preview_surf, tool, start_pos, current_pos, PREVIEW_COLOR, brush_size)
        screen.blit(preview_surf, (0, 0))
    
    # 🖌️ LAYER 3: Text preview (temporary)
    if text_mode and text_pos:
        preview = text_font.render(text_input, True, color)
        screen.blit(preview, text_pos)
    
    # 🖌️ LAYER 4: UI (always on top)
    draw_ui(screen, buttons, colors_dict, brush_sizes, tool, color, brush_size, text_mode, font)
    
    pygame.display.flip()
    clock.tick(60)

pygame.quit()