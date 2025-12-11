import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

ML_SERVER = os.getenv("ML_SERVER", "http://127.0.0.1:8601")

BACKEND_HOST = os.getenv("BACKEND_HOST", "0.0.0.0")
BACKEND_PORT = int(os.getenv("BACKEND_PORT", "8000"))

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql+psycopg2://postgres:kabil@localhost:5432/mock_interview_db")

VOSK_MODEL_PATH = os.getenv("VOSK_MODEL_PATH", "")
