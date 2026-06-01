import Piece
import Config
from pygame.math import Vector2

def move_keeps_king_safe(board, start_row, start_col, end_row, end_col, is_white):

    moving_piece = board[start_row][start_col]
    captured_piece = board[end_row][end_col]

    # Simulate move
    board[end_row][end_col] = moving_piece
    board[start_row][start_col] = Piece.Empty((start_row, start_col), None)

    moving_piece.row = end_row
    moving_piece.column = end_col

    # Find king and check if attacked
    king_safe = True

    for row in board:
        for piece in row:
            if type(piece) == Piece.King and piece.is_white == is_white:
                king_safe = not piece.isInCheck(board)
                break

    # Undo move
    board[start_row][start_col] = moving_piece
    board[end_row][end_col] = captured_piece

    moving_piece.row = start_row
    moving_piece.column = start_col

    return king_safe
def is_checkmate(board, is_white):
    
    # Find king
    king = None
    for row in board:
        for piece in row:
            if type(piece) == Piece.King and piece.is_white == is_white:
                king = piece
                break
    if not king.isInCheck(board):
        return False
    for row in board:
        for piece in row:
            if piece.is_white != is_white:
                continue
            moves = piece.getValidMoves(board)
            if moves is None:
                continue
            for move_row, move_col in moves:
                if move_keeps_king_safe(
                    board,
                    piece.row,
                    piece.column,
                    move_row,
                    move_col,
                    is_white
                ):
                    return False
    return True
def is_stalemate(board, is_white):

    # Find king
    king = None
    for row in board:
        for piece in row:
            if type(piece) == Piece.King and piece.is_white == is_white:
                king = piece
                break
    # Stalemate only if NOT in check
    if king.isInCheck(board):
        return False
    # Check for any legal move
    for row in board:
        for piece in row:
            if piece.is_white != is_white:
                continue
            moves = piece.getValidMoves(board)
            if moves is None:
                continue
            for move_row, move_col in moves:
                if move_keeps_king_safe(
                    board,
                    piece.row,
                    piece.column,
                    move_row,
                    move_col,
                    is_white
                ):
                    return False
    return True
def convertBoardToObj(board):
    isWhite = True
    for x,row in enumerate(board):
        for y in range(len(row)):
            if row[y] / 7 > 1:
                isWhite = False
            else:
                isWhite = True
            vector = Vector2(x, y)
            if row[y] % 7 == 1:
                board[x][y] = Piece.Pawn(vector, isWhite)
            elif row[y] % 7 == 2:
                board[x][y] = Piece.Bishop(vector, isWhite)
            elif row[y] % 7 == 3:
                board[x][y] = Piece.Knight(vector, isWhite)
            elif row[y] % 7 == 4:
                board[x][y] = Piece.Rook(vector, isWhite)
            elif row[y] % 7 == 5:
                board[x][y] = Piece.Queen(vector, isWhite)
            elif row[y] % 7 == 6:
                board[x][y] = Piece.King(vector, isWhite)
            else: 
                board[x][y] = Piece.Empty(vector, None)
