# ml/ml_service.py
import os
import base64
import json
import logging
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

# import your modules
import stt_streaming   # this is your file that uses VOSK (uploaded). :contentReference[oaicite:12]{index=12}
import scoring_model   # uploaded scoring model. :contentReference[oaicite:13]{index=13}
import emotion_model   # uploaded emotion model. :contentReference[oaicite:14]{index=14}
import question_generator  # uploaded. :contentReference[oaicite:15]{index=15}

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("ml_service")

app = FastAPI()

class STTReq(BaseModel):
    audio_b64: str  # base64 wav or raw pcm bytes

class STTResp(BaseModel):
    text: str

@app.post("/stt", response_model=STTResp)
def stt_endpoint(req: STTReq):
    # stt_streaming.transcribe_chunk expects base64 of PCM16 (int16) bytes
    try:
        # simply forward to stt_streaming.transcribe_chunk
        # if stt_streaming expects PCM raw bytes encoded in base64, we're good.
        return stt_streaming.transcribe_chunk(session_id="local", chunk_b64=req.audio_b64)
    except Exception as e:
        logger.exception("STT failed")
        raise HTTPException(status_code=500, detail="STT error")

class ScoreReq(BaseModel):
    question: str
    answer: str
    expected_keywords: list = None

@app.post("/score")
def score_endpoint(payload: ScoreReq):
    scores = scoring_model.score_answer(payload.question, payload.answer, payload.expected_keywords)
    return scores

class ExprReq(BaseModel):
    image_b64: str

@app.post("/expression")
def expression_endpoint(payload: ExprReq):
    try:
        res = emotion_model.analyze_emotion_from_b64(payload.image_b64)
        return res
    except Exception as e:
        logger.exception("Expression failed")
        raise HTTPException(status_code=500, detail="Expression error")

class QGenReq(BaseModel):
    role: str
    difficulty: str = "easy"

@app.post("/generate_question")
def generate_question(payload: QGenReq):
    q = question_generator.generate_question(payload.role, payload.difficulty)
    return {"question": q}
