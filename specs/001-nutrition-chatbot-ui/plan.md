# Implementation Plan: Nutrition Chatbot Web UI

**Branch**: `001-nutrition-chatbot-ui` | **Date**: 2026-04-17 | **Spec**: [specs/001-nutrition-chatbot-ui/spec.md](spec.md)
**Input**: Feature specification from `/specs/001-nutrition-chatbot-ui/spec.md`

## Summary

Build a web-accessible chatbot UI that lets nutrition students ask questions, generate flashcards, and practice exam questions — all grounded in course PowerPoint content. The backend uses Python/Flask with an OpenAI-compatible LLM API to process queries against extracted PDF text. The frontend is a single-page vanilla HTML/CSS/JS chat interface served by Flask.

## Technical Context

**Language/Version**: Python 3.11+  
**Primary Dependencies**: Flask 3.x, openai (Python SDK), PyMuPDF (pymupdf), python-dotenv  
**Storage**: In-memory (Python dicts) — no database required  
**Testing**: pytest + Flask test client  
**Target Platform**: Linux/macOS/Windows server, accessed via web browser  
**Project Type**: web-service (single-process Flask app serving API + static frontend)  
**Performance Goals**: <15s response time per question (LLM-bound), single-user/low-concurrency  
**Constraints**: Must fit course content in LLM context window (~128k tokens); no GPU required  
**Scale/Scope**: 1-5 concurrent users, 7 PDF source files, 1 HTML page, ~10 source files

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

Constitution is not customized (blank template). No specific gates to enforce. Proceeding with default best practices:
- ✅ Keep it simple (single Flask process, no unnecessary abstractions)
- ✅ Test-first approach (pytest for all backend logic)
- ✅ No over-engineering (in-memory storage, vanilla frontend)

**Post-Phase 1 re-check**: ✅ Design remains simple. Single project structure, no database, no build tools, no framework overhead. All decisions align with simplicity principles.

## Project Structure

### Documentation (this feature)

```text
specs/001-nutrition-chatbot-ui/
├── plan.md              # This file
├── research.md          # Phase 0: Technology decisions and rationale
├── data-model.md        # Phase 1: Entity definitions and relationships
├── quickstart.md        # Phase 1: Setup and run instructions
├── contracts/
│   └── api.md           # Phase 1: HTTP API contract
└── tasks.md             # Phase 2 output (/speckit.tasks command)
```

### Source Code (repository root)

```text
app.py                   # Flask application entry point
requirements.txt         # Python dependencies
.env.example             # Environment variable template
src/
├── __init__.py
├── knowledge.py         # PDF extraction and course content loading
├── agents.py            # LLM agent routing (tutor, flashcard, exam)
├── sessions.py          # In-memory session management with TTL
└── prompts.py           # System prompts for each agent mode
static/
├── style.css            # Chat UI responsive styles
└── app.js               # Chat UI client-side logic
templates/
└── index.html           # Chat page template (Jinja2)
tests/
├── __init__.py
├── test_knowledge.py    # PDF extraction tests
├── test_agents.py       # Agent routing tests
├── test_sessions.py     # Session management tests
└── test_api.py          # API endpoint integration tests
```

**Structure Decision**: Single-project structure. Flask serves both the API and the frontend from one process. No separate frontend build step. The `src/` directory contains all backend Python modules. `static/` and `templates/` are Flask convention directories for frontend assets. This is the simplest possible structure for a Python web application.

## Complexity Tracking

No constitution violations. No complexity justifications needed.
