# Quickstart: Session Conversation Persistence

**Feature**: 002-session-persistence  
**Date**: 2026-04-17

---

## What Was Built

Session conversation persistence is already active in the terminal chatbot. No installation or configuration is required — it works out of the box.

---

## How It Works

Every message you send and every response the bot gives is remembered for the duration of the current session. You can ask follow-up questions naturally:

```
Tu: O que é a glicémia?
[Tutor] A glicémia refere-se à concentração de glucose no sangue...

Tu: Como se relaciona com a diabetes?
[Tutor] Como discutimos, a glicémia elevada de forma crónica é a base da diabetes...
```

---

## Commands That Affect History

| Command | Effect |
|---------|--------|
| `limpar` / `clear` | Wipes all conversation history — fresh start |
| `sair` / `exit` / `quit` | Exits the program — history is discarded |

---

## Limits

- History is trimmed to the last **40 messages** (20 exchanges) automatically when it grows beyond that. This prevents hitting the model's context window limit.
- History lives **in memory only** — it is not saved to disk and does not carry over to the next run of the program.

---

## Running the Chatbot

```bash
# Linux/macOS
./run.sh

# Windows
run.bat

# Manual
source venv/bin/activate && python chat.py
```
