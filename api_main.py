"""
File: api_server/main.py

Purpose:
This file is the main entry point of the FastAPI backend server.

It is responsible for:
1. Creating the FastAPI application instance.
2. Registering all API routes used by the AI system.
3. Serving the frontend UI (graphic_ai folder).
4. Connecting the backend API with the frontend interface.

In this architecture:
- FastAPI handles backend logic and API endpoints.
- The "graphic_ai" folder contains the frontend interface.
- StaticFiles allows the frontend to be served directly from FastAPI.
"""

# Import the FastAPI framework to create the backend application
from fastapi import FastAPI

# Import StaticFiles to serve frontend files (HTML, CSS, JS)
from fastapi.staticfiles import StaticFiles

# Import the API router that contains all backend routes
from api_server.api_routes import router

# Import os module to handle file system paths
import os


# Create the FastAPI application instance
# The title is used for API documentation (Swagger UI)
app = FastAPI(title="PROJECT-F API")


# Include all API routes from api_routes.py
# All endpoints inside that router will be available under the "/api" prefix
# Example: /api/chat , /api/tts , etc.
app.include_router(router, prefix="/api")


# Determine the absolute path to the frontend directory
# __file__ → current file path
# dirname(__file__) → folder of this file (api_server)
# ".." → move one level up to project root
# "graphic_ai" → frontend folder
frontend_path = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "graphic_ai")
)


# Mount the frontend directory as static files
# This allows FastAPI to serve HTML, CSS, and JavaScript files directly
# When users open the root URL "/", the frontend UI will load
app.mount(
    "/",  # Root URL where frontend will be accessible
    StaticFiles(directory=frontend_path, html=True),  # Serve static files and allow index.html
    name="frontend"  # Name used internally by FastAPI
)