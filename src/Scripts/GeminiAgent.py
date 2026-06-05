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
    return f"{'/'.join(fen_rows)}"


def getMove(board) -> str:
    queryString = board_to_fen(board)
    print(queryString)
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
        print(e)
        return ""

# response = client.models.generate_content(
#     model=Config.GEMINI_MODEL,
#     contents="I need you to respond with a VALID chess move to make when the board looks like this (B before name means Black, W before name means White):" \
#     "BPawn BPawn BPawn Empty Empty Empty Empty Empty" \
#     "Empty Empty Empty Empty Empty Empty Empty Empty" \
#     "Empty Empty Empty Empty Empty Empty Empty Empty" \
#     "Empty Empty Empty Empty Empty Empty Empty Empty" \
#     "Empty Empty Empty Empty Empty Empty Empty Empty" \
#     "Empty Empty Empty Empty Empty Empty Empty Empty" \
#     "Empty Empty Empty Empty Empty Empty Empty Empty" \
#     "WPawn WPawn WPawn Empty Empty Empty Empty Empty" \
#     "Respond with the row and column of the piece you want to move, and then the row and column it should move to (in coordinate pairs, where (0,0) is the top left corner and (7,7) is the bottom right corner), and nothing else (You are White)."
# )
