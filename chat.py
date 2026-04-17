#!/usr/bin/env python3
"""Nutrition Study Chatbot — terminal interface."""

import os
import sys
import textwrap

from dotenv import load_dotenv

# ---------------------------------------------------------------------------
# Cross-platform color support
# ---------------------------------------------------------------------------
try:
    import colorama
    colorama.init(autoreset=True)
    GREEN   = "\033[92m"
    YELLOW  = "\033[93m"
    CYAN    = "\033[96m"
    RED     = "\033[91m"
    BOLD    = "\033[1m"
    DIM     = "\033[2m"
    RESET   = "\033[0m"
except ImportError:
    GREEN = YELLOW = CYAN = RED = BOLD = DIM = RESET = ""

# ---------------------------------------------------------------------------
# Load env and imports
# ---------------------------------------------------------------------------
load_dotenv()

from src.knowledge import build_knowledge_text, extract_modules  # noqa: E402
from src.agents import get_reply  # noqa: E402

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
OPENAI_BASE_URL = os.getenv("OPENAI_BASE_URL") or None
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini")

WIDTH = 80  # wrap width for bot replies

MODE_LABELS = {
    "tutor":    f"{GREEN}[Tutor]{RESET}",
    "flashcard": f"{YELLOW}[Flashcards]{RESET}",
    "exam":     f"{CYAN}[Exame]{RESET}",
}

HELP_TEXT = f"""
{BOLD}Comandos disponíveis:{RESET}
  {GREEN}ajuda{RESET} / {GREEN}help{RESET}       Mostrar esta mensagem
  {GREEN}limpar{RESET} / {GREEN}clear{RESET}      Limpar o histórico da conversa
  {GREEN}sair{RESET} / {GREEN}exit{RESET} / {GREEN}quit{RESET}  Sair do chatbot

{BOLD}Modos de uso:{RESET}
  Faz qualquer pergunta sobre nutrição  → modo Tutor
  Escreve "flashcards sobre [tema]"     → modo Flashcards
  Escreve "exame sobre [tema]"          → modo Exame
"""


def print_header(modules):
    print()
    print(f"{BOLD}{GREEN}{'='*WIDTH}{RESET}")
    print(f"{BOLD}{GREEN}  🥗  Nutrição Chatbot  —  Assistente de Estudo{RESET}")
    print(f"{BOLD}{GREEN}{'='*WIDTH}{RESET}")
    print(f"{DIM}  Módulos carregados: {len(modules)}{RESET}")
    for m in modules:
        print(f"{DIM}    • {m['title']} ({m['page_count']} páginas){RESET}")
    print(f"{BOLD}{GREEN}{'='*WIDTH}{RESET}")
    print(f"  Escreve {GREEN}ajuda{RESET} para ver os comandos disponíveis.")
    print(f"  Escreve {GREEN}sair{RESET} para terminar.")
    print(f"{BOLD}{GREEN}{'='*WIDTH}{RESET}")
    print()


def wrap_reply(text):
    """Wrap long lines in a reply for terminal readability."""
    lines = text.splitlines()
    wrapped = []
    for line in lines:
        if len(line) <= WIDTH:
            wrapped.append(line)
        else:
            wrapped.extend(textwrap.wrap(line, width=WIDTH, subsequent_indent="  "))
    return "\n".join(wrapped)


def print_bot(reply, mode):
    label = MODE_LABELS.get(mode, MODE_LABELS["tutor"])
    print(f"\n{label}")
    print(f"{wrap_reply(reply)}")
    print()


def print_user_prompt():
    return input(f"{BOLD}Tu:{RESET} ").strip()


def check_api_key():
    if not OPENAI_API_KEY or OPENAI_API_KEY == "your-api-key-here":
        print(f"\n{RED}Erro: OPENAI_API_KEY não está configurada.{RESET}")
        print("Edita o ficheiro .env e define a tua API key:")
        print("  OPENAI_API_KEY=sk-...")
        print("\nSe não tens uma key, podes usar Ollama (local) com:")
        print("  OPENAI_BASE_URL=http://localhost:11434/v1")
        print("  OPENAI_API_KEY=ollama")
        print("  OPENAI_MODEL=llama3.2\n")
        sys.exit(1)


def main():
    check_api_key()

    # Load PDFs from the same directory as this script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    modules = extract_modules(script_dir)

    if not modules:
        print(f"{RED}Aviso: Nenhum PDF encontrado em {script_dir}{RESET}")
        print("Certifica-te de que os ficheiros PDF estão na mesma pasta que este script.")

    knowledge_text = build_knowledge_text(modules)
    print_header(modules)

    history = []  # [{role: user|assistant, content: str}, ...]

    while True:
        try:
            message = print_user_prompt()
        except (EOFError, KeyboardInterrupt):
            print(f"\n{DIM}Até logo!{RESET}")
            break

        if not message:
            continue

        lower = message.lower()

        if lower in ("sair", "exit", "quit", "q"):
            print(f"\n{DIM}Até logo!{RESET}\n")
            break

        if lower in ("ajuda", "help", "h"):
            print(HELP_TEXT)
            continue

        if lower in ("limpar", "clear"):
            history.clear()
            print(f"{DIM}  Histórico limpo.{RESET}\n")
            continue

        print(f"{DIM}  A processar...{RESET}", end="\r")

        try:
            reply, mode = get_reply(
                message,
                history,
                knowledge_text,
                api_key=OPENAI_API_KEY,
                base_url=OPENAI_BASE_URL,
                model=OPENAI_MODEL,
            )
        except Exception as e:
            err = str(e)
            if "insufficient_quota" in err or "quota" in err.lower():
                print(f"\n{RED}Erro: A tua quota OpenAI está esgotada.{RESET}")
                print("Adiciona créditos em https://platform.openai.com/settings/billing")
                print("Ou usa Ollama local — edita o .env com OPENAI_BASE_URL=http://localhost:11434/v1\n")
            elif "401" in err or "Unauthorized" in err or "invalid_api_key" in err:
                print(f"\n{RED}Erro: API key inválida. Verifica o ficheiro .env.{RESET}\n")
            elif "Connection" in err or "connect" in err.lower():
                print(f"\n{RED}Erro: Não foi possível ligar à API. Verifica a ligação à internet.{RESET}\n")
            else:
                print(f"\n{RED}Erro inesperado: {err[:200]}{RESET}\n")
            continue

        # Keep history for context continuity
        history.append({"role": "user", "content": message})
        history.append({"role": "assistant", "content": reply})

        # Trim to last 20 exchanges (40 messages) to avoid context overflow
        if len(history) > 40:
            history = history[-40:]

        print_bot(reply, mode)


if __name__ == "__main__":
    main()
