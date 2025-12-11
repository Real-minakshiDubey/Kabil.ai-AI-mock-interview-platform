# 🚀 Kabil.ai — AI Mock Interview Platform

An end-to-end AI-powered mock interview system that evaluates users on communication skills, technical responses, and emotional tone using Speech-to-Text, NLP scoring models, and Emotion Analysis, with a React.js front-end and FastAPI backend.

This project is built as part of GUVI – IIT Bombay AI Hackathon (2025).

## 📌 🔹 Key Features

Real-time AI Speech-to-Text (STT) using Vosk + WebSockets

AI Question Generator (easy/medium/hard levels)

AI Answer Scoring Model using Sentence Transformers

Emotion Detection using PyTorch model

Live Camera & Audio Streaming (frontend → backend)

Smart interview dashboard

Interview report generation

## 📁 Project Structure
kabil-ai-interview/
│
├── backend/
│   ├── ws_stt_fastapi.py
│   ├── models.py
│   ├── db.py
│   ├── config.py
│   ├── requirements.txt
│
├── ml/
│   ├── ml_service.py
│   ├── scoring_model.py
│   ├── stt_streaming.py
│   ├── emotion_model.py
│   ├── question_generator.py
│   ├── requirements.txt
│
├── frontend/
│   ├── src/
│   ├── package.json
│   ├── .env
│
└── README.md  


## 🔧 Installation Instructions
## 1️⃣ Clone Repo
git clone https://github.com/<your-username>/Kabil.ai-AI-mock-interview-platform.git
cd Kabil.ai-AI-mock-interview-platform

## 2️⃣ Backend Setup (FastAPI)
Create Virtual Environment
cd backend
python -m venv backend_env
backend_env\Scripts\activate

Install Requirements
pip install -r requirements.txt

Run Backend
uvicorn ws_stt_fastapi:app --host 0.0.0.0 --port 8000 --reload


Backend will run at:

http://127.0.0.1:8000

## 3️⃣ ML Service Setup
Create environment
cd ml
python -m venv ml_env
ml_env\Scripts\activate

Install ML dependencies
pip install -r ml_requirements.txt

Run ML server
uvicorn ml_service:app --host 127.0.0.1 --port 8601 --reload


ML Service runs at:

http://127.0.0.1:8601

## 4️⃣ Frontend Setup (React + Vite)
cd frontend
npm install
npm run dev


Frontend runs at:

http://localhost:5173

## 🌐 API Endpoints
Start Interview Session
POST /api/session/start


Request:

{ "role": "ml_engineer" }

Speech-to-Text (WebSocket)
ws://127.0.0.1:8000/ws/stt/{session_id}

Score User Answer
POST /score


Example:

{
  "question": "What is Python?",
  "answer": "Python is a programming language.",
  "expected_keywords": ["programming", "language"]
}

## 📥 Model Downloads

Large models ARE NOT included in GitHub due to the 25MB limit.

Download Vosk Model (small model recommended):
https://alphacephei.com/vosk/models

Place inside:

/vosk_model/

## 📘 Architecture Overview
Frontend (React)
│
│-- camera + microphone → WebSocket → Backend
│
Backend (FastAPI)
│-- Real-time STT using Vosk
│-- Sends transcript → ML Service
│
ML Service
│-- scoring_model.py → NLP similarity + keywords
│-- emotion_model.py → emotion prediction
│-- question_generator.py → generate next question

## 🧠 AI Models Used
1. SentenceTransformer (all-MiniLM-L6-v2)

Used for semantic similarity scoring.

2. Vosk Speech Recognition

Offline STT engine with low latency.

3. Custom emotion_classifier.pt

PyTorch-based emotion classification model.

📝 Example Output
{
  "overall": 57.17,
  "breakdown": {
    "relevance": 41.12,
    "keywords": 100.0,
    "length": 25.0
  },
  "comments": ["Good use of expected keywords.", "Try to expand your answer."]
}

## 👨‍💻 Contributors

**Minakshi Dubey– Lead ML

Tanishka Gour – Frontend

Suvidha vishwakarma – Backend

Sonali Kumari - design, database**

## 3-Week Implementation Plan
**Week 1 — Setup, Architecture & Backend Foundation**

-ML

Define full voice + video AI pipeline

Select models: Whisper, MediaPipe/Facemesh, LLM

Define metrics: confidence, eye_contact, posture, engagement

-Backend

Create FastAPI project + routing

Setup WebSockets for audio & video

Design REST APIs for interview workflow

-Database 

Schema creation: sessions, Q/A, transcripts, video_scores, reports

ER diagram + migrations

-Frontend 

Setup React project

Build Home, Role Selection, Interview layout

**Week 2 — Core AI Integration & Workflow Development**

-ML 

Implement video models: face detection, emotion, eye contact

Generate metrics every 2 seconds

Build scoring engine (audio + video fusion)

-Backend 

Integrate ML services: /stt, /expression, /score

Implement multi-question flow logic

-Database 

Test DB operations

Verify metric storage

-Frontend 

Add camera + mic access

Stream audio via WebSocket

Display real-time transcripts

**Week 3 — Complete Integration, Testing & Refinement**

-Frontend

Send video frames every 200–300ms

Add live evaluation indicators

Build results dashboard (scores, graphs, improvements)

-Backend

Complete end-to-end interview workflow

Performance optimization for WS streams

Error handling + retry logic

-ML

Combine all metrics into final scoring JSON

Improve feedback quality using LLM

Database

Validate multi-question flows

Optimize JSONB queries

## 🏆 Status

✔ Prototype Completed
✔ Real-time STT working
✔ ML scoring model working
✔ Frontend integrated
⬜ Deployment (optional)

📄 MIT License

This project is open-source under the MIT license.

✅ 2. /models/README.md (Include This in Models Folder)
# Models Folder

This folder contains instructions for downloading the large AI models.

GitHub does not support files over 25MB, so model files are not stored here.

---

## 1. Download Vosk Model
Recommended model (Small):
https://alphacephei.com/vosk/models

Extract and place inside:

/vosk_model/

