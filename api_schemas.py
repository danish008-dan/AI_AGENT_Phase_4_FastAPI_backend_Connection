"""
File: api_server/schemas.py

Purpose:
This file provides procedural validation and response construction
for API requests and responses.

Instead of using Pydantic models or OOP-based schemas, this module
implements lightweight validation helpers using simple Python
functions.

Responsibilities:
1. Validate incoming API request payloads
2. Enforce correct data types for inputs
3. Construct standardized response dictionaries
4. Maintain consistent API response structure

Architecture Role:
This module replaces traditional schema systems (like Pydantic models)
with procedural validation to keep the architecture minimal and
framework-independent.
"""

# Import typing utilities for type hints
# List -> represents a list/array
# Dict -> represents a dictionary/object
from typing import List, Dict


# -------------------------------------------------
# VALIDATION HELPERS
# -------------------------------------------------

# Internal helper function used to enforce type validation
# It checks whether a given value matches the expected type
def _ensure_type(value, expected_type, field_name):

    # Verify that the value is of the expected Python type
    if not isinstance(value, expected_type):

        # If the type is incorrect, raise an informative error
        raise TypeError(f"{field_name} must be {expected_type.__name__}")

    # If validation passes, return the original value
    return value


# -------------------------------------------------
# MESSAGE REQUEST
# -------------------------------------------------

# Validate the incoming message request payload
# This replaces a traditional Pydantic MessageRequest model
def validate_message_request(data: Dict) -> Dict:

    # Ensure the incoming request body is a dictionary
    _ensure_type(data, dict, "MessageRequest")

    # Check whether the required "message" field exists
    if "message" not in data:

        # Raise an error if the field is missing
        raise ValueError("Missing field: message")

    # Ensure the "message" value is a string
    message = _ensure_type(data["message"], str, "message")

    # Return a normalized dictionary structure
    return {
        "message": message
    }


# -------------------------------------------------
# MESSAGE RESPONSE
# -------------------------------------------------

# Construct the API response for AI-generated messages
# This replaces a traditional Pydantic MessageResponse model
def create_message_response(response: str, memory_size: int, state: str, language: str) -> Dict:

    # Validate the response text type
    _ensure_type(response, str, "response")

    # Validate memory size type
    _ensure_type(memory_size, int, "memory_size")

    # Validate system state type
    _ensure_type(state, str, "state")

    # Validate detected language type
    _ensure_type(language, str, "language")

    # Return standardized API response structure
    return {
        "response": response,       # AI generated reply
        "memory_size": memory_size, # Current conversation memory size
        "state": state,             # Current system state (e.g., responding)
        "language": language        # Detected language of the user input
    }


# -------------------------------------------------
# MEMORY RESPONSE
# -------------------------------------------------

# Construct the response containing stored conversation memory
def create_memory_response(memory: List[Dict]) -> Dict:

    # Ensure the memory container is a list
    _ensure_type(memory, list, "memory")

    # Validate each item in the memory list
    for i, item in enumerate(memory):

        # Ensure every memory entry is a dictionary
        _ensure_type(item, dict, f"memory[{i}]")

    # Return formatted memory response
    return {
        "memory": memory
    }


# -------------------------------------------------
# STATUS RESPONSE
# -------------------------------------------------

# Construct a system status response containing configuration info
def create_status_response(model: str, max_memory: int, temperature: float) -> Dict:

    # Validate model name type
    _ensure_type(model, str, "model")

    # Validate max memory type
    _ensure_type(max_memory, int, "max_memory")

    # Validate temperature type
    _ensure_type(temperature, float, "temperature")

    # Return system configuration response
    return {
        "model": model,           # Name of the AI model in use
        "max_memory": max_memory, # Maximum conversation memory size
        "temperature": temperature # AI sampling temperature
    }