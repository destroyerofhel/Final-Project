import pygame
import Config
import Game

def keepInBounds(available_moves: list[tuple[int, int]]):
    in_bounds_moves = []
    for move in available_moves:
        x_pos = move[0]
        y_pos = move[1]
        in_bounds = x_pos >= 0 and x_pos < Config.BOARD_ROWS and y_pos >= 0 and y_pos < Config.BOARD_COLUMNS
        if in_bounds:
            in_bounds_moves.append(move)
    return in_bounds_moves

class Piece:
    def __init__(self, position: tuple[int, int], is_white: bool):
        self.row = int(position[0])
        self.column = int(position[1])
        self.selected = False
        self.is_white = is_white
        self.piece_type = 0
    def movePiece(self):
        pass
    def drawPiece(self, screen, board):
        pass
    def removePiece(self):
        pass
    def getValidMoves(self, board):
        pass
    def getAvailableMoves(self, board):
        return self.getValidMoves(board)
    def selectPiece(self, screen, board):
        for i in self.getValidMoves(board):
            x_pos = i[0]
            y_pos = i[1]
            in_bounds = x_pos >= 0 and x_pos < Config.BOARD_ROWS and y_pos >= 0 and y_pos < Config.BOARD_COLUMNS
            if in_bounds:
                x_size = Config.WIDTH // Config.BOARD_COLUMNS
                y_size = Config.HEIGHT // Config.BOARD_ROWS

                radius = int((Config.WIDTH/Config.BOARD_COLUMNS) // 2 * 0.8)
                move_surface = pygame.Surface((radius * 2, radius * 2), pygame.SRCALPHA)
                pygame.draw.circle(
                    move_surface,
                    (0, 0, 0, 100),
                    (radius, radius),
                    radius
                )
                screen.blit(move_surface, (y_pos * x_size + x_size // 2 - radius, x_pos * y_size + y_size // 2 - radius))
    
    def checkVerticalUp(self, board):
        moves = []
        for distance in range(1, self.row + 1):
            if board[self.row - distance][self.column].is_white == None:
                moves.append((self.row - distance, self.column))
            elif board[self.row - distance][self.column].is_white != self.is_white:
                moves.append((self.row - distance, self.column))
                break
            else:
                break
        return moves
    def checkVerticalDown(self, board):
    
        moves = []
        for distance in range(1, Config.BOARD_ROWS - self.row):
            if board[self.row + distance][self.column].is_white == None:
                moves.append((self.row + distance, self.column))
            elif board[self.row + distance][self.column].is_white != self.is_white:
                moves.append((self.row + distance, self.column))
                break
            else:
                break
        return moves
    def checkHorizontalRight(self, board):
        moves = []
        for distance in range(1, Config.BOARD_COLUMNS - self.column):
            if board[self.row][self.column + distance].is_white == None:
                moves.append((self.row, self.column + distance))
            elif board[self.row][self.column + distance].is_white != self.is_white:
                moves.append((self.row, self.column + distance))
                break
            else:
                break
        return moves
    def checkHorizontalLeft(self, board):
        moves = []
        for distance in range(1, self.column + 1):
            if board[self.row][self.column - distance].is_white == None:
                moves.append((self.row, self.column - distance))
            elif board[self.row][self.column - distance].is_white != self.is_white:
                moves.append((self.row, self.column - distance))
                break
            else:
                break
        return moves
    def checkDiagonalUpRight(self, board):
        moves = []
        for distance in range(1, min(self.row + 1, Config.BOARD_COLUMNS - self.column)):
            if board[self.row - distance][self.column + distance].is_white == None:
                moves.append((self.row - distance, self.column + distance))
            elif board[self.row - distance][self.column + distance].is_white != self.is_white:
                moves.append((self.row - distance, self.column + distance))
                break
            else:
                break
            
        return moves
    def checkDiagonalUpLeft(self, board):
        moves = []
        for distance in range(1, min(self.row + 1, self.column + 1)):
            if board[self.row - distance][self.column - distance].is_white == None:
                moves.append((self.row - distance, self.column - distance))
            elif board[self.row - distance][self.column - distance].is_white != self.is_white:
                moves.append((self.row - distance, self.column - distance))
                break
            else:
                break
        return moves
    def checkDiagonalDownRight(self, board):
    
        moves = []
        for distance in range(1, min(Config.BOARD_ROWS - self.row, Config.BOARD_COLUMNS - self.column)):
            if board[self.row + distance][self.column + distance].is_white == None:
                moves.append((self.row + distance, self.column + distance))
            elif board[self.row + distance][self.column + distance].is_white != self.is_white:
                moves.append((self.row + distance, self.column + distance))
                break
            else:
                break
        return moves
    def checkDiagonalDownLeft(self, board):
        moves = []
        for distance in range(1, min(Config.BOARD_ROWS - self.row, self.column + 1)):
            if board[self.row + distance][self.column - distance].is_white == None:
                moves.append((self.row + distance, self.column - distance))
            elif board[self.row + distance][self.column - distance].is_white != self.is_white:
                moves.append((self.row + distance, self.column - distance))
                break
            else:
                break
        return moves

class Empty(Piece):
    def __init__(self, position: tuple[int, int], is_white: bool):
        super().__init__(position, is_white)

class Pawn(Piece):
    piece_type = 1
    def drawPiece(self, screen, board):
        color = "White"
        if(not self.is_white):
            color = "Black"
        size = (Config.WIDTH/Config.BOARD_COLUMNS,Config.HEIGHT/Config.BOARD_ROWS)
        loaded_image = pygame.transform.scale(pygame.image.load(Config.SPRITES_DIRECTORY + color + "\\pawn.png"), size)
        screen.blit(loaded_image, (self.column*size[0], self.row*size[1]))

        if self.selected:
            self.selectPiece(screen, board)
    def getAvailableMoves(self, board):
        # moves = []
        # if self.is_white:
        #     moves.append((self.row - 1, self.column))
        #     if self.row == 6:
        #         moves.append((self.row - 2, self.column))
        # else:
        #     moves.append((self.row + 1, self.column))
        #     if self.row == 1:
        #         moves.append((self.row + 2, self.column))
        # return moves
        return self.getValidMoves(board)
        
    def getValidMoves(self, board):
        moves = []
        if self.is_white:
            if self.row == 6 and board[self.row - 2][self.column].is_white == None and board[self.row - 1][self.column].is_white == None:
                moves.append((self.row - 2, self.column))
            if self.row > 0 and board[self.row - 1][self.column].is_white == None:
                moves.append((self.row - 1, self.column))
            if self.row > 0 and self.column > 0 and board[self.row - 1][self.column - 1].is_white != None and board[self.row - 1][self.column - 1].is_white != self.is_white:
                moves.append((self.row - 1, self.column - 1))
            if self.row > 0 and self.column < Config.BOARD_COLUMNS - 1 and board[self.row - 1][self.column + 1].is_white != None and board[self.row - 1][self.column + 1].is_white != self.is_white:
                moves.append((self.row - 1, self.column + 1))
        else:
            if self.row == 1 and board[self.row + 2][self.column].is_white == None and board[self.row + 1][self.column].is_white == None:
                moves.append((self.row + 2, self.column))
            if self.row < Config.BOARD_ROWS - 1 and board[self.row + 1][self.column].is_white == None:
                moves.append((self.row + 1, self.column))
            if self.row < Config.BOARD_ROWS - 1 and self.column > 0 and board[self.row + 1][self.column - 1].is_white != None and board[self.row + 1][self.column - 1].is_white != self.is_white:
                moves.append((self.row + 1, self.column - 1))
            if self.row < Config.BOARD_ROWS - 1 and self.column < Config.BOARD_COLUMNS - 1 and board[self.row + 1][self.column + 1].is_white != None and board[self.row + 1][self.column + 1].is_white != self.is_white:
                moves.append((self.row + 1, self.column + 1))       
        return moves
        
class Bishop(Piece):
    piece_type = 2
    def drawPiece(self, screen, board):
        color = "White"
        if(not self.is_white):
            color = "Black"
        size = (Config.WIDTH/Config.BOARD_COLUMNS,Config.HEIGHT/Config.BOARD_ROWS)
        loaded_image = pygame.transform.scale(pygame.image.load(Config.SPRITES_DIRECTORY + color + "\\bishop.png"), size)
        screen.blit(loaded_image, (self.column*size[0], self.row*size[1]))

        if self.selected:
            self.selectPiece(screen, board)
    def getValidMoves(self, board):
        moves = [] 

        moves += self.checkDiagonalUpRight(board)
        moves += self.checkDiagonalUpLeft(board)
        moves += self.checkDiagonalDownRight(board)
        moves += self.checkDiagonalDownLeft(board)

        return keepInBounds(moves)
    def getAvailableMoves(self, board):
        # moves = []
        # for distance in range(1,8):
        #     moves+=[(self.row+distance, self.column+distance)]
        #     moves+=[(self.row+distance, self.column-distance)]
        #     moves+=[(self.row-distance, self.column+distance)]
        #     moves+=[(self.row-distance, self.column-distance)]
        # return keepInBounds(moves)
        return self.getValidMoves(board)

class Knight(Piece):
    piece_type = 3
    def drawPiece(self, screen, board):
        color = "White"
        if(not self.is_white):
            color = "Black"
        size = (Config.WIDTH/Config.BOARD_COLUMNS,Config.HEIGHT/Config.BOARD_ROWS)
        loaded_image = pygame.transform.scale(pygame.image.load(Config.SPRITES_DIRECTORY + color + "\\knight.png"), size)
        screen.blit(loaded_image, (self.column*size[0], self.row*size[1]))
        if self.selected:
            self.selectPiece(screen, board)
    def getValidMoves(self, board):
        moves = []
        for move in self.getAvailableMoves(board):
            if move[0] >= 0 and move[0] < Config.BOARD_ROWS and move[1] >= 0 and move[1] < Config.BOARD_COLUMNS:
                if board[move[0]][move[1]].is_white == None or board[move[0]][move[1]].is_white != self.is_white:
                    moves.append(move)
        return keepInBounds(moves)
    def getAvailableMoves(self, board):
        moves = []
        moves+=[(self.row + 2, self.column + 1)]
        moves+=[(self.row + 2, self.column - 1)]
        moves+=[(self.row - 2, self.column + 1)]
        moves+=[(self.row - 2, self.column - 1)]
        moves+=[(self.row + 1, self.column + 2)]
        moves+=[(self.row + 1, self.column - 2)]
        moves+=[(self.row - 1, self.column + 2)]
        moves+=[(self.row - 1, self.column - 2)]
        return keepInBounds(moves)
    
class Rook(Piece):
    piece_type = 4
    def drawPiece(self, screen, board):
        color = "White"
        if(not self.is_white):
            color = "Black"
        size = (Config.WIDTH/Config.BOARD_COLUMNS,Config.HEIGHT/Config.BOARD_ROWS)
        loaded_image = pygame.transform.scale(pygame.image.load(Config.SPRITES_DIRECTORY + color + "\\rook.png"), size)
        screen.blit(loaded_image, (self.column*size[0], self.row*size[1]))

        if self.selected:
            self.selectPiece(screen, board)
    def getValidMoves(self, board):
        moves = []

        moves += self.checkVerticalUp(board)
        moves += self.checkVerticalDown(board)
        moves += self.checkHorizontalRight(board)
        moves += self.checkHorizontalLeft(board)

        return keepInBounds(moves)
    def getAvailableMoves(self, board):
        # moves = []
        # for distance in range(1, 8):
        #     moves+=[(self.row+distance, self.column)]
        #     moves+=[(self.row-distance, self.column)]
        #     moves+=[(self.row, self.column+distance)]
        #     moves+=[(self.row, self.column-distance)]
        # return moves
        return self.getValidMoves(board)

class Queen(Piece):
    piece_type = 5
    def drawPiece(self, screen, board):
        color = "White"
        if(not self.is_white):
            color = "Black"
        size = (Config.WIDTH/Config.BOARD_COLUMNS,Config.HEIGHT/Config.BOARD_ROWS)
        loaded_image = pygame.transform.scale(pygame.image.load(Config.SPRITES_DIRECTORY + color + "\\queen.png"), size)
        screen.blit(loaded_image, (self.column*size[0], self.row*size[1]))
        
        if self.selected:
            self.selectPiece(screen, board)
    def getValidMoves(self, board):
        moves = []

        moves += self.checkVerticalUp(board)
        moves += self.checkVerticalDown(board)
        moves += self.checkHorizontalRight(board)
        moves += self.checkHorizontalLeft(board)
        moves += self.checkDiagonalUpRight(board)
        moves += self.checkDiagonalUpLeft(board)
        moves += self.checkDiagonalDownRight(board)
        moves += self.checkDiagonalDownLeft(board)

        return keepInBounds(moves)
    def getAvailableMoves(self, board):
        # moves = []
        # for distance in range(1, 8):
        #     moves+=[(self.row+distance, self.column)]
        #     moves+=[(self.row-distance, self.column)]
        #     moves+=[(self.row, self.column+distance)]
        #     moves+=[(self.row, self.column-distance)]
            
        #     moves+=[(self.row+distance, self.column+distance)]
        #     moves+=[(self.row+distance, self.column-distance)]
        #     moves+=[(self.row-distance, self.column+distance)]
        #     moves+=[(self.row-distance, self.column-distance)]
        # return keepInBounds(moves)
        return self.getValidMoves(board)

class King(Piece):
    piece_type = 6

    def drawPiece(self, screen, board):
        color = "White"
        if(not self.is_white):
            color = "Black"
        size = (Config.WIDTH/Config.BOARD_COLUMNS,Config.HEIGHT/Config.BOARD_ROWS)
        loaded_image = pygame.transform.scale(pygame.image.load(Config.SPRITES_DIRECTORY + color + "\\king.png"), size)
        screen.blit(loaded_image, (self.column*size[0], self.row*size[1]))

        if self.selected:
            self.selectPiece(screen, board)
    def getValidMoves(self, board):
        moves = []
        for move in self.getAvailableMoves(board):
            row, column = move
            if 0 <= row < Config.BOARD_ROWS and 0 <= column < Config.BOARD_COLUMNS:
                target = board[row][column]
                is_empty = target.is_white is None
                is_enemy = target.is_white is not None and target.is_white != self.is_white
                if (is_empty or is_enemy) and Game.move_keeps_king_safe(board, self.row, self.column, row, column, self.is_white):
                    moves.append(move)
        return keepInBounds(moves)
    def getAvailableMoves(self, board):
        moves = []
        moves+=[(self.row + 1, self.column)]
        moves+=[(self.row + 1, self.column + 1)]
        moves+=[(self.row + 1, self.column - 1)]
        moves+=[(self.row, self.column + 1)]
        moves+=[(self.row, self.column - 1)]
        moves+=[(self.row - 1, self.column + 1)]
        moves+=[(self.row - 1, self.column)]
        moves+=[(self.row - 1, self.column - 1)]
        return keepInBounds(moves)
    def isInCheck(self, board):
        for row_num, row in enumerate(board):
            for col_num, piece in enumerate(row):
                if piece.is_white != self.is_white and piece.getAvailableMoves(board) != None and (self.row, self.column) in piece.getAvailableMoves(board):
                    return True
        return False
