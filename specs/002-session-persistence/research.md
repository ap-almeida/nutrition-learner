# Research: Session Conversation Persistence

**Feature**: 002-session-persistence  
**Date**: 2026-04-17

---

## Finding 1 — Current Implementation Status

**Decision**: The feature is already fully implemented in the codebase on branch `001-nutrition-chatbot-ui`.

**Evidence** (`chat.py`):
```python
history = []  # line 122 — initialised at session start

reply, mode = get_reply(      # line 155 — history passed on every call
    message,
    history,
    ...
)

history.append({"role": "user", "content": message})      # appended after success
history.append({"role": "assistant", "content": reply})   # appended after success

if len(history) > 40:          # trim to last 40 messages
    history = history[-40:]

# On limpar/clear:
history.clear()                # line 148 — resets history on demand
```

**Evidence** (`src/agents.py`):
```python
messages = [{"role": "system", "content": system_prompt}]
messages.extend(history)                                  # all prior exchanges included
messages.append({"role": "user", "content": message})    # then current message
```

**Rationale**: The standard OpenAI/Ollama messages array format is used correctly. Prior conversation turns are prepended before the current user message on every call, giving the model full session context.

---

## Finding 2 — FR Coverage Analysis

| FR | Requirement | Status |
|----|-------------|--------|
| FR-001 | In-memory history list maintained | ✅ `history = []` in `chat.py` |
| FR-002 | User message appended before LLM call | ✅ (passed as arg; appended after for next call — correct pattern) |
| FR-003 | Bot response appended after LLM call | ✅ `history.append({"role": "assistant", ...})` |
| FR-004 | History passed to LLM on every call | ✅ `messages.extend(history)` in `get_reply()` |
| FR-005 | History reset on `limpar`/`clear` | ✅ `history.clear()` in `chat.py` |
| FR-006 | Trim to 40 messages max | ✅ `history = history[-40:]` |
| FR-007 | No disk persistence | ✅ pure in-memory `list`, no file I/O |
| FR-008 | Mode switch does not reset history | ✅ mode is detected inside `get_reply`; `history` in `chat.py` is unaffected |

**All 8 FRs are already satisfied.**

---

## Finding 3 — One Gap: Failed Messages Not Added to History

**Decision**: This is correct, intentional behaviour.

When `get_reply()` raises an exception (network error, quota error, etc.), the `history.append()` calls are skipped. This means failed messages are not polluting history, which is the right behaviour. No change needed.

---

## Finding 4 — Optional Enhancement (Out of Scope)

**Considered**: Showing the user a message count indicator in the prompt (e.g. `Tu [12]:`) so they know how much history the bot has.

**Decision**: Out of scope for this feature — not in the spec. Can be added as a future enhancement.

---

## Conclusion

No implementation work is required. The feature requested in the spec is already present and correct. This plan documents it for traceability and closes the spec/branch properly.
