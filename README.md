# Kabil.AI — AI Mock Interview Platform
Team Gen Z | HCL–GUVI Upskill India Challenge
Overview

Kabil.AI is an AI-powered mock interview system that analyzes audio + video in real time to evaluate communication skills, confidence, posture, eye contact, and fluency.
LLM-based evaluation provides personalized feedback and an improvement plan.

## 🚀 Team Members
- **Minakshi Dubey** – ML Lead  
- **Suvidha Vishwakarma** – Backend  
- **Tanishka Gour** – Frontend  
- **Sonali Kumari** – Design and Database 

---

# 📁 Project Structure

kabil_ai/
│
├── backend/
│   ├── backend_env/              
│   ├── __pycache__/
│   ├── config.py
│   ├── create_tables.py
│   ├── db.py
│   ├── models.py
│   ├── ws_stt_fastapi.py         
│   ├── requirements.txt
│   └── (NO ML FILES HERE)
│
├── frontend/
│   ├── node_modules/
│   ├── public/
│   │   ├── logo.png
│   │   ├── mic.svg
│   │   └── wave.svg
│   ├── src/
│   │   ├── assets/
│   │   ├── components/
│   │   │   ├── Bubble.jsx
│   │   │   ├── Card.jsx
│   │   │   ├── MicButton.jsx
│   │   │   └── Nav.jsx
│   │   ├── pages/
│   │   │   ├── Interview.jsx      
│   │   ├── styles/
│   │   ├── api.js                 
│   │   ├── config.js
│   │   ├── App.jsx
│   │   ├── App.css
│   │   ├── index.css
│   │   └── main.jsx
│   │
│   ├── .env.local                 
│   │       VITE_BACKEND_WS=ws://127.0.0.1:8000/ws/stt
│   │       VITE_BACKEND_API=http://127.0.0.1:8000/api
│   │
│   ├── package.json
│   ├── vite.config.js
│   └── index.html
│
├── ml/
│   ├── ml_env/                    
│   ├── __pycache__/
│   ├── emotion_model.py
│   ├── scoring_model.py
│   ├── question_generator.py
│   ├── stt_streaming.py           
│   ├── ml_service.py              
│   ├── requirements.txt
│   ├── ml_workspace/              
│   ├── vosk_model/                
│   └── test_emotion.py
│
└── ws_test.html                   





## Features

Real-time speech-to-text (Whisper)

Live video evaluation (eye contact, posture, emotion)

LLM-based question generation & scoring

Final report with improvement plan

FastAPI backend + PostgreSQL database

React frontend with camera & mic streaming

## System Architecture
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
       │ • WS: /ws/stt/{session_id}                     │
       │ • WS: /ws/video/{session_id}                   │
       │ • REST: /start, /qa, /finalize                 │
       │ • Sends audio/video to ML services             │
       │ • Stores transcripts & scores in DB            │
       └───────────────┬─────────────────────────── ─── ┘
                       │ HTTP
                       ▼
       ┌────────────────────────────────────────────────┐
       │               ML MICROSERVICES                 │
       │────────────────────────────────────────────────│
       │ • /stt → Speech-to-Text (Whisper)              │
       │ • /expression → Video metrics                  │
       │ • /score → Combined scoring engine             │
       │ • LLM-based question generation                │
       └───────────────┬─────────────────────────────  ─┘
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



## Development Plan
**Week 1 — Setup**

Project architecture, DB schema, FastAPI base setup

Frontend layout & ML pipeline definition

**Week 2 — Core Integration**

Implement STT, video metrics (eye contact, posture)

Backend routing & state management

Frontend audio + camera streaming

**Week 3 — Full Workflow**

Multi-question flow

Combined scoring (audio + video + LLM)

Results dashboard

**Week 4 — Refinement**

UI polish, error handling

Performance optimization

Documentation & testing
## 3-Week Implementation Plan
**Week 1 — Setup, Architecture & Backend Foundation**
**ML**

Define full voice + video AI pipeline

Select models: Whisper, MediaPipe/Facemesh, LLM

Define metrics: confidence, eye_contact, posture, engagement

**Backend**

Create FastAPI project + routing

Setup WebSockets for audio & video

Design REST APIs for interview workflow

**Database**

Schema creation: sessions, Q/A, transcripts, video_scores, reports

ER diagram + migrations

Frontend (Tanishka)

Setup React project

Build Home, Role Selection, Interview layout

**Week 2 — Core AI Integration & Workflow Development**
**ML**

Implement video models: face detection, emotion, eye contact

Generate metrics every 2 seconds

Build scoring engine (audio + video fusion)

**Backend**

Integrate ML services: /stt, /expression, /score

Implement multi-question flow logic

Database (Sonali)

Test DB operations

Verify metric storage

**Frontend**

Add camera + mic access

Stream audio via WebSocket

Display real-time transcripts

**Week 3 — Complete Integration, Testing & Refinement**
**Frontend**

Send video frames every 200–300ms

Add live evaluation indicators

Build results dashboard (scores, graphs, improvements)

**Backend**

Complete end-to-end interview workflow

Performance optimization for WS streams

Error handling + retry logic

**ML**

Combine all metrics into final scoring JSON

Improve feedback quality using LLM

Database

Validate multi-question flows

Optimize JSONB queries
## Main APIs
POST /api/session/start
WS   /ws/stt/{session_id}
WS   /ws/video/{session_id}
POST /api/session/{id}/qa
POST /api/session/{id}/finalize

## Conclusion

Kabil.AI delivers a working multimodal mock interview platform with real-time evaluation and AI-driven scoring, meeting the Round-2 prototype requirements.
