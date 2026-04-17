import uuid
from datetime import datetime, timedelta


# In-memory session store: {session_id: session_dict}
_sessions = {}

MAX_MESSAGES = 100


def create_session():
    """Create a new session and return its ID."""
    session_id = str(uuid.uuid4())
    now = datetime.utcnow()
    _sessions[session_id] = {
        "session_id": session_id,
        "messages": [],
        "created_at": now,
        "last_active": now,
        "active_mode": "tutor",
    }
    return session_id


def get_session(session_id):
    """Get a session by ID, or None if it doesn't exist or is expired."""
    session = _sessions.get(session_id)
    if session is None:
        return None
    return session


def get_or_create_session(session_id):
    """Get existing session or create a new one. Returns (session_dict, session_id)."""
    if session_id:
        session = get_session(session_id)
        if session is not None:
            session["last_active"] = datetime.utcnow()
            return session, session_id
    new_id = create_session()
    return _sessions[new_id], new_id


def add_message(session_id, role, content, message_type="chat"):
    """Add a message to the session's conversation history."""
    session = _sessions.get(session_id)
    if session is None:
        return
    msg = {
        "id": str(uuid.uuid4()),
        "role": role,
        "content": content,
        "message_type": message_type,
        "timestamp": datetime.utcnow().isoformat(),
    }
    session["messages"].append(msg)
    # Truncate if exceeding max
    if len(session["messages"]) > MAX_MESSAGES:
        session["messages"] = session["messages"][-MAX_MESSAGES:]
    session["last_active"] = datetime.utcnow()
    return msg


def get_messages(session_id):
    """Get all messages for a session."""
    session = _sessions.get(session_id)
    if session is None:
        return []
    return session["messages"]


def get_conversation_history(session_id):
    """Get messages formatted for the OpenAI API (list of {role, content} dicts)."""
    session = _sessions.get(session_id)
    if session is None:
        return []
    return [{"role": m["role"], "content": m["content"]} for m in session["messages"]]


def cleanup_expired_sessions(ttl_hours=2):
    """Remove sessions that have been inactive longer than ttl_hours."""
    cutoff = datetime.utcnow() - timedelta(hours=ttl_hours)
    expired = [sid for sid, s in _sessions.items() if s["last_active"] < cutoff]
    for sid in expired:
        del _sessions[sid]
    return len(expired)


def clear_all_sessions():
    """Clear all sessions. Used for testing."""
    _sessions.clear()
