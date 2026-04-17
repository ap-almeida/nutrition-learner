# nutri Development Guidelines

Auto-generated from all feature plans. Last updated: 2026-04-17

## Active Technologies
- Python 3.10+ + openai>=1.0, PyMuPDF, python-dotenv, colorama (002-session-persistence)
- In-memory only (`list` in `chat.py`) — no disk persistence (002-session-persistence)

- Python 3.11+ + Flask 3.x, openai (Python SDK), PyMuPDF (pymupdf), python-dotenv (001-nutrition-chatbot-ui)

## Project Structure

```text
backend/
frontend/
tests/
```

## Commands

cd src && pytest && ruff check .

## Code Style

Python 3.11+: Follow standard conventions

## Recent Changes
- 002-session-persistence: Added Python 3.10+ + openai>=1.0, PyMuPDF, python-dotenv, colorama

- 001-nutrition-chatbot-ui: Added Python 3.11+ + Flask 3.x, openai (Python SDK), PyMuPDF (pymupdf), python-dotenv

<!-- MANUAL ADDITIONS START -->
<!-- MANUAL ADDITIONS END -->
