from dotenv import load_dotenv
from google import genai
import os
import Config

load_dotenv()

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)

def board_to_fen(board):
    piece_map = {
        "Pawn": "p",
        "Knight": "n",
        "Bishop": "b",
        "Rook": "r",
        "Queen": "q",
        "King": "k"
    }

    fen_rows = []

    for row in board:
        fen_row = ""
        empty_count = 0

        for piece in row:
            piece_type = type(piece).__name__

            if piece_type == "Empty":
                empty_count += 1
                continue

            if empty_count:
                fen_row += str(empty_count)
                empty_count = 0

            symbol = piece_map[piece_type]

            if piece.is_white:
                symbol = symbol.upper()

            fen_row += symbol

        if empty_count:
            fen_row += str(empty_count)

        fen_rows.append(fen_row)
    return f"{'/'.join(fen_rows)} b - - 0 1"


def getMove(board) -> str:
    queryString = board_to_fen(board)

    try:
        response = client.models.generate_content(
            model=Config.GEMINI_MODEL,
            contents=queryString,
            config=genai.types.GenerateContentConfig(
                system_instruction=Config.SYSTEM_PROMPT
            )
        )

        return response.text.strip()

    except Exception as e:
        return ""
