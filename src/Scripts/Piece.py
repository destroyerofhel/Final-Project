import math

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
def checkVerticalUp(position: tuple[int, int], board):
    moves = []
    row, column = position
    for distance in range(1, row + 1):
        if board[row - distance][column].is_white == None:
            moves.append((row - distance, column))
        elif board[row - distance][column].is_white != board[row][column].is_white:
            moves.append((row - distance, column))
            break
        else:
            break
    return moves
def checkVerticalDown(position: tuple[int, int], board):

    moves = []
    row, column = position
    for distance in range(1, Config.BOARD_ROWS - row):
        if board[row + distance][column].is_white == None:
            moves.append((row + distance, column))
        elif board[row + distance][column].is_white != board[row][column].is_white:
            moves.append((row + distance, column))
            break
        else:
            break
    return moves
def checkHorizontalRight(position: tuple[int, int], board):
    row, column = position  
    moves = []
    for distance in range(1, Config.BOARD_COLUMNS - column):
        if board[row][column + distance].is_white == None:
            moves.append((row, column + distance))
        elif board[row][column + distance].is_white != board[row][column].is_white:
            moves.append((row, column + distance))
            break
        else:
            break
    return moves
def checkHorizontalLeft(position: tuple[int, int], board):
    row, column = position

    moves = []
    for distance in range(1, column + 1):
        if board[row][column - distance].is_white == None:
            moves.append((row, column - distance))
        elif board[row][column - distance].is_white != board[row][column].is_white:
            moves.append((row, column - distance))
            break
        else:
            break
    return moves
def checkDiagonalUpRight(position: tuple[int, int], board):
    row, column = position
    moves = []
    for distance in range(1, min(row + 1, Config.BOARD_COLUMNS - column)):
        if board[row - distance][column + distance].is_white == None:
            moves.append((row - distance, column + distance))
        elif board[row - distance][column + distance].is_white != board[row][column].is_white:
            moves.append((row - distance, column + distance))
            break
        else:
            break
        
    return moves
def checkDiagonalUpLeft(position: tuple[int, int], board):
    row, column = position
    moves = []
    for distance in range(1, min(row + 1, column + 1)):
        if board[row - distance][column - distance].is_white == None:
            moves.append((row - distance, column - distance))
        elif board[row - distance][column - distance].is_white != board[row][column].is_white:
            moves.append((row - distance, column - distance))
            break
        else:
            break
    return moves
def checkDiagonalDownRight(position: tuple[int, int], board):
    row, column = position  
    moves = []
    for distance in range(1, min(Config.BOARD_ROWS - row, Config.BOARD_COLUMNS - column)):
        if board[row + distance][column + distance].is_white == None:
            moves.append((row + distance, column + distance))
        elif board[row + distance][column + distance].is_white != board[row][column].is_white:
            moves.append((row + distance, column + distance))
            break
        else:
            break
    return moves
def checkDiagonalDownLeft(position: tuple[int, int], board):
    row, column = position
    moves = []
    for distance in range(1, min(Config.BOARD_ROWS - row, column + 1)):
        if board[row + distance][column - distance].is_white == None:
            moves.append((row + distance, column - distance))
        elif board[row + distance][column - distance].is_white != board[row][column].is_white:
            moves.append((row + distance, column - distance))
            break
        else:
            break
    return moves

class Piece:
    def __init__(self, position: tuple[int, int], is_white: bool):
        self.row = int(position[0])
        self.column = int(position[1])
        self.selected = False
        self.is_white = is_white
        self.has_moved = False
    def movePiece(self, new_position: tuple[int, int], board):
        board[self.row][self.column] = Empty((self.row, self.column), None)
        board[new_position[0]][new_position[1]] = self
        self.row = new_position[0]
        self.column = new_position[1]
        self.has_moved = True
        return True
    def drawPiece(self, screen, board):
        pass
    def removePiece(self):
        pass
    def getValidMoves(self, board):
        moves = []
        if self.getAvailableMoves(board) == None:
            return None
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
        pass
    def selectPiece(self, screen, board):
        for i in self.getValidMoves(board):
            x_pos = i[0]
            y_pos = i[1]
            in_bounds = x_pos >= 0 and x_pos < Config.BOARD_ROWS and y_pos >= 0 and y_pos < Config.BOARD_COLUMNS
            if in_bounds:
                x_size = Config.GAME_WIDTH // Config.BOARD_COLUMNS
                y_size = Config.GAME_HEIGHT // Config.BOARD_ROWS

                radius = int((Config.GAME_WIDTH/Config.BOARD_COLUMNS) // 2 * 0.8)
                move_surface = pygame.Surface((radius * 2, radius * 2), pygame.SRCALPHA)
                pygame.draw.circle(
                    move_surface,
                    (0, 0, 0, 100),
                    (radius, radius),
                    radius
                )
                screen.blit(move_surface, (y_pos * x_size + x_size // 2 - radius, x_pos * y_size + y_size // 2 - radius))



class Empty(Piece):
    def __init__(self, position: tuple[int, int], is_white: bool):
        super().__init__(position, is_white)

class Pawn(Piece):
    piece_type = 1
    def drawPiece(self, screen, board):
        color = "White"
        if(not self.is_white):
            color = "Black"
        size = (Config.GAME_WIDTH/Config.BOARD_COLUMNS,Config.GAME_HEIGHT/Config.BOARD_ROWS)
        loaded_image = pygame.transform.scale(pygame.image.load(Config.SPRITES_DIRECTORY + color + "\\pawn.png"), size)
        screen.blit(loaded_image, (self.column*size[0], self.row*size[1]))

        if self.selected:
            self.selectPiece(screen, board)
    def getAvailableMoves(self, board):
        moves = []
        if self.is_white:
            if not self.has_moved and board[self.row - 2][self.column].is_white == None and board[self.row - 1][self.column].is_white == None:
                moves.append((self.row - 2, self.column))
            if self.row > 0 and board[self.row - 1][self.column].is_white == None:
                moves.append((self.row - 1, self.column))
            if self.row > 0 and self.column > 0 and board[self.row - 1][self.column - 1].is_white != None and board[self.row - 1][self.column - 1].is_white != self.is_white:
                moves.append((self.row - 1, self.column - 1))
            if self.row > 0 and self.column < Config.BOARD_COLUMNS - 1 and board[self.row - 1][self.column + 1].is_white != None and board[self.row - 1][self.column + 1].is_white != self.is_white:
                moves.append((self.row - 1, self.column + 1))
        else:
            if not self.has_moved and board[self.row + 2][self.column].is_white == None and board[self.row + 1][self.column].is_white == None:
                moves.append((self.row + 2, self.column))
            if self.row < Config.BOARD_ROWS - 1 and board[self.row + 1][self.column].is_white == None:
                moves.append((self.row + 1, self.column))
            if self.row < Config.BOARD_ROWS - 1 and self.column > 0 and board[self.row + 1][self.column - 1].is_white != None and board[self.row + 1][self.column - 1].is_white != self.is_white:
                moves.append((self.row + 1, self.column - 1))
            if self.row < Config.BOARD_ROWS - 1 and self.column < Config.BOARD_COLUMNS - 1 and board[self.row + 1][self.column + 1].is_white != None and board[self.row + 1][self.column + 1].is_white != self.is_white:
                moves.append((self.row + 1, self.column + 1))  
        return keepInBounds(moves)


class Bishop(Piece):
    piece_type = 2
    def drawPiece(self, screen, board):
        color = "White"
        if(not self.is_white):
            color = "Black"
        size = (Config.GAME_WIDTH/Config.BOARD_COLUMNS,Config.GAME_HEIGHT/Config.BOARD_ROWS)
        loaded_image = pygame.transform.scale(pygame.image.load(Config.SPRITES_DIRECTORY + color + "\\bishop.png"), size)
        screen.blit(loaded_image, (self.column*size[0], self.row*size[1]))

        if self.selected:
            self.selectPiece(screen, board)
    def getAvailableMoves(self, board):
        moves = [] 

        moves += checkDiagonalUpRight((self.row, self.column), board)
        moves += checkDiagonalUpLeft((self.row, self.column), board)
        moves += checkDiagonalDownRight((self.row, self.column), board)
        moves += checkDiagonalDownLeft((self.row, self.column), board)

        return keepInBounds(moves)

class Knight(Piece):
    piece_type = 3
    def drawPiece(self, screen, board):
        color = "White"
        if(not self.is_white):
            color = "Black"
        size = (Config.GAME_WIDTH/Config.BOARD_COLUMNS,Config.GAME_HEIGHT/Config.BOARD_ROWS)
        loaded_image = pygame.transform.scale(pygame.image.load(Config.SPRITES_DIRECTORY + color + "\\knight.png"), size)
        screen.blit(loaded_image, (self.column*size[0], self.row*size[1]))
        if self.selected:
            self.selectPiece(screen, board)
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

        legal_moves = []
        for move in keepInBounds(moves):
            if board[move[0]][move[1]].is_white == None or board[move[0]][move[1]].is_white != self.is_white:
                legal_moves.append(move)
        return legal_moves

class Rook(Piece):
    piece_type = 4
    def drawPiece(self, screen, board):
        color = "White"
        if(not self.is_white):
            color = "Black"
        size = (Config.GAME_WIDTH/Config.BOARD_COLUMNS,Config.GAME_HEIGHT/Config.BOARD_ROWS)
        loaded_image = pygame.transform.scale(pygame.image.load(Config.SPRITES_DIRECTORY + color + "\\rook.png"), size)
        screen.blit(loaded_image, (self.column*size[0], self.row*size[1]))

        if self.selected:
            self.selectPiece(screen, board)
    def getAvailableMoves(self, board):
        moves = []
        moves += checkVerticalUp((self.row, self.column), board)
        moves += checkVerticalDown((self.row, self.column), board)
        moves += checkHorizontalRight((self.row, self.column), board)
        moves += checkHorizontalLeft((self.row, self.column), board)

        return keepInBounds(moves)

class Queen(Piece):
    piece_type = 5
    def drawPiece(self, screen, board):
        color = "White"
        if(not self.is_white):
            color = "Black"
        size = (Config.GAME_WIDTH/Config.BOARD_COLUMNS,Config.GAME_HEIGHT/Config.BOARD_ROWS)
        loaded_image = pygame.transform.scale(pygame.image.load(Config.SPRITES_DIRECTORY + color + "\\queen.png"), size)
        screen.blit(loaded_image, (self.column*size[0], self.row*size[1]))
        
        if self.selected:
            self.selectPiece(screen, board)
    def getAvailableMoves(self, board):
        moves = []

        moves += checkVerticalUp((self.row, self.column), board)
        moves += checkVerticalDown((self.row, self.column), board)
        moves += checkHorizontalRight((self.row, self.column), board)
        moves += checkHorizontalLeft((self.row, self.column), board)
        moves += checkDiagonalUpRight((self.row, self.column), board)
        moves += checkDiagonalUpLeft((self.row, self.column), board)
        moves += checkDiagonalDownRight((self.row, self.column), board)
        moves += checkDiagonalDownLeft((self.row, self.column), board)

        return moves

class King(Piece):
    piece_type = 6

    def drawPiece(self, screen, board):
        color = "White"
        if(not self.is_white):
            color = "Black"
        size = (Config.GAME_WIDTH/Config.BOARD_COLUMNS,Config.GAME_HEIGHT/Config.BOARD_ROWS)
        loaded_image = pygame.transform.scale(pygame.image.load(Config.SPRITES_DIRECTORY + color + "\\king.png"), size)
        screen.blit(loaded_image, (self.column*size[0], self.row*size[1]))

        if self.selected:
            self.selectPiece(screen, board)

    def can_castle(self, board, rook_position):
        rook_row, rook_col = rook_position
        if self.has_moved:
            print(f"King {self.row}, {self.column} has already moved, cannot castle")
            return False
        if board[rook_row][rook_col].is_white != self.is_white:
            print(f"Rook {rook_row}, {rook_col} is not the same color as king, cannot castle")
            return False
        if board[rook_row][rook_col].has_moved:
            print(f"Rook {rook_row}, {rook_col} has already moved, cannot castle")
            return False
        return True

    def castle_moves(self, board):
        if self.has_moved:
            return []
        moves = []
        pieces = checkHorizontalRight((self.row, self.column), board) + checkHorizontalLeft((self.row, self.column), board)
        for piece in pieces:
            if piece[1] == 7 or piece[1] == 0:
                continue
            piece_row = piece[0]
            piece_col = piece[1] - 1 if piece[1] < self.column else piece[1] + 1
            
            print(f"Checking for castle move with piece at {piece_row}, {piece_col}")
            if isinstance(board[piece_row][piece_col], Rook) and self.can_castle(board, (piece_row, piece_col)):
                moves.append((math.ceil((piece_row + self.row)/2), math.ceil((piece_col + self.column)/2)))
                
        return moves
    
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

        legal_moves = []
        for move in keepInBounds(moves):
            if board[move[0]][move[1]].is_white == None or board[move[0]][move[1]].is_white != self.is_white:
                legal_moves.append(move)
        return legal_moves
    
    def getValidMoves(self, board):
        moves = []
        for move in self.getAvailableMoves(board):
            if Game.move_keeps_king_safe(board, self.row, self.column, move[0], move[1], self.is_white):
                moves.append(move)
        for move in self.castle_moves(board):
            if Game.move_keeps_king_safe(board, self.row, self.column, move[0], move[1], self.is_white):
                moves.append(move)
            
        return keepInBounds(moves)
    
    def movePiece(self, new_position: tuple[int, int], board):
        if new_position in self.castle_moves(board):
            rook_col = 0 if new_position[1] < self.column else Config.BOARD_COLUMNS - 1
            rook_new_col = self.column - 1 if new_position[1] < self.column else self.column + 1
            board[self.row][rook_col].movePiece((self.row, rook_new_col), board)
        return super().movePiece(new_position, board)

    def isInCheck(self, board):
        for row_num, row in enumerate(board):
            for col_num, piece in enumerate(row):
                if piece.is_white != self.is_white and piece.getAvailableMoves(board) != None and (self.row, self.column) in piece.getAvailableMoves(board):
                    return True
        return False
