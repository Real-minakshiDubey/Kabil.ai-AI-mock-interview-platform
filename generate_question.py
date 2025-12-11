# ml_workflow/generate_question.py

from ml.question_generator import next_question
from .utils import normalize_text

def get_next_question(prev_answer: str, role: str, difficulty: str):
    cleaned = normalize_text(prev_answer)
    q = next_question(cleaned, role, difficulty)
    return {"next_question": q}
