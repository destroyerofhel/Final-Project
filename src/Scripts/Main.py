import pygame
import sys
from typing import List
from enum import Enum
from pygame import Vector2
import Piece 
import Game
import Config
import GeminiAgent
import time

class ChessPiece(Enum):
        EMPTY = 0
        PAWN = 1
        BISHOP = 2
        KNIGHT = 3
        ROOK = 4
        QUEEN = 5
        KING = 6

pygame.init()

FPS_CAP = Config.FPS_CAP
BOARD_ROWS = Config.BOARD_ROWS
BOARD_COLUMNS = Config.BOARD_COLUMNS
SCREEN_WIDTH = Config.SCREEN_WIDTH
SCREEN_HEIGHT = Config.SCREEN_HEIGHT
GAME_WIDTH = Config.GAME_WIDTH
GAME_HEIGHT = Config.GAME_HEIGHT

#SRC_DIRECTORY = "C:\\Users\\NathanielOlveira\\OneDrive - NYC Public Schools\\Documents\\AI chess game\\Final-Project-1\\src"
SRC_DIRECTORY = Config.SRC_DIRECTORY
SPRITES_DIRECTORY = Config.SPRITES_DIRECTORY

WHITE = (255, 255, 255)
BLUE = (50, 100, 255)

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()
pygame.display.set_caption("AI Chess")

selected_row = -1
selected_column = -1
selected_piece : ChessPiece = Piece.Empty((-1, -1), None)
selected_is_black : bool = False

chessboard_image = pygame.transform.scale(pygame.image.load(SPRITES_DIRECTORY + "board.png"), (GAME_WIDTH,GAME_HEIGHT))
title_screen_image = pygame.transform.scale(pygame.image.load(SPRITES_DIRECTORY + "title screen.png"), (SCREEN_WIDTH,SCREEN_HEIGHT))

previous_piece = Piece.Empty((-1, -1), None)

#makes it so the left click event doesn't run multiple times if you hold left mouse button down
mouse_debounce = False
whites_turn = True
running = True
row = -1
column = -1
in_check_white = False
in_check_black = False
ran_out = False
wait_a_frame = False
move_name = ""

#8 by 8 grid (white : 0-6, black : 7-13), 0 = empty, 1 = pawn, 2 = bishop, 3 = knight, 4 = rook, 5 = queen, 6 = king; refer to ChessPiece enum
board : List[List[int]] = [
    [4+7,3+7,2+7,5+7,6+7,2+7,3+7,4+7],
    [1+7,1+7,1+7,1+7,1+7,1+7,1+7,1+7],
    [0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0],
    [1,1,1,1,1,1,1,1],
    [4,3,2,5,6,2,3,4]
]


# ladder mate setup
# board = [
#     [0,0,0,6+7,0,0,0,0],
#     [0,0,0,0,0,0,0,0],
#     [5,0,0,0,0,0,0,0],
#     [0,5,0,0,0,0,0,0],
#     [0,0,0,0,0,0,0,0],
#     [0,0,0,0,0,0,0,0],
#     [0,0,0,0,0,0,0,0],
#     [0,0,0,0,6,0,0,0]
# ]

#castle setup
# board = [
#     [4+7,0,0,0,6+7,0,0,4+7],
#     [0,0,0,0,0,0,0,0],
#     [0,0,0,0,0,0,0,0],
#     [0,0,0,0,0,0,0,0],
#     [0,0,0,0,0,0,0,0],
#     [0,0,0,0,0,0,0,0],
#     [0,0,0,0,0,0,0,0],
#     [4,0,0,0,6,0,0,4]
# ]

#castle setup
# board = [
#     [4+7,0,0,0,6+7,0,0,4+7],
#     [0,0,0,0,0,0,0,0],
#     [0,0,0,0,0,0,0,0],
#     [0,0,0,0,0,0,0,0],
#     [0,0,0,0,0,0,0,0],
#     [0,0,0,0,0,0,0,0],
#     [0,0,0,0,0,0,0,0],
#     [4,0,0,0,6,0,0,4]
# ]

def updateUI():
    global whites_turn, ran_out, move_name
    turn_text = "Turn: "
    if whites_turn:
        turn_text += "White"
    else:
        turn_text += "AI (may take a few seconds)"

    if ran_out:
        turn_text = "Ran out of requests"
    screen.blit(Config.TURN_UI_FONT.render(turn_text, True, WHITE, (60,60,255)), (GAME_WIDTH + 10, 0), )
    screen.blit(Config.TURN_UI_FONT.render("Move: " + move_name, True, WHITE, (60,60,255)), (GAME_WIDTH + 10, 50))

def moveAI():
    global whites_turn, ran_out, move_name
    moveString = GeminiAgent.getMove(board)
    print("Response: " + moveString)
    if moveString == "":
        ran_out = True
        print("Ran out of requests")
        sys.exit()
        updateUI()
        return
    updateUI()
    splitString = moveString.split(" ")
    ai_row = splitString[0]
    ai_column = splitString[1]
    ai_piece = board[int(ai_row)][int(ai_column)]
    move_ai_row = splitString[2]
    move_ai_column = splitString[3]
    move_name = ""
    for i in range(4,len(splitString)):
        move_name += splitString[i] + " "
    print("Chosen piece: (" + ai_row + "," + ai_column + ")")
    print("Moving to: (" + move_ai_row + "," + move_ai_column + ")")
    move_ai_row = int(move_ai_row)
    move_ai_column = int(move_ai_column)
    valid_move = True if ai_piece.getValidMoves(board) != None and (move_ai_row, move_ai_column) in ai_piece.getValidMoves(board) else False
    ai_piece.movePiece((move_ai_row, move_ai_column), board)
    whites_turn = True

def inputController():
    global wait_a_frame, mouse_debounce, selected_piece, selected_move, previous_piece, previous_row, previous_column, whites_turn, row, column, selected_row, selected_column, selected_is_black
    if pygame.mouse.get_pressed()[0] and not mouse_debounce:
        mouse_debounce = True
        mouse_pos = pygame.mouse.get_pos()
        if mouse_pos[0] > GAME_WIDTH or mouse_pos[1] > GAME_HEIGHT:
            return

        column = int(mouse_pos[0] // (GAME_WIDTH/BOARD_COLUMNS))
        row = int(mouse_pos[1] // (GAME_HEIGHT/BOARD_ROWS))
        selected_piece = board[row][column]
        selected_move = (row, column)
        print(f"Selected piece: {type(selected_piece).__name__} at position ({row}, {column})")

        if selected_piece.is_white != None: #check if piece is not empty square
            selected_piece.selected = True
    
        valid_move = True if previous_piece.getValidMoves(board) != None and selected_move in previous_piece.getValidMoves(board) else False
        print(f"Piece {type(previous_piece).__name__} at ({previous_piece.row}, {previous_piece.column}) is trying to move to ({row}, {column}), valid move: {valid_move}")
        
        if previous_piece == selected_piece:
            selected_piece.selected = False
            selected_piece = Piece.Empty((-1, -1), None)
        elif previous_piece.is_white == selected_piece.is_white or not valid_move: #deselect if same color
            previous_piece.selected = False
            selected_piece.selected = True
        elif previous_piece.is_white != None and previous_piece.selected: #capture piece if different color
            if whites_turn == previous_piece.is_white and valid_move and Game.move_keeps_king_safe(board, previous_row, previous_column, row, column, previous_piece.is_white): #check if piece color matches turn
                previous_piece.selected = False
                selected_piece.selected = False
                previous_piece.movePiece((row, column), board)

                print(f"{type(previous_piece).__name__} at ({previous_row}, {previous_column}) captured {type(selected_piece).__name__} at position ({row}, {column})")
                whites_turn = not whites_turn
                print("switched to black")
                wait_a_frame = True
            else:
                selected_piece.selected = False
                previous_piece.selected = False

Game.convertBoardToObj(board)

screen.blit(title_screen_image, (0,0))
pygame.display.flip()

clicked = False
while not clicked:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            clicked = True
            running = False
    if pygame.mouse.get_pressed()[0]:
        clicked = True
    
    

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    screen.fill((0,0,0))
    screen.blit(chessboard_image, (0,0))
 
    if whites_turn:
        inputController()

    mouse_debounce = pygame.mouse.get_pressed()[0]
    previous_piece = selected_piece
    previous_row = row
    previous_column = column
    
    for idk1, idk2 in enumerate(board):
        for idk3, idk4 in enumerate(idk2):
            idk4.drawPiece(screen, board)
            if idk4.is_white == True and type(idk4) == Piece.King:
                in_check_white = idk4.isInCheck(board)
            elif idk4.is_white == False and type(idk4) == Piece.King:   
                in_check_black = idk4.isInCheck(board)

    for idk5, idk6 in enumerate(board):
        for idk7, idk8 in enumerate(idk6):
            text_surface = Config.UI_FONT.render(f"{idk5}, {idk7}", True, (0, 0, 0))
            screen.blit(text_surface, (idk7*(GAME_WIDTH/BOARD_COLUMNS), idk5*(GAME_HEIGHT/BOARD_ROWS)))

    # UI rendering
    updateUI()

    # game ending checks
    if Game.is_checkmate(board, True):
        print("Checkmate! Black wins!")
        running = False
    elif Game.is_checkmate(board, False):
        print("Checkmate! White wins!")
        running = False
    elif Game.is_stalemate(board, True):
        print("Stalemate! It's a draw!")
        running = False
    elif Game.is_stalemate(board, False):
        print("Stalemate! It's a draw!")
        running = False

    if not whites_turn:
        if not wait_a_frame:
            moveAI()
        wait_a_frame = False

    pygame.display.flip()

    clock.tick(FPS_CAP)
for row in board: #print the grid in number form
    for piece in row:
        piece_name = type(piece).__name__
        print(ChessPiece[piece_name.upper()].value if piece.is_white == True else ChessPiece[piece_name.upper()].value + 7, end=" ")
    print()
pygame.quit()
sys.exit()
