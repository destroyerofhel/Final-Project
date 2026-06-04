import pygame
pygame.font.init()
FPS_CAP = 60
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 800
BOARD_ROWS = 8
BOARD_COLUMNS = 8
SRC_DIRECTORY = "src\\"
SPRITES_DIRECTORY = SRC_DIRECTORY + "Data\\Sprites\\"
GAME_WIDTH = 800
GAME_HEIGHT = 800
UI_FONT = pygame.font.SysFont("Arial", 18)
TURN_UI_FONT = pygame.font.SysFont("Arial", 30)
GEMINI_MODEL = "gemini-2.5-flash-lite"
SYSTEM_PROMPT = "You are a chess engine playing Black. Input is a FEN string. Output only source_row source_col moved_row moved_col. 0 0=top-left 7 7=bottom-right. Example 1 0 3 0"
