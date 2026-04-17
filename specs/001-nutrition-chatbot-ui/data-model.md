# Data Model: Nutrition Chatbot Web UI

**Feature**: 001-nutrition-chatbot-ui  
**Date**: 2026-04-17

## Entities

### Session

Represents a single browser session with the chatbot.

| Field | Type | Description |
|-------|------|-------------|
| session_id | string (UUID) | Unique identifier, stored in browser cookie |
| messages | list[Message] | Ordered conversation history |
| created_at | datetime | When the session was created |
| last_active | datetime | Last interaction timestamp, used for TTL cleanup |
| active_mode | enum | Current agent mode: `tutor`, `flashcard`, `exam` |

**Validation rules**:
- `session_id` must be a valid UUID v4
- `messages` list has a maximum length (to prevent unbounded memory growth; configurable, default 100)
- Sessions are purged after 2 hours of inactivity based on `last_active`

---

### Message

An individual exchange unit in a conversation.

| Field | Type | Description |
|-------|------|-------------|
| id | string (UUID) | Unique message identifier |
| role | enum | `user` or `assistant` |
| content | string | The message text (plain text or markdown) |
| timestamp | datetime | When the message was created |
| message_type | enum | `chat`, `flashcard`, `exam_question`, `exam_feedback` |

**Validation rules**:
- `content` must not be empty or whitespace-only
- `content` maximum length: 5000 characters (user messages)
- `role` must be one of `user`, `assistant`
- `message_type` must be one of `chat`, `flashcard`, `exam_question`, `exam_feedback`

---

### CourseModule

Represents extracted content from a single PDF file.

| Field | Type | Description |
|-------|------|-------------|
| filename | string | Original PDF filename |
| title | string | Cleaned display name derived from filename |
| content | string | Extracted text content from the PDF |
| page_count | integer | Number of pages in the source PDF |

**Validation rules**:
- `content` must not be empty (PDF extraction must yield text)
- `filename` must end in `.pdf`

---

### FlashcardSet

A generated collection of Q&A flashcard pairs.

| Field | Type | Description |
|-------|------|-------------|
| topic | string | The topic the flashcards cover |
| cards | list[Flashcard] | Ordered list of flashcard pairs |

### Flashcard

| Field | Type | Description |
|-------|------|-------------|
| question | string | The flashcard question |
| answer | string | The flashcard answer |

---

### ExamQuestionSet

A generated set of practice exam questions.

| Field | Type | Description |
|-------|------|-------------|
| topic | string | The topic the exam covers |
| questions | list[ExamQuestion] | Ordered list of exam questions |

### ExamQuestion

| Field | Type | Description |
|-------|------|-------------|
| id | integer | Question number (1-based) |
| question | string | The exam question text |
| expected_answer | string | The model answer (not shown to user until they respond) |

---

## Relationships

```
Session 1──* Message
Session 1──1 active_mode (enum, determines agent routing)

CourseModule *──* Session (modules provide context for LLM prompts)

Message.message_type determines rendering:
  - "chat" → standard text bubble
  - "flashcard" → card-style layout with Q/A pairs
  - "exam_question" → question with answer input
  - "exam_feedback" → scored feedback display
```

## State Transitions

### Session Lifecycle
```
[New Visit] → ACTIVE → (interaction) → ACTIVE → (2h inactivity) → EXPIRED → [Purged]
     ↓                                    ↑
  [Page Refresh] ─────────────────────────┘ (new session)
```

### Agent Mode Transitions
```
[Default: tutor] ←→ [flashcard] (user requests flashcards)
[Default: tutor] ←→ [exam] (user requests practice exam)
[flashcard] ←→ [exam] (user switches mode via keywords)
```
Mode switches happen automatically based on message intent detection. The mode reverts to `tutor` for general questions.
