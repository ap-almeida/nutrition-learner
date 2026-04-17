# Implementation Plan: Conversation Persistence within a Session

**Branch**: `001-nutrition-chatbot-ui` | **Date**: 2026-04-17 | **Spec**: specs/001-nutrition-chatbot-ui/spec.md

## Summary

Add full conversational context to the terminal chatbot so follow-up questions within a session are understood without repeating context. The main changes are: (1) replace per-message system-prompt switching with a single unified session system prompt, and (2) raise the history trim ceiling from 40 to a configurable `MAX_HISTORY` (default 60).

## Technical Context

**Language/Version**: Python 3.10+  
**Primary Dependencies**: openai>=1.0, PyMuPDF, python-dotenv, colorama  
**Storage**: In-memory list (no disk persistence — session only)  
**Testing**: Manual smoke test via `python chat.py`  
**Target Platform**: Linux / macOS / Windows terminal  
**Project Type**: CLI  
**Performance Goals**: No regression in response time  
**Constraints**: Must stay within llama3.2 / gpt-4o-mini context window  
**Scale/Scope**: Single-user terminal session

## Constitution Check

No project constitution defined — no gates to evaluate.

## Project Structure

### Documentation (this feature)

```text
specs/001-nutrition-chatbot-ui/
├── plan.md              ← This file
├── research.md          ← Phase 0 output
├── data-model.md        ← Phase 1 output
└── tasks.md             ← Phase 2 output
```

### Source Code changes

```text
src/prompts.py     ← Add SESSION_SYSTEM_PROMPT (unified)
src/agents.py      ← Accept system_prompt param; default to unified prompt
chat.py            ← Use unified prompt; raise MAX_HISTORY; show turn count
```

## Phase 0: Research findings

See research.md. Key decisions:

1. **Single unified system prompt** — system prompt stays constant for the whole session; `detect_mode()` runs for the UI label only  
2. **MAX_HISTORY = 60** (default) — configurable via `.env`; keeps last 30 exchanges  
3. **No file persistence** — "durante uma sessão" scope only

## Phase 1: Design

### data-model.md

No new entities. The `history` list already models the conversation:

```python
history: list[dict]  # [{"role": "user"|"assistant", "content": str}, ...]
```

Trim policy: keep `history[-MAX_HISTORY:]` where `MAX_HISTORY` is read from env (default 60).

### Unified system prompt design

`SESSION_SYSTEM_PROMPT` in `src/prompts.py`:
- Combines tutor + flashcard + exam instructions into one prompt
- LLM selects the appropriate response style based on the user's message naturally
- Keeps `{knowledge}` placeholder filled with course content

### contracts/

No external API contract changes. The `get_reply()` signature gains one optional parameter:

```python
get_reply(message, history, knowledge_text, api_key, base_url=None, model=..., system_prompt=None)
```

When `system_prompt` is `None`, uses `SESSION_SYSTEM_PROMPT`. This is backwards-compatible.


## Summary

[Extract from feature spec: primary requirement + technical approach from research]

## Technical Context

<!--
  ACTION REQUIRED: Replace the content in this section with the technical details
  for the project. The structure here is presented in advisory capacity to guide
  the iteration process.
-->

**Language/Version**: [e.g., Python 3.11, Swift 5.9, Rust 1.75 or NEEDS CLARIFICATION]  
**Primary Dependencies**: [e.g., FastAPI, UIKit, LLVM or NEEDS CLARIFICATION]  
**Storage**: [if applicable, e.g., PostgreSQL, CoreData, files or N/A]  
**Testing**: [e.g., pytest, XCTest, cargo test or NEEDS CLARIFICATION]  
**Target Platform**: [e.g., Linux server, iOS 15+, WASM or NEEDS CLARIFICATION]
**Project Type**: [e.g., library/cli/web-service/mobile-app/compiler/desktop-app or NEEDS CLARIFICATION]  
**Performance Goals**: [domain-specific, e.g., 1000 req/s, 10k lines/sec, 60 fps or NEEDS CLARIFICATION]  
**Constraints**: [domain-specific, e.g., <200ms p95, <100MB memory, offline-capable or NEEDS CLARIFICATION]  
**Scale/Scope**: [domain-specific, e.g., 10k users, 1M LOC, 50 screens or NEEDS CLARIFICATION]

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

[Gates determined based on constitution file]

## Project Structure

### Documentation (this feature)

```text
specs/[###-feature]/
├── plan.md              # This file (/speckit.plan command output)
├── research.md          # Phase 0 output (/speckit.plan command)
├── data-model.md        # Phase 1 output (/speckit.plan command)
├── quickstart.md        # Phase 1 output (/speckit.plan command)
├── contracts/           # Phase 1 output (/speckit.plan command)
└── tasks.md             # Phase 2 output (/speckit.tasks command - NOT created by /speckit.plan)
```

### Source Code (repository root)
<!--
  ACTION REQUIRED: Replace the placeholder tree below with the concrete layout
  for this feature. Delete unused options and expand the chosen structure with
  real paths (e.g., apps/admin, packages/something). The delivered plan must
  not include Option labels.
-->

```text
# [REMOVE IF UNUSED] Option 1: Single project (DEFAULT)
src/
├── models/
├── services/
├── cli/
└── lib/

tests/
├── contract/
├── integration/
└── unit/

# [REMOVE IF UNUSED] Option 2: Web application (when "frontend" + "backend" detected)
backend/
├── src/
│   ├── models/
│   ├── services/
│   └── api/
└── tests/

frontend/
├── src/
│   ├── components/
│   ├── pages/
│   └── services/
└── tests/

# [REMOVE IF UNUSED] Option 3: Mobile + API (when "iOS/Android" detected)
api/
└── [same as backend above]

ios/ or android/
└── [platform-specific structure: feature modules, UI flows, platform tests]
```

**Structure Decision**: [Document the selected structure and reference the real
directories captured above]

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| [e.g., 4th project] | [current need] | [why 3 projects insufficient] |
| [e.g., Repository pattern] | [specific problem] | [why direct DB access insufficient] |
