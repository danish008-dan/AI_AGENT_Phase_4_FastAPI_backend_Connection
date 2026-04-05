"""
File: api_server/routes.py

Purpose:
This file defines all backend API routes used by the AI system.

The routes handle:
1. Text-to-Speech generation
2. AI message processing
3. Conversation memory retrieval
4. System status reporting
5. Streaming AI responses (token-by-token)

Architecture Role:
This file acts as the main API controller layer that connects the
frontend UI with the backend AI brain modules.

Important Notes:
- The architecture is procedural (no OOP and no Pydantic models).
- Manual validation functions are used instead of schemas.
- AI responses are generated using the Groq client.
- Conversation memory is stored and retrieved from the memory module.
"""

# Import APIRouter to define grouped API routes
# Import Request to access raw incoming HTTP request data
from fastapi import APIRouter, Request


# Import procedural validation and response builder functions
# These replace traditional Pydantic request/response schemas
from api_server.api_schemas import (
    validate_message_request,   # Validates incoming message payload
    create_message_response,    # Creates formatted AI message response
    create_memory_response,     # Creates formatted memory response
    create_status_response      # Creates formatted system status response
)


# Import AI response generation function from the brain module
# This function communicates with the Groq model
from phase_two.brain.groq_client import generate_ai_response


# Import conversation memory utilities
from phase_two.memory.conversation_memory import (
    get_memory,   # Returns stored conversation history
    MAX_MEMORY    # Maximum allowed memory size
)


# Import AI configuration settings
from phase_two.config.settings import (
    MODEL_NAME,   # Name of the AI model being used
    TEMPERATURE   # Sampling temperature for AI responses
)


# Import language detection library
# Used to detect the language of the user message
from langdetect import detect


# Import FileResponse to return files (audio files for TTS)
from fastapi.responses import FileResponse


# Import function that converts text into audio
from phase_one.modules.text_to_audio import convert_text_to_audio


# Import OS module for file handling operations
import os


# Import BackgroundTask to run cleanup tasks after a response is sent
from starlette.background import BackgroundTask


# Import StreamingResponse to stream AI tokens in real time
from fastapi.responses import StreamingResponse, FileResponse, JSONResponse


# Import streaming AI response generator
from phase_two.brain.groq_client import generate_ai_response_stream

from os_layer.os_controller import router as os_router

# Import JSON module (used when formatting streaming data if needed)
import json
from os_layer.core.os_pipeline import process_command

# Create router instance
# This router will be mounted in main.py under the "/api" prefix
router = APIRouter()
router.include_router(os_router)


# -------------------------------------------------
# TEXT TO SPEECH ROUTE
# -------------------------------------------------
# This endpoint converts text into speech and returns an audio file
@router.get("/tts")
async def tts(text: str):

    try:
        # Generate audio file
        path = await convert_text_to_audio(text)

    except Exception as e:
        # DO NOT crash server
        return JSONResponse(
            status_code=500,
            content={
                "status": "failed",
                "error": str(e)
            }
        )

    def cleanup_file(file_path: str):
        if os.path.exists(file_path):
            os.remove(file_path)

    return FileResponse(
        path,
        media_type="audio/mpeg",
        background=BackgroundTask(cleanup_file, path)
    )



# -------------------------------------------------
# MESSAGE ROUTE
# -------------------------------------------------
# This route processes user messages and generates AI responses
@router.post("/message")
async def process_message(request: Request):

    # Read raw JSON body from the request
    data = await request.json()


    # Validate the request payload manually
    # This replaces the Pydantic MessageRequest model
    validated = validate_message_request(data)


    # Extract user message text from validated data
    user_text = validated["message"]


    # Attempt to detect the language of the user message
    try:
        language = detect(user_text)

    # If language detection fails, fallback to English
    except:
        language = "en"


    # Generate AI response using the brain module

    # Try executing OS command first
    os_result = process_command(user_text)

    # If OS command executed successfully
    if os_result["status"] == "success":
        ai_response = os_result.get("output", "Command executed")

    else:
        # fallback to AI response
        ai_response = generate_ai_response(user_text)

    # Retrieve current conversation memory
    memory = get_memory()


    # Return formatted response
    # This replaces the Pydantic MessageResponse model
    return create_message_response(
        ai_response,      # AI generated reply
        len(memory),      # Current memory size
        "responding",     # System state
        language          # Detected language
    )



# -------------------------------------------------
# MEMORY ROUTE
# -------------------------------------------------
# This endpoint returns stored conversation history
@router.get("/memory")
def get_conversation_memory():

    # Retrieve memory and format it into response structure
    return create_memory_response(get_memory())



# -------------------------------------------------
# STATUS ROUTE
# -------------------------------------------------
# This endpoint provides system configuration details
@router.get("/status")
def get_status():

    # Return model configuration and system limits
    return create_status_response(
        MODEL_NAME,   # AI model name
        MAX_MEMORY,   # Maximum allowed memory size
        TEMPERATURE   # AI temperature setting
    )



# -------------------------------------------------
# STREAMING MESSAGE ROUTE
# -------------------------------------------------
# This endpoint streams AI responses token-by-token
# It allows real-time response generation similar to ChatGPT streaming
@router.post("/stream")
async def stream_message(request: Request):

    # Read incoming JSON request body
    data = await request.json()


    # Validate incoming message data
    validated = validate_message_request(data)


    # Extract the user message
    user_text = validated["message"]


    # Define a generator function that yields tokens one by one
    def token_generator():

        # Iterate over tokens generated by the streaming AI function
        for token in generate_ai_response_stream(user_text):

            # Yield each token to the client
            yield token


    # Return streaming response
    # The client receives tokens in real time
    return StreamingResponse(
        token_generator(),
        media_type="text/plain"
    )