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
