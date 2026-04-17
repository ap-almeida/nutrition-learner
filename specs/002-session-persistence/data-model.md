# Data Model: Session Conversation Persistence

**Feature**: 002-session-persistence  
**Date**: 2026-04-17

---

## Entities

### Message

A single exchange unit in the conversation.

| Field | Type | Values | Description |
|-------|------|--------|-------------|
| `role` | `str` | `"user"` \| `"assistant"` | Who sent the message |
| `content` | `str` | Any non-empty string | Text content of the message |

Represented as a plain Python `dict`: `{"role": "user", "content": "..."}`.

---

### Session History

An ordered list of `Message` objects maintained in memory for the lifetime of one `chat.py` process.

| Property | Value |
|----------|-------|
| Type | `list[dict]` |
| Scope | Single process execution |
| Max size | 40 messages (20 user + 20 assistant turns) |
| Persistence | In-memory only — discarded on exit |
| Owner | `main()` in `chat.py` — variable `history` |

**Lifecycle**:

```
process start → history = []
  ↓ (each successful exchange)
history.append({role: user, content: msg})
history.append({role: assistant, content: reply})
  ↓ (if len > 40)
history = history[-40:]
  ↓ (on limpar/clear command)
history.clear()
  ↓
process exit → history discarded
```

---

## Message Flow to LLM

```
[system prompt (mode-specific)]
+ [history[0] … history[n]]    ← all prior exchanges
+ [current user message]
→ LLM API call
→ reply appended to history
```

The system prompt is **not** stored in `history` — it is reconstructed on every call from `get_system_prompt(mode, knowledge_text)`. This means:

- System prompt can change across mode switches without corrupting history.
- History contains only user/assistant turns.
