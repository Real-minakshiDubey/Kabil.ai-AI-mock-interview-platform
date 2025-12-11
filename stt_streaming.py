# ml/stt_streaming.py

import base64
import json
import os
import numpy as np
from vosk import Model, KaldiRecognizer

# Correct Vosk model path
MODEL_PATH = r"C:\Users\pcc\OneDrive\Desktop\shivaay\vosk_model"

if not os.path.exists(MODEL_PATH):
    raise FileNotFoundError(f"Vosk model folder not found at: {MODEL_PATH}")

model = Model(MODEL_PATH)

def transcribe_chunk(session_id: str, chunk_b64: str):
    """
    Takes base64 PCM 16kHz audio & returns partial transcript using Vosk.
    """

    audio_bytes = base64.b64decode(chunk_b64)
    audio_np = np.frombuffer(audio_bytes, dtype=np.int16)

    rec = KaldiRecognizer(model, 16000)

    if rec.AcceptWaveform(audio_np.tobytes()):
        result = json.loads(rec.Result())
        text = result.get("text", "")
    else:
        partial = json.loads(rec.PartialResult())
        text = partial.get("partial", "")

    return {"partial_transcript": text}

