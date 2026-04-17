# Feature Specification: Session Conversation Persistence

**Feature Branch**: `002-session-persistence`  
**Created**: 2026-04-17  
**Status**: Draft  
**Input**: User description: "quero que o chat bot existente tenha persistencia na conversa ou seja, que durante uma sessao ele tenha contexto todo dessa sessao"

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Full Session Context (Priority: P1)

During a terminal chat session, the user asks multiple related questions and expects the chatbot to remember everything said earlier in that same session — so follow-up questions are answered with awareness of the full conversation history.

**Why this priority**: Core of the feature request. Without this, every message is treated in isolation and the bot cannot answer follow-up or contextual questions.

**Independent Test**: Start a session, send 3 messages where message 3 references something from message 1. The bot must answer coherently referencing the earlier context.

**Acceptance Scenarios**:

1. **Given** the user has asked "O que é glicémia?" earlier in the session, **When** the user asks "Como se relaciona com a diabetes?", **Then** the bot answers in the context of glycaemia without needing the topic to be repeated.
2. **Given** the user has had a 10-message conversation, **When** the user asks a follow-up, **Then** the bot has access to all prior messages in that session.
3. **Given** a fresh session start, **When** the user sends the first message, **Then** the bot responds with no assumed prior context.

---

### User Story 2 - Context Preserved Across Mode Switches (Priority: P2)

The user starts in tutor mode, asks several questions, then switches to flashcard or exam mode — and the bot retains the conversation history across that mode switch within the same session.

**Why this priority**: Users naturally mix modes during a study session; losing context on mode switch would feel broken.

**Independent Test**: Ask a tutor question, then request flashcards on the same topic. The flashcards should reflect the specific subject discussed, not just the raw keyword.

**Acceptance Scenarios**:

1. **Given** the user discussed "Módulo 8 Tema 1" in tutor mode, **When** the user types "flashcards sobre isso", **Then** the bot generates flashcards using the context of the prior discussion.
2. **Given** a mixed-mode conversation, **When** the user asks "resume o que discutimos", **Then** the bot can summarize the full session.

---

### User Story 3 - Session Reset on Demand (Priority: P3)

The user can explicitly clear the conversation history mid-session to start fresh, without quitting the application.

**Why this priority**: Useful when switching topics completely and the prior context would confuse the model.

**Independent Test**: Start a conversation, type `limpar`/`clear`, then ask a follow-up. The bot must not reference anything said before the clear.

**Acceptance Scenarios**:

1. **Given** a long ongoing conversation, **When** the user types `limpar` or `clear`, **Then** the conversation history is wiped and the bot acknowledges a fresh start.
2. **Given** the user clears history, **When** the user asks a follow-up to a pre-clear question, **Then** the bot has no knowledge of the pre-clear conversation.

---

### Edge Cases

- What happens when the conversation history grows very long and exceeds the model's context window?
- How does the system behave if the user never sends any message (empty session)?
- What happens if the user switches between flashcard/exam/tutor modes many times in one session?

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: The system MUST retain all messages exchanged in the current terminal session in an in-memory history list.
- **FR-002**: Every outgoing user message MUST be appended to the session history before the LLM call.
- **FR-003**: Every bot response MUST be appended to the session history after the LLM call.
- **FR-004**: The session history MUST be passed to the LLM on every call, so the model has full conversation context.
- **FR-005**: The session history MUST be reset to empty when the user issues the `limpar` or `clear` command.
- **FR-006**: When the session history exceeds a configurable threshold (default: 40 messages), the system MUST trim the oldest messages to stay within model context limits, always retaining the system prompt.
- **FR-007**: The session history MUST NOT persist across separate executions of the program (i.e., no disk storage — in-memory only).
- **FR-008**: Mode switching (tutor / flashcard / exam) MUST NOT reset the conversation history.

### Key Entities

- **Session History**: An ordered list of message objects (`role`: user/assistant, `content`: text) maintained in memory for the duration of one program execution.
- **Message**: A single exchange unit with `role` (user or assistant) and `content` (string).

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: A follow-up question referencing a topic from earlier in the session is answered correctly without re-stating the topic, in 100% of test cases with a capable model.
- **SC-002**: Session history is fully cleared after a `limpar`/`clear` command — verified by a follow-up question that returns no prior context.
- **SC-003**: Conversations of at least 20 exchanges remain coherent without crashing or exceeding model limits.
- **SC-004**: Mode switching between tutor/flashcard/exam does not lose any conversation history.

## Assumptions

- Session persistence is in-memory only — no file or database storage is required.
- The existing `history` list in `chat.py` is the correct place to implement this; it already exists but may not be passed consistently to `get_reply`.
- The LLM (Ollama/llama3.2) supports multi-turn conversation via the standard OpenAI messages array format.
- History trimming (FR-006) is acceptable to the user as a tradeoff against model context limits.
- This feature applies only to the terminal CLI (`chat.py`); no web interface is in scope.
