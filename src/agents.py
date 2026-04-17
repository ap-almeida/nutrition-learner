import re

from openai import OpenAI

from src.prompts import get_system_prompt

# Keyword patterns for intent detection
_FLASHCARD_PATTERN = re.compile(
    r"\b(flashcards?|flash\s*cards?|cart[aã]o|cart[oõ]es)\b",
    re.IGNORECASE,
)
_EXAM_PATTERN = re.compile(
    r"\b(exam|quiz|practice|exame|teste|questões|questoes|prática|pratica)\b",
    re.IGNORECASE,
)


def detect_mode(message):
    """Detect the agent mode from the user's message content."""
    if _FLASHCARD_PATTERN.search(message):
        return "flashcard"
    if _EXAM_PATTERN.search(message):
        return "exam"
    return "tutor"


def get_reply(message, history, knowledge_text, api_key, base_url=None, model="gpt-4o-mini"):
    """Process a user message and return the LLM reply and detected mode.

    Args:
        message: The user's message string.
        history: List of {"role": ..., "content": ...} dicts (conversation so far).
        knowledge_text: Full course content string for the system prompt.
        api_key: OpenAI API key.
        base_url: Optional alternative API base URL.
        model: Model name to use.

    Returns:
        (reply_text, mode) tuple.
    """
    mode = detect_mode(message)
    system_prompt = get_system_prompt(mode, knowledge_text)

    messages = [{"role": "system", "content": system_prompt}]
    messages.extend(history)
    messages.append({"role": "user", "content": message})

    client_kwargs = {"api_key": api_key}
    if base_url:
        client_kwargs["base_url"] = base_url

    client = OpenAI(**client_kwargs)
    response = client.chat.completions.create(
        model=model,
        messages=messages,
    )

    reply = response.choices[0].message.content
    return reply, mode
