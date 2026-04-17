# API Contract: Chat Endpoint

**Feature**: 001-nutrition-chatbot-ui  
**Date**: 2026-04-17

## POST /api/chat

Send a user message and receive a chatbot response.

### Request

```json
{
  "message": "string (required, 1-5000 chars, user's question or input)"
}
```

**Headers**:
- `Content-Type: application/json`
- `Cookie: session_id=<uuid>` (set automatically by the server)

### Response — Success (200)

```json
{
  "reply": "string (chatbot response text, may contain markdown)",
  "message_type": "chat | flashcard | exam_question | exam_feedback",
  "session_id": "string (UUID, for reference)"
}
```

### Response — Validation Error (400)

```json
{
  "error": "string (human-readable error message)"
}
```

Triggered when:
- `message` is empty or whitespace-only
- `message` exceeds 5000 characters

### Response — Server Error (500)

```json
{
  "error": "string (generic error message, no internals exposed)"
}
```

Triggered when:
- LLM API is unreachable or returns an error
- Unexpected server-side failure

---

## GET /api/history

Retrieve the conversation history for the current session.

### Request

**Headers**:
- `Cookie: session_id=<uuid>`

### Response — Success (200)

```json
{
  "messages": [
    {
      "id": "string (UUID)",
      "role": "user | assistant",
      "content": "string",
      "message_type": "chat | flashcard | exam_question | exam_feedback",
      "timestamp": "string (ISO 8601)"
    }
  ],
  "session_id": "string (UUID)"
}
```

### Response — No Session (200)

```json
{
  "messages": [],
  "session_id": "string (new UUID, new session created)"
}
```

---

## GET /api/modules

List available course modules (extracted from PDFs).

### Response — Success (200)

```json
{
  "modules": [
    {
      "filename": "string",
      "title": "string (cleaned display name)",
      "page_count": "integer"
    }
  ]
}
```

---

## GET /

Serve the chat UI (HTML page).

### Response — Success (200)

Returns the HTML page with embedded CSS and JavaScript for the chat interface.

---

## Error Handling Contract

All error responses follow the same shape:

```json
{
  "error": "string (human-readable, safe to display to user)"
}
```

No stack traces, internal paths, or sensitive information are ever included in error responses.
