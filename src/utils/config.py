import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY")

    if not GEMINI_API_KEY or GEMINI_API_KEY == "my_key":
        raise ValueError("CRITICAL ERROR: GEMINI_API_KEY is not set correctly in the .env file!")