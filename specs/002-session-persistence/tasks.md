# Tasks: Session Conversation Persistence

**Input**: Design documents from `/specs/002-session-persistence/`
**Prerequisites**: plan.md ✅, spec.md ✅, research.md ✅, data-model.md ✅, quickstart.md ✅

> **⚠️ NOTE**: Research confirmed all 8 functional requirements are already implemented in `chat.py` and `src/agents.py`. No new code is required. Tasks below cover verification and branch closure only.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel
- **[Story]**: User story label (US1, US2, US3)

---

## Phase 1: Setup

**Purpose**: No setup needed — feature is already implemented. Confirm environment is working.

- [X] T001 Verify venv is active and dependencies installed: `source venv/bin/activate && pip install -r requirements.txt`

---

## Phase 2: Foundational

**Purpose**: Confirm the existing history mechanism is wired correctly end-to-end before verifying individual stories.

- [X] T002 Verify `get_reply()` signature accepts `history` param in `src/agents.py` and passes it to LLM via `messages.extend(history)`
- [X] T003 [P] Verify `history = []` is initialised at session start in `chat.py` (line ~122)
- [X] T004 [P] Verify `history.append()` calls exist after successful LLM reply in `chat.py`

**Checkpoint**: Core wiring confirmed — all story verifications can proceed

---

## Phase 3: User Story 1 - Full Session Context (Priority: P1) 🎯 MVP

**Goal**: The LLM receives the full conversation history on every call so follow-up questions are answered in context.

**Independent Test**: Start `python chat.py`, ask "O que é glicémia?", then ask "Como se relaciona com a diabetes?" — the bot should reference glycaemia without being told again.

### Implementation for User Story 1

- [X] T005 [US1] Verify `messages.extend(history)` in `src/agents.py` — history is prepended before current user message on every LLM call
- [X] T006 [US1] Verify history grows correctly: after each successful exchange, both `{"role": "user"}` and `{"role": "assistant"}` entries are appended in `chat.py`
- [X] T007 [US1] Manual test: run `python chat.py`, hold a 3-message conversation where message 3 references message 1 — confirm coherent response

**Checkpoint**: US1 verified — multi-turn context working

---

## Phase 4: User Story 2 - Context Across Mode Switches (Priority: P2)

**Goal**: Switching between tutor/flashcard/exam modes within a session does NOT reset conversation history.

**Independent Test**: Ask a tutor question, then type "flashcards sobre isso" — the flashcards should reflect the prior discussion topic.

### Implementation for User Story 2

- [X] T008 [US2] Verify `detect_mode()` in `src/agents.py` only affects `system_prompt` selection — the `history` list in `chat.py:main()` is never reset or passed to `detect_mode()`
- [X] T009 [US2] Verify no `history.clear()` or `history = []` call anywhere in the message-processing loop except the explicit `limpar`/`clear` branch in `chat.py`
- [X] T010 [US2] Manual test: ask a question in tutor mode, then switch to flashcard mode — confirm prior conversation context is retained

**Checkpoint**: US2 verified — mode switching keeps history intact

---

## Phase 5: User Story 3 - Session Reset on Demand (Priority: P3)

**Goal**: `limpar`/`clear` command wipes history; next message has no prior context.

**Independent Test**: Chat for a few messages, type `limpar`, then ask a follow-up to an earlier message — bot should not reference any pre-clear content.

### Implementation for User Story 3

- [X] T011 [US3] Verify `history.clear()` is called when user types `limpar` or `clear` in `chat.py`
- [X] T012 [US3] Verify a confirmation message is printed after clear (e.g., "Histórico limpo.")
- [X] T013 [US3] Manual test: hold a conversation, run `limpar`, confirm next reply has no prior context

**Checkpoint**: US3 verified — on-demand reset working

---

## Phase 6: Polish & Cross-Cutting Concerns

**Purpose**: Trim behaviour, branch closure, and push to remote.

- [X] T014 [P] Verify trim logic: `history = history[-40:]` fires when `len(history) > 40` in `chat.py` — oldest messages dropped, newest retained
- [X] T015 [P] Verify no disk writes anywhere in `chat.py` or `src/` related to history (grep for `open(`, `json.dump`, `pickle`)
- [X] T016 Commit all spec artifacts: `git add -A && git commit -m "feat: session persistence verified and documented"`
- [X] T017 Push branch: `git push origin 002-session-persistence`
- [X] T018 [P] Update `README.md` if needed to mention multi-turn conversation support

---

## Dependencies

```
T001
 └── T002, T003, T004 (can run in parallel)
      └── T005 → T006 → T007  (US1)
      └── T008 → T009 → T010  (US2, parallel with US1)
      └── T011 → T012 → T013  (US3, parallel with US1/US2)
           └── T014, T015 (parallel polish)
                └── T016 → T017 → T018
```

## Parallel Execution per Story

```
After T001–T004 (foundation):
  [US1: T005→T006→T007]   ←─ can run simultaneously with US2 and US3
  [US2: T008→T009→T010]   ←─ can run simultaneously with US1 and US3
  [US3: T011→T012→T013]   ←─ can run simultaneously with US1 and US2
Then: T014, T015 (parallel) → T016 → T017 → T018
```

## Implementation Strategy

**MVP scope**: T001–T007 (US1 alone) — confirms multi-turn context works.  
**Full delivery**: T001–T018 — all stories verified, branch pushed.

Since all code already exists, each task is a verification step that takes minutes. Total estimated effort: ~30 minutes of manual testing + commit/push.
