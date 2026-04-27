import pygame

class Button:
    def __init__(self, text, x, y, w, h, color, font):
        self.rect = pygame.Rect(x, y, w, h)
        self.text = text
        self.color = color
        self.font = font

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect, border_radius=5)
        txt = self.font.render(self.text, True, (255, 255, 255))
        screen.blit(txt, (self.rect.centerx - txt.get_width()//2, self.rect.centery - txt.get_height()//2))

    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)

def get_user_name(screen, font):
    name = ""
    input_active = True
    while input_active:
        screen.fill((200, 200, 200))
        prompt = font.render("Enter Name and Press ENTER:", True, (0, 0, 0))
        name_txt = font.render(name, True, (0, 0, 255))
        screen.blit(prompt, (50, 200))
        screen.blit(name_txt, (50, 250))
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN and name != "":
                    input_active = False
                elif event.key == pygame.K_BACKSPACE:
                    name = name[:-1]
                else:
                    if len(name) < 10:
                        name += event.unicode
            if event.type == pygame.QUIT:
                pygame.quit(); exit()
    return name