# AI_AGENT_Phase_4 — FastAPI Backend Core

Phase 4 of PROJECT-F  
A high-performance FastAPI backend that powers an AI agent with real-time responses, memory, TTS, and OS-level command execution.

---

## Overview

This repository contains the backend engine of the AI system.

It acts as the central brain connector between:
- Frontend UI (graphic_ai)
- AI Brain (Groq-based LLM)
- Memory System
- OS Command Layer
- Text-to-Speech Engine

Built with a procedural architecture (no OOP, no Pydantic) for:
- Maximum control
- Minimal overhead
- High flexibility

---

## Core Responsibilities

- FastAPI server initialization
- API route management
- AI response generation (Groq)
- Conversation memory handling
- Text-to-Speech (TTS)
- Language detection
- Streaming responses (token-by-token)
- OS command execution pipeline
- Serving frontend UI

## Folder Structure

PROJECT-F/
└── api_server/
    ├── main.py        # Entry point of FastAPI server
    ├── routes.py      # All API endpoints
    ├── schemas.py     # Validation & response builders (procedural)

---

## API Architecture

### Base URL
/api

---

## Endpoints

### 1. Message Processing
POST /api/message

Description:
- Processes user input
- Detects language
- Executes OS command (if applicable)
- Falls back to AI response
- Returns structured output

Flow:
User Input → Validation → Language Detection → OS Command Check → AI Response → Memory Fetch → Response

---

### 2. Streaming AI Response
POST /api/stream

Description:
- Streams AI response token-by-token
- Real-time response system

---

### 3. Text-to-Speech
GET /api/tts?text=your_text

Description:
- Converts text into audio file
- Automatically deletes file after response

---

### 4. Memory Retrieval
GET /api/memory

Description:
- Returns stored conversation history

---

### 5. System Status
GET /api/status

Returns:
- Model name
- Max memory size
- Temperature setting

---

## Architecture Design

### 1. Procedural Schema System (No Pydantic)

Instead of models:
- Manual validation functions
- Lightweight and faster execution

Functions:
- validate_message_request()
- create_message_response()
- create_memory_response()
- create_status_response()

---

### 2. Hybrid Intelligence Layer

Flow:
User Input
   ↓
OS Command Processor
   ↓ (if fails)
AI Brain (Groq)

This ensures:
- Real command execution priority
- Reduced AI hallucination
- Practical system behavior

---

### 3. Memory System

- Stores conversation history
- Controlled using MAX_MEMORY
- Accessible via API

---

### 4. Streaming Engine

Implementation:
StreamingResponse(token_generator())

- Token-by-token response delivery
- Real-time interaction capability

---

### 5. Frontend Integration

Implementation:
app.mount("/", StaticFiles(...))

- Serves frontend directly from backend
- No separate deployment required

---

## Code Breakdown

### main.py

Role:
- Entry point of the application

Responsibilities:
- Create FastAPI instance
- Register API routes with prefix "/api"
- Resolve frontend path
- Serve static frontend using StaticFiles

---

### routes.py

Role:
- API controller layer

Handles:
- Text-to-Speech generation
- AI message processing
- Streaming responses
- Memory retrieval
- System status reporting
- OS command execution

Core Logic:
os_result = process_command(user_text)

if os_result["status"] == "success":
    ai_response = os_result.get("output", "Command executed")
else:
    ai_response = generate_ai_response(user_text)

---

### schemas.py

Role:
- Validation and response construction layer

Replaces:
- Pydantic models

Features:
- Manual type validation
- Error handling
- Standardized API responses

Key Functions:
- _ensure_type()
- validate_message_request()
- create_message_response()
- create_memory_response()
- create_status_response()

---

## Key Features

- Lightweight architecture without heavy schema frameworks
- Hybrid AI and OS execution system
- Real-time streaming responses
- Built-in TTS with automatic cleanup
- Language detection support
- Modular and scalable design
- Backend-served frontend
- Persistent conversation memory

---

## Tech Stack

- FastAPI — Backend framework
- Groq API — LLM inference
- LangDetect — Language detection
- Starlette — Background tasks and streaming
- Custom OS Layer — Command execution
- Custom Memory Engine

---

## Error Handling Strategy

- Try/except blocks in critical routes
- JSON-based error responses
- Prevents server crashes
- Background cleanup tasks for file handling

---

