import Piece
import Config
from pygame.math import Vector2

def move_keeps_king_safe(board, start_row, start_col, end_row, end_col, is_white):
    
    moving_piece = board[start_row][start_col]
    captured_piece = board[end_row][end_col]
    # simulate move
    board[end_row][end_col] = moving_piece
    board[start_row][start_col] = Piece.Empty((start_row, start_col), None)
    moving_piece.row = end_row
    moving_piece.column = end_col
    # find king
    king = None
    for row in board:
        for piece in row:
            if isinstance(piece, Piece.King) and piece.is_white == is_white:
                king = piece
                break
        if king:
            break
    # safety fallback
    if king is None:
        result = False
    else:
        result = not king.isInCheck(board)
    # undo move
    board[start_row][start_col] = moving_piece
    board[end_row][end_col] = captured_piece
    moving_piece.row = start_row
    moving_piece.column = start_col

    return result
def is_checkmate(board, is_white):
    
    # 1. Find king safely
    king = None
    for row in board:
        for piece in row:
            if isinstance(piece, Piece.King) and piece.is_white == is_white:
                king = piece
                break
        if king:
            break
    if king is None:
        return False  # safety fallback
    # 2. If NOT in check → not checkmate
    if not king.isInCheck(board):
        return False
    # 3. Try ALL moves for all pieces
    for row in board:
        for piece in row:
            if piece.is_white != is_white:
                continue
            moves = piece.getValidMoves(board) or []
            print(f"Checking {type(piece).__name__} at ({piece.row}, {piece.column}) with moves: {moves}")
            for move_row, move_col in moves:
                if move_keeps_king_safe(board, piece.row, piece.column, move_row, move_col, is_white):
                    return False  # found escape → not checkmate
    return True
def is_stalemate(board, is_white):

    # Find king
    king = None
    for row in board:
        for piece in row:
            if isinstance(piece, Piece.King) and piece.is_white == is_white:
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
