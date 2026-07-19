import pygame

pygame.init()
print(pygame version, pygame.__version__)

screen = pygame.display.set_mode((640, 480))
pygame.display.set_caption(pygame-ce test window)

running = True
while running
    for event in pygame.event.get()
        if event.type == pygame.QUIT
            running = False

    screen.fill((30, 30, 30))
    pygame.display.flip()

pygame.quit()