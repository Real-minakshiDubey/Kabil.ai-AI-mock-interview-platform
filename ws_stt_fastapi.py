# backend/ws_stt_fastapi.py

import base64
import json
import logging
import asyncio
import traceback
from datetime import datetime
from typing import List, Optional

import requests
from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from sqlalchemy.orm import Session

from db import get_db
from models import InterviewSession, InterviewQA, InterviewReport
from config import ML_SERVER   # <-- ensure ML_SERVER env/url is correct

# --------------------------------------------------------------------
# Logging
# --------------------------------------------------------------------
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("ws_stt")

# --------------------------------------------------------------------
# FastAPI App
# --------------------------------------------------------------------
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],   # dev mode
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --------------------------------------------------------------------
# Pydantic Models
# --------------------------------------------------------------------
class StartSessionReq(BaseModel):
    user_id: Optional[str] = None
    role: str
    difficulty: Optional[str] = "easy"


class StartSessionResp(BaseModel):
    session_id: str
    role: str
    difficulty: str


class QAItemReq(BaseModel):
    question_text: str
    answer_transcript: str
    partial_score: dict
    expected_keywords: Optional[List[str]] = None
    is_followup: bool = False


class FinalizeReq(BaseModel):
    avg_scores: dict
    improvement_plan: dict
    recommended_resources: List[dict]


class FinalizeResp(BaseModel):
    report_id: str
    overall_score: float


class ExpressionReq(BaseModel):
    image_b64: str


# --------------------------------------------------------------------
# 1. START SESSION
# --------------------------------------------------------------------
@app.post("/api/session/start", response_model=StartSessionResp)
def start_session(payload: StartSessionReq, db: Session = Depends(get_db)):

    session = InterviewSession(
        user_id=payload.user_id,
        role=payload.role,
        difficulty=payload.difficulty,
        started_at=datetime.utcnow(),
    )

    db.add(session)
    db.commit()
    db.refresh(session)

    return StartSessionResp(
        session_id=str(session.session_id),
        role=session.role,
        difficulty=session.difficulty,
    )


# --------------------------------------------------------------------
# 2. ADD QA
# --------------------------------------------------------------------
@app.post("/api/session/{session_id}/qa")
def add_qa(session_id: str, payload: QAItemReq, db: Session = Depends(get_db)):

    session = db.query(InterviewSession).filter(
        InterviewSession.session_id == session_id
    ).first()

    if not session:
        raise HTTPException(status_code=404, detail="Session not found")

    qa = InterviewQA(
        session_id=session.session_id,
        question_text=payload.question_text,
        answer_transcript=payload.answer_transcript,
        partial_score=payload.partial_score,
        expected_keywords=payload.expected_keywords,
        is_followup=payload.is_followup,
    )

    db.add(qa)
    db.commit()
    db.refresh(qa)

    return {"qa_id": qa.qa_id}


# --------------------------------------------------------------------
# 3. FINALIZE SESSION
# --------------------------------------------------------------------
@app.post("/api/session/{session_id}/finalize", response_model=FinalizeResp)
def finalize_session(session_id: str, payload: FinalizeReq, db: Session = Depends(get_db)):

    session = db.query(InterviewSession).filter(
        InterviewSession.session_id == session_id
    ).first()

    if not session:
        raise HTTPException(status_code=404, detail="Session not found")

    scores = payload.avg_scores

    overall_score = float(
        (
            scores.get("communication", 0)
            + scores.get("technical", 0)
            + scores.get("confidence", 0)
        ) / 3.0
    )

    session.overall_score = overall_score
    session.ended_at = datetime.utcnow()
    db.add(session)

    report = InterviewReport(
        session_id=session.session_id,
        avg_scores=payload.avg_scores,
        improvement_plan=payload.improvement_plan,
        recommended_resources=payload.recommended_resources,
    )

    db.add(report)
    db.commit()
    db.refresh(report)

    return FinalizeResp(
        report_id=str(report.report_id),
        overall_score=overall_score,
    )


# --------------------------------------------------------------------
# 4. EXPRESSION ANALYSIS — FORWARDED TO ML SERVER
# --------------------------------------------------------------------
@app.post("/api/session/{session_id}/expression")
def analyze_expression(session_id: str, payload: ExpressionReq):

    resp = requests.post(
        f"{ML_SERVER}/expression",
        json={"image_b64": payload.image_b64},
        timeout=30
    )

    return resp.json()


# --------------------------------------------------------------------
# 5. WEBSOCKET — STREAMING STT VIA ML SERVER
# --------------------------------------------------------------------
@app.websocket("/ws/stt/{session_id}")
async def ws_stt(websocket: WebSocket, session_id: str):

    await websocket.accept()
    logger.info(f"WS connected session={session_id}")

    try:
        while True:

            raw = await websocket.receive_text()
            data = json.loads(raw)

            if data.get("type") == "audio_chunk":

                blob_b64 = data.get("chunk_b64", "")
                seq = data.get("seq", 0)

                try:
                    # decode and forward to ML STT endpoint
                    blob_bytes = base64.b64decode(blob_b64)
                except Exception:
                    logger.exception("Failed to decode base64 chunk")
                    blob_bytes = b""

                try:
                    resp = requests.post(
                        f"{ML_SERVER}/stt",
                        json={"audio_b64": blob_b64},
                        timeout=30
                    )
                    transcript = resp.json().get("text", "")
                except Exception:
                    logger.exception("Error calling ML STT")
                    transcript = ""

                await websocket.send_text(json.dumps({
                    "type": "transcript_partial",
                    "seq": seq,
                    "text": transcript
                }))

            elif data.get("type") == "end_interview":

                await websocket.send_text(json.dumps({
                    "type": "transcript_final",
                    "text": "Interview ended"
                }))
                break

    except WebSocketDisconnect:
        logger.info("WS disconnected")
    except Exception:
        logger.error("Unhandled WS error")
        logger.error(traceback.format_exc())
        try:
            await websocket.close()
        except Exception:
            pass
