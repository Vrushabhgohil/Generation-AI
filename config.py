import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Database URL
DATABASE_URL = os.getenv("DATABASE_URL", "").strip()

if not DATABASE_URL:
    raise ValueError("DATABASE_URL is not set or is empty! Check your .env file.")

# Authentication & Security
SECRET_KEY = os.getenv("SECRET_KEY", "default_secret_key")
ALGORITHM = os.getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30))
