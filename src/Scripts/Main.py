import pygame
import sys

pygame.init()

FPS_CAP = 60
WIDTH = 800
HEIGHT = 800
SRC_DIRECTORY = "D:\\Software Development\\final project csa\\Final-Project\\src\\"
SPRITES_DIRECTORY = SRC_DIRECTORY + "Data\Sprites\\"

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("AI Chess")
white_pawn_image = pygame.transform.scale(pygame.image.load(SPRITES_DIRECTORY + "White\\pawn.png"), (100,100))
black_pawn_image = pygame.transform.scale(pygame.image.load(SPRITES_DIRECTORY + "Black\\pawn.png"), (100,100))
chessboard_image = pygame.transform.scale(pygame.image.load(SPRITES_DIRECTORY + "board.png"), (WIDTH,HEIGHT))


WHITE = (255, 255, 255)
BLUE = (50, 100, 255)

clock = pygame.time.Clock()

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill(WHITE)

    screen.blit(chessboard_image, (0,0))
    screen.blit(white_pawn_image, (50,50))
    screen.blit(black_pawn_image, (150,50))
    #pygame.draw.rect(screen, BLUE, (300, 250, 200, 100))
    
    pygame.display.flip()

    clock.tick(FPS_CAP)

pygame.quit()
sys.exit()