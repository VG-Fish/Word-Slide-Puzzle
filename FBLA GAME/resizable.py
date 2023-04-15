import pygame

pygame.init()
width, height = 640, 480
screen = pygame.display.set_mode((width, height), pygame.RESIZABLE)
image = pygame.Surface((120, 100), pygame.SRCALPHA)
image.fill(pygame.color.Color("royalblue"))
center_pos = (width // 2, height // 2)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
        elif event.type == pygame.VIDEORESIZE:
            width, height = event.dict["size"]
            # recreate screen object required for pygame version 1
            pygame.display.set_mode((width, height), pygame.RESIZABLE)
            # TODO: resize image if needed
            center_pos = (width // 2, height // 2)
    screen.fill(0)
    screen.blit(image, image.get_rect(center=center_pos))
    pygame.display.update()