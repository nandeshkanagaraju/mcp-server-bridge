import json
import os
from config.logger import logger

# --- Configuration ---
# This will create a directory to store conversation files
SESSION_DIR = "storage/session/conversations"
os.makedirs(SESSION_DIR, exist_ok=True)

def _get_session_filepath(session_id: str) -> str:
    """Generates a safe file path for a given session ID."""
    # Basic sanitization to prevent directory traversal
    safe_session_id = "".join(c for c in session_id if c.isalnum() or c in ('-', '_'))
    return os.path.join(SESSION_DIR, f"session_{safe_session_id}.json")

def get_history(session_id: str) -> list:
    """Retrieves conversation history from a JSON file."""
    filepath = _get_session_filepath(session_id)
    if not os.path.exists(filepath):
        return []
    try:
        with open(filepath, 'r') as f:
            return json.load(f)
    except Exception as e:
        logger.error(f"Error reading history file for session {session_id}: {e}")
        return []

def set_history(session_id: str, history: list):
    """Saves conversation history to a JSON file."""
    filepath = _get_session_filepath(session_id)
    try:
        with open(filepath, 'w') as f:
            json.dump(history, f, indent=2)
    except Exception as e:
        logger.error(f"Error writing history file for session {session_id}: {e}")