# Tasks: Nutrition Chatbot Web UI

**Input**: Design documents from `/specs/001-nutrition-chatbot-ui/`
**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md, contracts/api.md, quickstart.md

**Tests**: Not explicitly requested in the feature specification. Omitted.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization, dependencies, and configuration files

- [X] T001 Create project directory structure: `src/`, `static/`, `templates/`, `tests/` per plan.md
- [X] T002 Create `requirements.txt` with Flask==3.x, openai, pymupdf, python-dotenv, pytest
- [X] T003 [P] Create `.env.example` with all environment variables per quickstart.md
- [X] T004 [P] Create `src/__init__.py` and `tests/__init__.py` package init files

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [X] T005 Implement PDF extraction and course content loading in `src/knowledge.py` — extract text from all `.pdf` files in the project root using PyMuPDF, return list of CourseModule dicts per data-model.md
- [X] T006 [P] Implement system prompts for all three agent modes (tutor, flashcard, exam) in `src/prompts.py` — each prompt includes course content context and mode-specific instructions per research.md
- [X] T007 [P] Implement in-memory session management with TTL cleanup in `src/sessions.py` — Session entity with messages list, created_at, last_active, active_mode per data-model.md
- [X] T008 Implement agent routing with keyword-based intent detection in `src/agents.py` — detect flashcard/exam/tutor mode from message content, call OpenAI API with appropriate system prompt and conversation history per research.md
- [X] T009 Create Flask application entry point in `app.py` — initialize Flask app, load course content at startup via `src/knowledge.py`, configure routes, load env vars via python-dotenv

**Checkpoint**: Foundation ready — all backend modules exist and Flask app starts. User story implementation can begin.

---

## Phase 3: User Story 1 — Ask a Nutrition Question (Priority: P1) 🎯 MVP

**Goal**: Student can type a nutrition question in the web UI and receive an accurate answer grounded in course PowerPoint content.

**Independent Test**: Open http://localhost:5000, type a nutrition question, verify response is relevant and sourced from course slides.

### Implementation for User Story 1

- [X] T010 [US1] Create Jinja2 chat page template in `templates/index.html` — clean chat layout with message list area, text input, send button; include links to `static/style.css` and `static/app.js`; meta viewport tag for responsive base
- [X] T011 [P] [US1] Create chat UI styles in `static/style.css` — message bubbles with distinct styling for user (right-aligned, colored) vs assistant (left-aligned, different color); scrollable message area; fixed input bar at bottom; loading indicator styles
- [X] T012 [P] [US1] Create chat client-side logic in `static/app.js` — send message via POST `/api/chat`, append user message and bot reply to DOM, show/hide loading indicator while waiting, validate empty input before submit, auto-scroll to latest message
- [X] T013 [US1] Implement `GET /` route in `app.py` — serve `templates/index.html` via Flask's `render_template`
- [X] T014 [US1] Implement `POST /api/chat` route in `app.py` — validate message per contracts/api.md (non-empty, ≤5000 chars), get/create session from cookie, detect intent via `src/agents.py`, call LLM, store messages in session, return JSON response with reply and message_type; set session cookie in response
- [X] T015 [US1] Implement `GET /api/history` route in `app.py` — return conversation messages for current session per contracts/api.md
- [X] T016 [US1] Add error handling in `POST /api/chat` — catch OpenAI API errors and return user-friendly 500 response per contracts/api.md; handle out-of-scope questions via system prompt instruction (FR-007)

**Checkpoint**: User Story 1 complete. Student can open the web page, ask a nutrition question, see a loading indicator, and receive an answer. Chat history is visible. Errors are handled gracefully. This is a fully functional MVP.

---

## Phase 4: User Story 2 — Generate Flashcards for Study (Priority: P2)

**Goal**: Student can request flashcards on a specific topic and receive formatted Q&A pairs.

**Independent Test**: Type "Generate flashcards about Module 8 Theme 1" in the chat, verify the response contains clear Q&A flashcard pairs based on course content.

### Implementation for User Story 2

- [X] T017 [US2] Add flashcard-specific system prompt in `src/prompts.py` — instruct LLM to output structured Q&A pairs with clear question/answer separation; include course module content relevant to the requested topic
- [X] T018 [US2] Add flashcard keyword detection in `src/agents.py` — detect "flashcard", "cartão", "cartões", "flash card" keywords and route to flashcard prompt; set message_type to "flashcard" in response
- [X] T019 [P] [US2] Add flashcard rendering styles in `static/style.css` — card-style layout for Q&A pairs displayed in the chat, visually distinct from regular chat messages
- [X] T020 [US2] Add flashcard message rendering in `static/app.js` — detect `message_type: "flashcard"` in response and render with card-style DOM elements instead of plain text bubble

**Checkpoint**: User Story 2 complete. Student can request flashcards and receive visually formatted Q&A pairs. Regular Q&A from US1 still works.

---

## Phase 5: User Story 3 — Practice Exam Questions (Priority: P2)

**Goal**: Student can request practice exam questions, answer them, and receive scored feedback.

**Independent Test**: Type "Give me practice questions about integrated approaches", answer the questions, verify feedback is accurate and references course material.

### Implementation for User Story 3

- [X] T021 [US3] Add exam-prep-specific system prompt in `src/prompts.py` — instruct LLM to generate numbered exam questions; instruct LLM to evaluate student answers and provide detailed feedback referencing course content
- [X] T022 [US3] Add exam keyword detection in `src/agents.py` — detect "exam", "quiz", "practice", "exame", "teste", "questões" keywords and route to exam prompt; set message_type to "exam_question" for questions, "exam_feedback" for feedback
- [X] T023 [P] [US3] Add exam question and feedback rendering styles in `static/style.css` — distinct styling for exam questions (numbered list, answer prompt) and feedback (correct/incorrect indicators)
- [X] T024 [US3] Add exam message rendering in `static/app.js` — detect `message_type: "exam_question"` and `"exam_feedback"` in response and render with appropriate DOM layout

**Checkpoint**: User Story 3 complete. Student can request exam questions, submit answers, and get feedback. US1 and US2 still work.

---

## Phase 6: User Story 4 — Conversational Context Continuity (Priority: P3)

**Goal**: Chatbot understands follow-up questions that reference previous answers within the same session.

**Independent Test**: Ask a question, then ask "Can you elaborate on the second point?" — verify the chatbot responds contextually.

### Implementation for User Story 4

- [X] T025 [US4] Update `src/agents.py` to include full conversation history in LLM API call — pass all session messages (up to context window limit) as the messages array to the OpenAI chat completion endpoint
- [X] T026 [US4] Implement conversation history truncation in `src/sessions.py` — when message count exceeds limit (100), keep system prompt + most recent N messages to fit within context window; preserve session continuity

**Checkpoint**: User Story 4 complete. Follow-up questions work within a session. Page refresh starts a fresh conversation.

---

## Phase 7: User Story 5 — Access from Any Device (Priority: P3)

**Goal**: Chat interface is fully usable on mobile phones and tablets.

**Independent Test**: Open http://localhost:5000 on a 320px-wide viewport, verify the interface is fully usable without horizontal scrolling.

### Implementation for User Story 5

- [X] T027 [US5] Add responsive CSS in `static/style.css` — media queries for screens ≤768px (tablet) and ≤480px (mobile); adjust message bubble widths, font sizes, input bar layout; ensure no horizontal scrolling at 320px width
- [X] T028 [US5] Update `templates/index.html` — verify meta viewport tag is correct; adjust any fixed-width elements; ensure touch-friendly input and button sizes (min 44px tap targets)

**Checkpoint**: User Story 5 complete. Chat works on desktop, tablet, and mobile. All previous stories still work.

---

## Phase 8: Polish & Cross-Cutting Concerns

**Purpose**: Edge cases, security, and final quality improvements

- [X] T029 [P] Implement `GET /api/modules` route in `app.py` — return list of loaded course modules per contracts/api.md
- [X] T030 [P] Add input length validation in `static/app.js` — prevent submission of messages exceeding 5000 characters, show client-side warning
- [X] T031 Add rate limiting for rapid message submission in `static/app.js` — disable send button while a request is in-flight to prevent duplicate requests (edge case from spec)
- [X] T032 [P] Add session cleanup background task in `app.py` — periodically purge sessions where `last_active` exceeds SESSION_TTL_HOURS
- [X] T033 Run `quickstart.md` validation — follow setup steps from scratch in a clean environment, verify the app starts and serves the chat UI correctly

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies — can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion — BLOCKS all user stories
- **User Story 1 (Phase 3)**: Depends on Foundational (Phase 2) — this is the MVP
- **User Story 2 (Phase 4)**: Depends on Foundational (Phase 2) — can run in parallel with US1
- **User Story 3 (Phase 5)**: Depends on Foundational (Phase 2) — can run in parallel with US1, US2
- **User Story 4 (Phase 6)**: Depends on US1 being complete (needs working session + agents)
- **User Story 5 (Phase 7)**: Depends on US1 being complete (needs working HTML/CSS)
- **Polish (Phase 8)**: Depends on all desired user stories being complete

### User Story Dependencies

- **US1 (P1)**: No dependencies on other stories. This is the MVP.
- **US2 (P2)**: Independent of US1. Both add to `agents.py`, `prompts.py`, `app.js`, `style.css` but in separate code paths.
- **US3 (P2)**: Independent of US1 and US2. Same files, separate code paths.
- **US4 (P3)**: Depends on US1 (needs working conversation flow to add context continuity).
- **US5 (P3)**: Depends on US1 (needs working HTML/CSS to make responsive).

### Within Each User Story

- Backend changes before frontend (prompts → agents → routes → JS → CSS)
- Core implementation before styling
- Story complete before moving to next priority

### Parallel Opportunities

- T003 and T004 can run in parallel (Setup phase)
- T006 and T007 can run in parallel (Foundational phase)
- T011 and T012 can run in parallel (US1: CSS and JS are independent)
- T019 can run in parallel with T017/T018 (US2: CSS independent of backend)
- T023 can run in parallel with T021/T022 (US3: CSS independent of backend)
- US2 and US3 can be worked on in parallel once Foundational is complete
- T029, T030, T032 can run in parallel (Polish phase)

---

## Parallel Example: User Story 1

```bash
# After Foundational phase is complete:

# These can run in parallel (different files):
Task T011: "Create chat UI styles in static/style.css"
Task T012: "Create chat client-side logic in static/app.js"

# Then sequential (depends on above):
Task T010: "Create Jinja2 chat page template in templates/index.html"
Task T013: "Implement GET / route in app.py"
Task T014: "Implement POST /api/chat route in app.py"
Task T015: "Implement GET /api/history route in app.py"
Task T016: "Add error handling in POST /api/chat"
```

---

## Parallel Example: User Stories 2 & 3 (can run concurrently)

```bash
# Developer A (US2):
Task T017: "Add flashcard-specific system prompt in src/prompts.py"
Task T018: "Add flashcard keyword detection in src/agents.py"
Task T019: "Add flashcard rendering styles in static/style.css"  # [P]
Task T020: "Add flashcard message rendering in static/app.js"

# Developer B (US3) — simultaneously:
Task T021: "Add exam-prep-specific system prompt in src/prompts.py"
Task T022: "Add exam keyword detection in src/agents.py"
Task T023: "Add exam question and feedback rendering styles in static/style.css"  # [P]
Task T024: "Add exam message rendering in static/app.js"
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup (T001–T004)
2. Complete Phase 2: Foundational (T005–T009)
3. Complete Phase 3: User Story 1 (T010–T016)
4. **STOP and VALIDATE**: Open http://localhost:5000, ask a nutrition question, verify response
5. Deploy/demo if ready — this is a working chatbot

### Incremental Delivery

1. Setup + Foundational → Foundation ready
2. Add User Story 1 → Test → Deploy/Demo (**MVP!**)
3. Add User Story 2 → Test → Deploy/Demo (flashcards added)
4. Add User Story 3 → Test → Deploy/Demo (exam prep added)
5. Add User Story 4 → Test → Deploy/Demo (context continuity)
6. Add User Story 5 → Test → Deploy/Demo (mobile responsive)
7. Polish → Final release

---

## Notes

- [P] tasks = different files, no dependencies
- [Story] label maps task to specific user story for traceability
- Each user story is independently completable and testable
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
- The spec does not request TDD — test tasks are omitted
