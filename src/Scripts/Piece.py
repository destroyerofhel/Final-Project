import pygame
from pygame import Vector2
import Config
from Main import board

class Piece:
    def __init__(self, position: Vector2):
        self.row = position.x
        self.column = position.y
        self.selected = False
        self.is_white = True
    def movePiece(self):
        pass
    def drawPiece(self, screen):
        pass
    def removePiece(self):
        pass
    def getAvailableMoves(self):
        pass
    def selectPiece(self, screen):
        self.selected = True
        for i in self.getAvailableMoves():
            x_pos = i[0]
            y_pos = i[1]
            if board[x_pos][y_pos] == 0 or board[x_pos][y_pos].is_white != self.is_white:
                x_size = Config.WIDTH // Config.BOARD_COLUMNS
                y_size = Config.HEIGHT // Config.BOARD_ROWS
                pygame.draw.circle(screen, (255, 0, 0), (x_pos, y_pos), x_size//2)

class Pawn(Piece):
    def getAvailableMoves(self):
        if self.is_white:
            return [self.row, self.column + 1]
        else:
            return [self.row, self.column - 1]

class Bishop(Piece):
    def getAvailableMoves(self):
        moves = []
        for distance in range(1,8):
            moves+=[(self.row+distance, self.column+distance)]
            moves+=[(self.row+distance, self.column-distance)]
            moves+=[(self.row-distance, self.column+distance)]
            moves+=[(self.row-distance, self.column-distance)]
        return moves

class Knight(Piece):
    def getAvailableMoves(self):
        moves = []
        moves+=[(self.row + 2, self.column + 1)]
        moves+=[(self.row + 2, self.column - 1)]
        moves+=[(self.row - 2, self.column + 1)]
        moves+=[(self.row - 2, self.column - 1)]
        moves+=[(self.row + 1, self.column + 2)]
        moves+=[(self.row + 1, self.column - 2)]
        moves+=[(self.row - 1, self.column + 2)]
        moves+=[(self.row - 1, self.column - 2)]
        return moves
    
class Rook(Piece):
    def getAvailableMoves(self):
        moves = []
        for distance in range(1, 8):
            moves+=[(self.row+distance, self.column)]
            moves+=[(self.row-distance, self.column)]
            moves+=[(self.row, self.column+distance)]
            moves+=[(self.row, self.column-distance)]
        return moves

class Queen(Piece):
    def getAvailableMoves(self):
        moves = []
        for distance in range(1, 8):
            moves+=[(self.row+distance, self.column)]
            moves+=[(self.row-distance, self.column)]
            moves+=[(self.row, self.column+distance)]
            moves+=[(self.row, self.column-distance)]
            
            moves+=[(self.row+distance, self.column+distance)]
            moves+=[(self.row+distance, self.column-distance)]
            moves+=[(self.row-distance, self.column+distance)]
            moves+=[(self.row-distance, self.column-distance)]
        return moves


class King(Piece):
    def isInCheck(self):
        pass