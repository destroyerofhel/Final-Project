import pygame
from pygame import Vector2
import Config

class Piece:
    def __init__(self, position: Vector2, isWhite: bool, type: int):
        self.row = position.x
        self.column = position.y
        self.selected = False
        self.is_white = isWhite
        self.piece_type = type
    def movePiece(self):
        pass
    def drawPiece(self, screen):
        import Main
        color = "White/"
        if not self.is_white: color = "Black/"
        path = Main.SPRITES_DIRECTORY + color + Main.ChessPiece(self.piece_type).name.lower() + ".png"
        size = (Config.WIDTH/Config.BOARD_COLUMNS, Config.HEIGHT/Config.BOARD_ROWS)
        loaded_image = pygame.transform.scale(pygame.image.load(path), (size))
        screen.blit(loaded_image, (0,0))

    def removePiece(self):
        pass
    def getAvailableMoves(self):
        pass
    def selectPiece(self, screen):
        import Main
        self.selected = True
        for i in self.getAvailableMoves():
            x_pos = i[0]
            y_pos = i[1]
            if Main.board[x_pos][y_pos] == 0 or Main.board[x_pos][y_pos].is_white != self.is_white:
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
    def getAvailableMoves(self):
        moves = []
        moves+=[(self.row + 1, self.column)]
        moves+=[(self.row + 1, self.column + 1)]
        moves+=[(self.row + 1, self.column - 1)]
        moves+=[(self.row, self.column + 1)]
        moves+=[(self.row, self.column - 1)]
        moves+=[(self.row - 1, self.column + 1)]
        moves+=[(self.row - 1, self.column)]
        moves+=[(self.row - 1, self.column - 1)]
        return moves
    
    def isInCheck(self):
        pass