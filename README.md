# Nutrição Chatbot

Terminal chatbot for nutrition course study. Answers questions, generates flashcards, and creates practice exam questions — all grounded in the course PowerPoint content.

## Requirements

- Python 3.11 or later
- An OpenAI API key (or an [Ollama](https://ollama.com) local model)

## Setup & Run

### Linux / macOS

```bash
git clone <repo-url>
cd nutri
./run.sh
```

On first run, `run.sh` will create a `.env` file. Edit it and set your API key, then run again:

```bash
nano .env      # set OPENAI_API_KEY=sk-...
./run.sh
```

### Windows

```bat
git clone <repo-url>
cd nutri
run.bat
```

On first run, edit `.env` with Notepad, set `OPENAI_API_KEY=sk-...`, then run `run.bat` again.

### Manual setup (any OS)

```bash
python3 -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
# Edit .env and set OPENAI_API_KEY
python chat.py
```

## Environment Variables

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `OPENAI_API_KEY` | Yes | — | OpenAI API key (`sk-...`) |
| `OPENAI_BASE_URL` | No | OpenAI | Alternative API endpoint (e.g. Ollama) |
| `OPENAI_MODEL` | No | `gpt-4o-mini` | Model name |

### Using Ollama (free, local, no API key needed)

1. Install Ollama: https://ollama.com
2. Run: `ollama pull llama3.2`
3. Set in `.env`:
   ```
   OPENAI_BASE_URL=http://localhost:11434/v1
   OPENAI_API_KEY=ollama
   OPENAI_MODEL=llama3.2
   ```

## Usage

The chatbot remembers everything you say within a session — ask follow-up questions naturally without repeating context.

```
Tu: O que é uma abordagem integrada em nutrição?
Tu: Como se aplica isso à diabetes?         ← follow-up, context is remembered
Tu: flashcards sobre o Módulo 8 Tema 1
Tu: exame sobre inovação digital em nutrição
Tu: ajuda
Tu: limpar
Tu: sair
```

| Command | Effect |
|---------|--------|
| Any question | Answered by the Nutrition Tutor |
| `flashcards sobre [tema]` | Generates Q&A flashcards |
| `exame sobre [tema]` | Generates practice exam questions |
| `ajuda` / `help` | Show help |
| `limpar` / `clear` | Clear conversation history (start fresh) |
| `sair` / `exit` / `quit` | Exit |

> Session history is kept in memory only — it is not saved to disk and does not carry over to the next run. History is automatically trimmed to the last 20 exchanges to stay within model limits.

## Project Structure

```
chat.py          ← Main entry point (run this)
run.sh           ← Linux/macOS launcher
run.bat          ← Windows launcher
requirements.txt
.env.example
src/
  knowledge.py   ← PDF extraction
  prompts.py     ← System prompts (tutor / flashcard / exam)
  agents.py      ← LLM routing and API call
*.pdf            ← Course material (PDFs must be in this folder)
```
