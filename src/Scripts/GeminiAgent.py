from dotenv import load_dotenv
from google import genai
import os

load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")
print(API_KEY)

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)

response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents="I need you to respond with a VALID chess move to make when the board looks like this (B before name means Black, W before name means White):" \
    "BPawn BPawn BPawn Empty Empty Empty Empty Empty" \
    "Empty Empty Empty Empty Empty Empty Empty Empty" \
    "Empty Empty Empty Empty Empty Empty Empty Empty" \
    "Empty Empty Empty Empty Empty Empty Empty Empty" \
    "Empty Empty Empty Empty Empty Empty Empty Empty" \
    "Empty Empty Empty Empty Empty Empty Empty Empty" \
    "Empty Empty Empty Empty Empty Empty Empty Empty" \
    "WPawn WPawn WPawn Empty Empty Empty Empty Empty" \
    "Respond with the row and column of the piece you want to move, and then the row and column it should move to (in coordinate pairs, where (0,0) is the top left corner and (7,7) is the bottom right corner), and nothing else (You are White)."
)

print(response.text)
