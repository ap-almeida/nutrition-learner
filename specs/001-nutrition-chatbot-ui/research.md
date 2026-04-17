# Research: Nutrition Chatbot Web UI

**Feature**: 001-nutrition-chatbot-ui  
**Date**: 2026-04-17

## Technology Stack Selection

### Decision: Python 3.11+ with Flask

**Rationale**: Flask is the simplest production-ready Python web framework. It requires minimal boilerplate, has excellent documentation, and can serve both the API backend and the static HTML frontend from a single process. Python is the most common language for AI/LLM integrations, making library support for PDF parsing and LLM APIs first-class.

**Alternatives considered**:
- **Streamlit/Gradio**: Even simpler for prototyping, but limited control over UI styling and chat UX. Not suitable for a polished chat interface with custom message formatting (flashcards, exam questions).
- **Node.js + Express**: Viable, but Python has better ecosystem support for PDF extraction and LLM integrations. Adds complexity of managing two languages if LLM logic is in Python.
- **Django**: Over-engineered for this use case — ORM, admin panel, migrations are unnecessary when there's no database.
- **FastAPI**: Excellent but async paradigm adds complexity for a simple synchronous chat workflow. Flask is simpler for beginners.

---

### Decision: Vanilla HTML/CSS/JavaScript frontend (no framework)

**Rationale**: The chat interface is a single page with a message list, input box, and send button. This does not warrant a build system (webpack, Vite) or a framework (React, Vue). Vanilla JS with modern DOM APIs is sufficient, requires zero build steps, and can be served directly by Flask as static files. This is the easiest to maintain and deploy.

**Alternatives considered**:
- **React/Vue/Svelte**: Adds npm/node toolchain, build step, and framework learning curve. Overkill for a single-page chat UI.
- **HTMX**: Good for server-rendered interactions, but chat UIs benefit from client-side state management for real-time message appending. Adds a dependency for minimal gain.
- **Jinja2 templates**: Could render server-side, but chat requires dynamic client-side updates (append messages without full page reload). Still used for the initial page shell.

---

### Decision: OpenAI-compatible API for LLM processing

**Rationale**: The OpenAI Python SDK (`openai`) is the most widely used and documented LLM client library. It supports the OpenAI API, Azure OpenAI, and any OpenAI-compatible endpoint (local LLMs via Ollama, LM Studio, etc.). This gives maximum flexibility for the user to choose their LLM provider via environment variables.

**Alternatives considered**:
- **LangChain**: Adds heavy abstraction layer and many transitive dependencies for what is essentially a single prompt-response pattern with context. Unnecessary complexity.
- **Direct HTTP requests**: Works but loses retry logic, streaming support, and type safety that the SDK provides.
- **Hugging Face Transformers (local)**: Requires GPU, large model downloads, and significant compute. Not suitable for a simple study tool.

---

### Decision: PyMuPDF (pymupdf) for PDF text extraction

**Rationale**: PyMuPDF is the fastest and most reliable Python PDF library. It extracts text preserving layout structure, handles Portuguese characters correctly, and has no system-level dependencies (pure Python wheel). The course PDFs are PowerPoint-exported slides, which PyMuPDF handles well.

**Alternatives considered**:
- **pdfplumber**: Good alternative, slightly slower but more layout-aware. PyMuPDF is faster for bulk extraction.
- **PyPDF2/pypdf**: Less reliable text extraction, especially for complex slide layouts.
- **Apache Tika**: Requires Java runtime — adds heavy system dependency.

---

### Decision: In-memory session storage (no database)

**Rationale**: The spec explicitly states conversation history is session-only and not persisted. With low concurrency (student study tool), Python dictionaries keyed by session ID are sufficient. This eliminates all database setup, migration, and connection management complexity.

**Alternatives considered**:
- **SQLite**: Would persist data unnecessarily and add ORM/query complexity.
- **Redis**: Overkill for single-user/low-concurrency sessions.
- **Flask-Session with filesystem**: Possible but adds dependency for minimal benefit over in-memory dicts.

---

### Decision: pytest for testing

**Rationale**: pytest is the standard Python testing framework. Flask has excellent test client support via `app.test_client()`. No additional testing dependencies needed beyond pytest itself.

---

## Architecture Decisions

### Agent Routing

The three agent capabilities (Nutrition Tutor, Flashcard Generator, Exam Prep Coach) will be implemented as a single LLM integration with different system prompts. The backend will detect the user's intent (ask question, generate flashcards, practice exam) based on keywords or explicit commands, and route to the appropriate system prompt that instructs the LLM to behave as that specific agent.

**Decision**: Keyword-based intent detection with fallback to Nutrition Tutor (default mode).
- Messages containing "flashcard" / "cartão" → Flashcard Generator prompt
- Messages containing "exam" / "quiz" / "practice" / "exame" / "teste" → Exam Prep Coach prompt
- All other messages → Nutrition Tutor prompt (default)

**Rationale**: Simple, predictable, no ML classification needed. The user can always reach any mode by using clear keywords. The Nutrition Tutor is the most common use case and serves as a safe default.

### Knowledge Base Loading

PDF content will be extracted once at application startup and stored in memory as a structured text corpus. Each PDF maps to a "module" that can be referenced by the LLM. The full text is included in the system prompt context window.

**Decision**: Load all PDFs at startup, structure by filename, include relevant sections in LLM context per request.

**Rationale**: The course material is a small corpus (7 PDFs of slide content). Total text likely fits within modern LLM context windows (128k tokens). Pre-loading avoids per-request file I/O.

### Session Management

Each browser session gets a UUID-based session ID (stored in a cookie). Conversation history is maintained in a server-side dictionary. Sessions are cleaned up after 2 hours of inactivity.

**Decision**: Server-side session dict with cookie-based session ID and TTL cleanup.

**Rationale**: Simpler than client-side storage (which would require sending full history with each request). Server-side allows the backend to manage context window limits.
