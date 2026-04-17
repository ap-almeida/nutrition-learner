# Quickstart: Nutrition Chatbot Web UI

**Feature**: 001-nutrition-chatbot-ui  
**Date**: 2026-04-17

## Prerequisites

- Python 3.11 or later
- An OpenAI API key (or compatible LLM API endpoint)

## Setup

```bash
# 1. Create virtual environment
python3 -m venv venv
source venv/bin/activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. Configure environment
cp .env.example .env
# Edit .env and set your OPENAI_API_KEY
```

## Environment Variables

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `OPENAI_API_KEY` | Yes | — | API key for the LLM provider |
| `OPENAI_BASE_URL` | No | `https://api.openai.com/v1` | Base URL for OpenAI-compatible API |
| `OPENAI_MODEL` | No | `gpt-4o-mini` | Model name to use for chat completions |
| `FLASK_PORT` | No | `5000` | Port the web server listens on |
| `FLASK_DEBUG` | No | `false` | Enable debug mode (development only) |
| `SESSION_TTL_HOURS` | No | `2` | Hours before inactive sessions are purged |

## Run

```bash
# Start the server
python app.py

# Open in browser
# http://localhost:5000
```

## Test

```bash
# Run all tests
pytest

# Run with verbose output
pytest -v
```

## Project Structure

```
├── app.py                  # Flask application entry point
├── requirements.txt        # Python dependencies
├── .env.example            # Environment variable template
├── src/
│   ├── __init__.py
│   ├── knowledge.py        # PDF extraction and course content loading
│   ├── agents.py           # LLM agent routing (tutor, flashcard, exam)
│   ├── sessions.py         # In-memory session management
│   └── prompts.py          # System prompts for each agent mode
├── static/
│   ├── style.css           # Chat UI styles
│   └── app.js              # Chat UI client-side logic
├── templates/
│   └── index.html          # Chat page template (Jinja2)
└── tests/
    ├── __init__.py
    ├── test_knowledge.py   # PDF extraction tests
    ├── test_agents.py      # Agent routing tests
    ├── test_sessions.py    # Session management tests
    └── test_api.py         # API endpoint integration tests
```
