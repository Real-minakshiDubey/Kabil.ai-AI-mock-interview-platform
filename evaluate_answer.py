# ml_workflow/evaluate_answer.py

from ml.scoring_model import score_answer
from ml.emotion_model import analyze_emotion_from_b64

def evaluate_interview_answer(question, answer, keywords, emotion_b64=None):
    
    # Scoring
    scoring = score_answer(question, answer, keywords)

    # Emotion (optional)
    emotion_result = None
    if emotion_b64:
        emotion_result = analyze_emotion_from_b64(emotion_b64)

    return {
        "scores": scoring,
        "emotion": emotion_result
    }
