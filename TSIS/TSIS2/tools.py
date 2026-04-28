import pygame
import math

def draw_shape_preview(surface, tool, start, end, color, brush_size):
    """Draw OUTLINE-ONLY shapes (no fill)"""
    if tool == "rect":
        rect = pygame.Rect(min(start[0], end[0]), min(start[1], end[1]),
                          abs(start[0] - end[0]), abs(start[1] - end[1]))
        pygame.draw.rect(surface, color, rect, brush_size)
    
    elif tool == "circle":
        radius = int(math.hypot(end[0] - start[0], end[1] - start[1]))
        pygame.draw.circle(surface, color, start, radius, brush_size)
    
    elif tool == "square":
        size = min(abs(end[0] - start[0]), abs(end[1] - start[1]))
        rect = pygame.Rect(start[0], start[1], size, size)
        pygame.draw.rect(surface, color, rect, brush_size)
    
    elif tool == "line":
        pygame.draw.line(surface, color, start, end, brush_size)
    
    elif tool == "rtri":
        points = [start, (start[0], end[1]), end]
        # ✅ OUTLINE ONLY - uses brush_size thickness
        pygame.draw.polygon(surface, color, points, brush_size)
    
    elif tool == "etri":
        side_length = math.hypot(end[0] - start[0], end[1] - start[1])
        height = side_length * math.sqrt(3) / 2
        p1 = start
        p2 = (start[0] + side_length, start[1])
        p3 = (start[0] + side_length/2, start[1] - height)
        points = [p1, p2, p3]
        # ✅ OUTLINE ONLY - uses brush_size thickness
        pygame.draw.polygon(surface, color, points, brush_size)
    
    elif tool == "rhombus":
        center_x = (start[0] + end[0]) // 2
        center_y = (start[1] + end[1]) // 2
        w_size, h_size = abs(end[0] - start[0]), abs(end[1] - start[1])
        points = [
            (center_x, center_y - h_size//2),
            (center_x + w_size//2, center_y),
            (center_x, center_y + h_size//2),
            (center_x - w_size//2, center_y)
        ]
        # ✅ OUTLINE ONLY - uses brush_size thickness
        pygame.draw.polygon(surface, color, points, brush_size)

def draw_final_shape(surface, tool, start, end, color, brush_size):
    """Final outline drawing"""
    draw_shape_preview(surface, tool, start, end, color, brush_size)

def draw_ui(screen, buttons, colors, brush_sizes, tool, color, brush_size, text_mode, font):
    """UI (unchanged)"""
    for name, rect in buttons.items():
        pygame.draw.rect(screen, (200, 200, 200), rect)
        pygame.draw.rect(screen, (0, 0, 0), rect, 2)
        text = font.render(name[:4].upper(), True, (0, 0, 0))
        screen.blit(text, (rect.x + 10, rect.y + 7))
    
    color_map = {"black": (0,0,0), "red": (255,0,0), "green": (0,255,0), 
                "blue": (0,0,255), "white": (255,255,255)}
    for name, rect in colors.items():
        pygame.draw.rect(screen, color_map[name], rect)
        pygame.draw.rect(screen, (0, 0, 0), rect, 2)
    
    sizes = [2, 5, 10]
    sizes_text = ["1px", "5px", "10px"]
    for i, (name, rect) in enumerate(brush_sizes.items()):
        pygame.draw.rect(screen, (230, 230, 230), rect)
        pygame.draw.rect(screen, (0, 0, 0), rect, 2)
        pygame.draw.circle(screen, (0, 0, 0), (rect.centerx, rect.centery), sizes[i]//2)
        text = font.render(sizes_text[i], True, (0, 0, 0))
        screen.blit(text, (rect.x + 5, rect.y + 5))
    
    status_rect = pygame.Rect(0, 570, 800, 30)
    pygame.draw.rect(screen, (230, 230, 230), status_rect)
    color_names = {(255,255,255):'WHITE', (0,0,0):'BLACK', (255,0,0):'RED',
                   (0,255,0):'GREEN', (0,0,255):'BLUE'}
    status_text = font.render(
        f"Tool: {tool} | Color: {color_names.get(color, 'CUSTOM')} | Size: {brush_size}px | "
        f"{'' if not text_mode else 'TEXT MODE'}", True, (0, 0, 0))
    screen.blit(status_text, (5, 575))

def flood_fill(canvas, x, y, fill_color):
    """Flood fill (unchanged)"""
    target_color = canvas.get_at((x, y))
    if target_color == fill_color: return
    stack = [(x, y)]
    width, height = canvas.get_size()
    while stack:
        cx, cy = stack.pop()
        if 0 <= cx < width and 0 <= cy < height and canvas.get_at((cx, cy)) == target_color:
            canvas.set_at((cx, cy), fill_color)
            stack.extend([(cx-1, cy), (cx+1, cy), (cx, cy-1), (cx, cy+1)])