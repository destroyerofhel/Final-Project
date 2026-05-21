import pygame
import sys
from typing import List
from enum import Enum
from pygame import Vector2

class ChessPiece(Enum):
        EMPTY = 0
        PAWN = 1
        BISHOP = 2
        KNIGHT = 3
        ROOK = 4
        QUEEN = 5
        KING = 6

pygame.init()

FPS_CAP = 60
WIDTH = 800
HEIGHT = 800
BOARD_ROWS = 8
BOARD_COLUMNS = 8

#SRC_DIRECTORY = "C:\\Users\\NathanielOlveira\\OneDrive - NYC Public Schools\\Documents\\AI chess game\\Final-Project-1\\src"
SRC_DIRECTORY = "/workspaces/Final-Project/src/"
SPRITES_DIRECTORY = SRC_DIRECTORY + "Data/Sprites/"

WHITE = (255, 255, 255)
BLUE = (50, 100, 255)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
pygame.display.set_caption("AI Chess")

chessboard_image = pygame.transform.scale(pygame.image.load(SPRITES_DIRECTORY + "board.png"), (WIDTH,HEIGHT))

#8 by 8 grid (white : 0-6, black : 7-13), 0 = empty, 1 = pawn, 2 = bishop, 3 = knight, 4 = rook, 5 = queen, 6 = king; refer to ChessPiece enum
board : List[List[int]] = [
    [4+7,3+7,2+7,5+7,6+7,2+7,3+7,4+7],
    [1+7,1+7,1+7,1+7,1+7,1+7,1+7,1+7],
    [0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0],
    [1,1,1,1,1,1,1,1],
    [4,3,2,6,5,2,3,4]
]
def convertBoardToObj():
    import Piece 
    isWhite = True
    for x,row in enumerate(board):
        for y in range(len(row)):
            if row[y] / 7 > 1:
                isWhite = False
            vector = Vector2(x, y)
            if row[y] % 7 == 1:
                board[x][y] = Piece.Pawn(vector, isWhite, row[y] % 7)
            elif row[y] % 7 == 2:
                board[x][y] = Piece.Bishop(vector, isWhite, row[y] % 7)
            elif row[y] % 7 == 3:
                board[x][y] = Piece.Knight(vector, isWhite, row[y] % 7)
            elif row[y] % 7 == 4:
                board[x][y] = Piece.Rook(vector, isWhite, row[y] % 7)
            elif row[y] % 7 == 5:
                board[x][y] = Piece.Queen(vector, isWhite, row[y] % 7)
            elif row[y] % 7 == 6:
                board[x][y] = Piece.King(vector, isWhite, row[y] % 7)

convertBoardToObj()
selected_row = -1
selected_column = -1
selected_piece : ChessPiece = None
selected_is_black : bool = False

def convertBoardToScreenCoordinates(row : int, column : int) -> tuple[int, int]: 
    return column*(HEIGHT/BOARD_ROWS), row*(WIDTH/BOARD_COLUMNS)

def drawChessPiece(piece : int, position : tuple[int, int]):
    chessPiece = ChessPiece(piece%7)
    if(chessPiece.name == "EMPTY"): return
    color = "White/"
    if(piece > 6): color = "Black/"
    loaded_image = pygame.transform.scale(pygame.image.load(SPRITES_DIRECTORY + color + chessPiece.name.lower() + ".png"), (WIDTH/BOARD_COLUMNS,HEIGHT/BOARD_ROWS))
    screen.blit(loaded_image, position)

def resetMouseSelection():
    global selected_row, selected_column, selected_piece, selected_is_black
    selected_row = -1
    selected_column = -1
    selected_piece = None
    selected_is_black = False

#TODO: make this function
def movePiece():
    pass

#makes it so the left click event doesn't run multiple times if you hold left mouse button down
mouse_debounce = False
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill(WHITE)

    #left mouse button pressed; get_pressed() returns a tuple[bool,bool,bool], first is left button pressed, second is middle button pressed, third is right button pressed
    if(pygame.mouse.get_pressed()[0] and not mouse_debounce):
        mouse_debounce = True
        mouse_x, mouse_y = pygame.mouse.get_pos()
        #print(mouse_x, mouse_y)
        mouse_row = int(mouse_y/(WIDTH/BOARD_ROWS))
        mouse_column = int(mouse_x/(WIDTH/BOARD_COLUMNS))
        mouse_piece = ChessPiece(board[mouse_row][mouse_column]%7)
        #print(mouse_row, mouse_column, board[mouse_row][mouse_column])
        if(selected_piece == None and board[mouse_row][mouse_column] != 0):
            selected_row = mouse_row
            selected_column = mouse_column
            selected_piece = mouse_piece
            selected_is_black = board[mouse_row][mouse_column] > 6
            print("Mouse selected a " + selected_piece.name.lower() + " at row " + str(selected_row) + ", column " + str(selected_column))
        elif(selected_piece == None and board[mouse_row][mouse_column] == 0):
            print("Mouse selected empty space")
        elif(selected_row == mouse_row and selected_column == mouse_column):
            print("Player stopped moving a " + selected_piece.name.lower())
            resetMouseSelection()
        elif(selected_piece != None and board[mouse_row][mouse_column] != 0):
            print("A " + selected_piece.name.lower() +" took over a " + mouse_piece.name.lower() + " at row " + str(mouse_row) + ", column" + str(mouse_column))
            board[mouse_row][mouse_column] = selected_piece.value + int(selected_is_black)*7
            board[selected_row][selected_column] = 0
            resetMouseSelection()
        else:
            print("Player moved a " + selected_piece.name.lower() + " to row " + str(mouse_row) + ", column " + str(mouse_column))
            board[mouse_row][mouse_column] = selected_piece.value + int(selected_is_black)*7
            board[selected_row][selected_column] = 0
            resetMouseSelection()
    elif(not pygame.mouse.get_pressed()[0]):
        mouse_debounce = False

    screen.blit(chessboard_image, (0,0))
    
    for row in range(0,8):
        for column in range(0,8):
            #drawChessPiece(board[row][column], convertBoardToScreenCoordinates(row, column))
            #run the convertboard to obj before ts loop so it not ints but objs
            if board[row][column] != 0:
                board[row][column].drawPiece(screen)
    
    pygame.display.flip()

    clock.tick(FPS_CAP)

pygame.quit()
sys.exit()