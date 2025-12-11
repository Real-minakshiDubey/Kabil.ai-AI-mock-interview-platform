from ml.question_generator import generate_question
from ml.scoring_model import score_answer
from ml.emotion_model import analyze_emotion_from_b64
from ml.stt_streaming import transcribe_chunk


class InterviewPipeline:

    def __init__(self):
        print("Pipeline initialized!")

    # ---------------------------
    # 1. Generate Question
    # ---------------------------
    def generate_question(self, role: str, difficulty: str):
        return generate_question(role, difficulty)

    # ---------------------------
    # 2. Score Answer
    # ---------------------------
    def score_answer(self, question: str, answer: str, expected_keywords=None):
        return score_answer(question, answer, expected_keywords)

    # ---------------------------
    # 3. Emotion Analysis
    # ---------------------------
    def analyze_emotion(self, image_b64: str):
        return analyze_emotion_from_b64(image_b64)

    # ---------------------------
    # 4. Speech-to-Text Chunk
    # ---------------------------
    def transcribe_audio_chunk(self, session_id: str, chunk_b64: str):
        return transcribe_chunk(session_id, chunk_b64)
