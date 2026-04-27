import pygame
from player import MusicPlayer

pygame.init()

# окно
screen = pygame.display.set_mode((600, 300))
pygame.display.set_caption("Music Player")

font = pygame.font.SysFont(None, 36)

player = MusicPlayer("music")

running = True

clock = pygame.time.Clock()

while running:
    screen.fill((30, 30, 30))

    # текст
    track_text = font.render(f"Track: {player.get_current_track_name()}", True, (255, 255, 255))
    controls_text = font.render("P=Play S=Stop N=Next B=Back Q=Quit", True, (200, 200, 200))

    screen.blit(track_text, (50, 100))
    screen.blit(controls_text, (50, 200))

    pygame.display.flip()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_p:
                player.play()

            elif event.key == pygame.K_s:
                player.stop()

            elif event.key == pygame.K_n:
                player.next_track()

            elif event.key == pygame.K_b:
                player.previous_track()

            elif event.key == pygame.K_q:
                running = False

    clock.tick(60)

pygame.quit()