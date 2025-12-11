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
               ┌──────────────────────────────┐
               │      FRONTEND (React)        │
               │──────────────────────────────│
               │ • Sends audio (1s chunks)    │
               │ • Sends video frames (200ms) │
               │ • Displays transcript        │
               │ • Shows live metrics         │
               └───────────────┬──────────────┘
                               │ WebSocket
                               ▼
       ┌────────────────────────────────────────────────┐
       │                BACKEND (FastAPI)               │
       │────────────────────────────────────────────────│
       │ • WS: /ws/stt/{session_id}                    │
       │ • WS: /ws/video/{session_id}                  │
       │ • REST: /start, /qa, /finalize                │
       │ • Sends audio/video to ML services            │
       │ • Stores transcripts & scores in DB           │
       └───────────────┬──────────────────────────────┘
                       │ HTTP
                       ▼
       ┌────────────────────────────────────────────────┐
       │               ML MICROSERVICES                │
       │────────────────────────────────────────────────│
       │ • /stt → Speech-to-Text (Whisper)             │
       │ • /expression → Video metrics                 │
       │ • /score → Combined scoring engine            │
       │ • LLM-based question generation               │
       └───────────────┬──────────────────────────────┘
                       │
                       ▼
       ┌────────────────────────────────────────────────┐
       │                DATABASE (PostgreSQL)           │
       │────────────────────────────────────────────────│
       │ • interview_sessions                           │
       │ • interview_qa                                 │
       │ • transcripts                                  │
       │ • video_scores (JSONB)                         │
       │ • final_reports                                │
       └────────────────────────────────────────────────┘


4-Week Development Roadmap
Week 1 — Setup, Architecture & Backend Scaffolding
ML (Mini)

Define full AI pipeline (audio + video)

Define metrics: confidence, posture, eye_contact, engagement

Choose models: Whisper, MediaPipe/Facemesh, LLM

Backend (Suvi)

Setup FastAPI structure

Create base endpoints

Setup PostgreSQL models

Database (Sonali)

ER diagram creation

Schema:

users

interview_sessions

transcripts

video_scores (JSONB)

final_reports

Frontend (Tanishka)

Build UI screens

Setup role selection & interview layout structure

Week 2 — AI Model Integration & Backend API Development
ML (Mini)

Video ML models:

Face detection

Eye-contact detection

Emotion analysis

Mouth movement → fluency

Produce metrics every 2 seconds

Build scoring logic combining audio + video

Backend (Suvi)

Connect ML endpoints: /stt, /expression, /score

Create interview workflow

Database (Sonali)

Test DB integrations

Validate schema for ML metrics

Frontend (Tanishka)

Implement camera + microphone access

Send audio via WebSocket

Show real-time transcripts

Week 3 — Full Frontend ↔ Backend ↔ ML Integration
Frontend

Send video frames every 200–300ms

Add live evaluation indicators

Build results dashboard (graphs + score cards)

Backend



Database Schema (Summary)
Table	Purpose
interview_sessions	Session metadata
interview_qa	Question + transcript + partial scores
transcripts	STT results
video_scores	Metrics from video frames
final_reports	Final multi-modal 
               │      FRONTEND (React)        │
               │──────────────────────────────│
               │ • Sends audio (1s chunks)    │
               │ • Sends video frames (200ms) │
               │ • Displays transcript        │
               │ • Shows live metrics         │
               └───────────────┬──────────────┘
                               │ WebSocket
                               ▼
       ┌────────────────────────────────────────────────┐
       │                BACKEND (FastAPI)               │
       │────────────────────────────────────────────────│
       │ • WS: /ws/stt/{session_id}                    │
       │ • WS: /ws/video/{session_id}                  │
       │ • REST: /start, /qa, /finalize                │
       │ • Sends audio/video to ML services            │
       │ • Stores transcripts & scores in DB           │
       └───────────────┬──────────────────────────────┘
                       │ HTTP
                       ▼
       ┌────────────────────────────────────────────────┐
       │               ML MICROSERVICES                │
       │────────────────────────────────────────────────│
       │ • /stt → Speech-to-Text (Whisper)             │
       │ • /expression → Video metrics                 │
       │ • /score → Combined scoring engine            │
       │ • LLM-based question generation               │
       └───────────────┬──────────────────────────────┘
                       │
                       ▼
       ┌────────────────────────────────────────────────┐
       │                DATABASE (PostgreSQL)           │
       │────────────────────────────────────────────────│
       │ • interview_sessions                           │
       │ • interview_qa                                 │
       │ • transcripts                                  │
       │ • video_scores (JSONB)                         │
       │ • final_reports                                │
       └────────────────────────────────────────────────┘

4-Week Development Roadmap
(Official Milestone Format)
Week 1 — Setup, Architecture & Backend Scaffolding
### ML (Mini)

Define complete AI pipeline (audio + video)

Define metrics: confidence, posture, eye_contact, engagement

Choose Whisper, MediaPipe/Facemesh, LLM models

### Backend (Suvi)

Initialize FastAPI backend

Create base endpoints (/start, /qa, /finalize)

Setup PostgreSQL + ORM models

### Database (Sonali)

Create database schema:

users

interview_sessions

transcripts

video_scores (JSONB)

final_reports

ER diagram + migrations

### Frontend (Tanishka)

Setup project structure

Create Home, Role Selection, Interview layout

Week 2 — AI Model Integration & Core API Development
### ML (Mini)

Implement video ML models:

Face detection

Eye-contact estimation

Emotion recognition

Mouth movement → fluency metrics

Generate metrics every 2 seconds

Build scoring engine (audio + video fusion)

### Backend m

Integrate ML endpoints: /stt, /expression, /score

Develop interview flow controller

### Database

Write & validate DB operations

Test metric storage and queries

### Frontend 

Implement camera & microphone access

Add WebSocket audio streaming

Show real-time transcripts

Week 3 — Full System Integration
### Frontend

Send video frames (200–300ms)

Display live metrics & transcript

Build results dashboard (charts + score cards)

### Backend

Complete multi-question workflow

Improve WebSocket performance

Implement next-question logic

### ML

Optimize FPS (~3 fps) for video scoring

Generate combined scoring JSON:

{
  "scores": {
    "confidence": 7.5,
    "communication": 8.0,
    "fluency": 7.0,
    "eye_contact": 8.0,
    "posture": 6.5
  },
  "feedback": "Good clarity; improve posture.",
  "improvement_plan": [
    "Practice posture alignment",
    "Reduce filler words",
    "Maintain consistent eye contact"
  ]
}



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

## Conclusion

Kabil.AI provides a functioning multimodal mock interview platform with speech + vision analysis, question generation, and personalized feedback.
This system satisfies the Round-2 requirements and prepares the foundation for Round-3 enhancements.


