import json
import time
from pathlib import Path

SESSIONS_FILE = Path("sessions.json")
LIMIT = 3
WINDOW = 120


def load_sessions() -> dict:
    if not SESSIONS_FILE.exists():
        return {}
    try:
        return json.loads(SESSIONS_FILE.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return {}


def save_sessions(sessions: dict):
    SESSIONS_FILE.write_text(json.dumps(sessions), encoding="utf-8")


def add_request(user_id: int) -> bool:
    sessions = load_sessions()
    now = time.time()

    sessions = {
        uid: [ts for ts in timestamps if now - ts < WINDOW]
        for uid, timestamps in sessions.items()
    }

    user_requests = sessions.get(str(user_id), [])

    if len(user_requests) >= LIMIT:
        save_sessions(sessions)
        return False

    user_requests.append(now)
    sessions[str(user_id)] = user_requests
    save_sessions(sessions)
    return True


def clear_sessions():
    save_sessions({})
