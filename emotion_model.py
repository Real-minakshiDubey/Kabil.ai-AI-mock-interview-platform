# lightweight emotion_model.py (no torch)
import base64
import numpy as np

# dummy lightweight emotion classifier (you can improve later)
def predict_emotion(image_b64: str):
    # return fixed label for now
    return {
        "emotion": "neutral",
        "confidence": 0.85
    }
