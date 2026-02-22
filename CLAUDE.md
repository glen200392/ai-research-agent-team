# AI Research Agent Team — Claude Code Integration

This file tells Claude Code how to work with this project.
Read it fully before making any changes.

## Project Purpose

Automated AI technology intelligence system with three specialized agent teams:

- **Team A** (implemented): Monthly/weekly research reports — scrapes AI news, analyzes, writes Traditional Chinese reports in 3 formats
- **Team B** (implemented): Evolution Chronicle — traces historical lineage of AI technologies mentioned in Team A reports
- **Team C** (implemented): Pedagogy Federation — converts research into 3-level educational content + quiz

All three teams share a unified provider abstraction (`core/providers.py`) that supports cloud APIs (Anthropic, OpenAI, Google) and local models (Ollama, LM Studio, any OpenAI-compatible endpoint).

## Directory Layout

```
CLAUDE.md                  ← you are here
run.py                     ← universal entry point (all teams)
setup.sh                   ← interactive first-run setup
Dockerfile / docker-compose.yml
core/
  providers.py             ← universal LLM factory (ALL provider types)
  env_detector.py          ← probe environment for available providers
config/
  config.yaml              ← main pipeline config (safe to edit)
env.example                ← copy to .env and fill in keys
frameworks/langgraph/
  nodes.py                 ← Team A agent nodes
  nodes_team_b.py          ← Team B agent nodes
  nodes_team_c.py          ← Team C agent nodes
  graph.py / graph_team_b.py / graph_team_c.py
prompts/
  01-07_*.md               ← Team A system prompts
  team_b/08_*.md           ← Team B system prompts
  team_c/10_*.md           ← Team C system prompts
reports/                   ← Team A output (monthly reports)
docs/evolution-chronicle/  ← Team B cumulative output
pedagogy/weekly-lessons/   ← Team C output
```

## Setup (first time on a new machine)

```bash
# 1. Copy and fill environment file
cp env.example .env
# Edit .env — minimum required: one LLM key + one search API key

# 2. Run interactive setup (validates env, installs deps)
bash setup.sh

# 3. Detect available providers
python run.py detect

# 4. Dry-run to validate config
python run.py team-a --dry-run
```

## Common Commands

```bash
# Run Team A monthly report (uses last month by default)
python run.py team-a

# Run Team A for a specific month
python run.py team-a --month 2026-02

# Run Team B (reads latest Team A report, updates evolution chronicle)
python run.py team-b

# Run Team B against a specific report
python run.py team-b --report reports/AI_Tech_Report_2026_02.md

# Run Team C (reads latest report + evolution context, generates lesson)
python run.py team-c

# Run all three teams in sequence
python run.py all --month 2026-02

# Detect available LLM providers
python run.py detect

# Validate config without executing agents
python run.py team-a --dry-run

# Run with a specific provider override
DEFAULT_LLM_PROVIDER=ollama python run.py team-a

# Run with local Ollama
OLLAMA_MODEL=llama3.2 python run.py team-b
```

## LLM Provider Configuration

Set `DEFAULT_LLM_PROVIDER` in `.env` to one of:

| Value | Requires | Notes |
|-------|----------|-------|
| `anthropic` | `ANTHROPIC_API_KEY` | Best quality (default) |
| `openai` | `OPENAI_API_KEY` | GPT-4o |
| `google` | `GOOGLE_API_KEY` | Gemini |
| `ollama` | Ollama running locally | Free, private |
| `lmstudio` | LM Studio running locally | Free, private, GUI |
| `openai_compatible` | `CUSTOM_API_BASE_URL` | Any compatible endpoint |

Auto-detection: if `DEFAULT_LLM_PROVIDER` is unset, the system tries providers in priority order (Anthropic → OpenAI → Google → Ollama → LM Studio → custom).

## Per-Agent Model Overrides

In `config/config.yaml` under `llm.agent_models`, each agent can use a different model:

```yaml
llm:
  provider: "anthropic"
  agent_models:
    intel_collector:
      provider: "ollama"     # use free local model for search
      model: "llama3.2"
    content_synthesizer:
      provider: "anthropic"  # use best model for writing
      model: "claude-opus-4-6"
```

## Architecture Constraints

- **Never hardcode API keys** — always use `os.getenv()`
- **Never commit `.env`** — it's in `.gitignore`
- **JSON parsing**: use `_extract_json()` from `nodes.py`, never bare `re.search(r"\{.*\}")`
- **LLM factory**: always use `core.providers.get_llm(config, agent_name)`, never instantiate models directly
- **State flows**: Team A → Team B → Team C (each reads previous team's output files)
- **Output directories**: `reports/` (Team A), `docs/evolution-chronicle/` (Team B), `pedagogy/` (Team C)

## Running with Docker

```bash
# Cloud providers (set keys in .env)
docker compose up app

# With local Ollama (pulls and runs Ollama as a sidecar)
docker compose --profile local up

# Pull a model into the Ollama container
docker compose exec ollama ollama pull llama3.2
```

## Adding a New Agent

1. Add system prompt to `prompts/` (follow XML format in existing prompts)
2. Add node function to the appropriate `nodes_team_*.py`
3. Register node in the corresponding `graph_team_*.py`
4. Update state schema in `state_team_*.py` if new fields are needed
5. Always call `get_llm(state["config"], agent_name="your_agent")` for the LLM

## Testing

```bash
# Syntax check all Python files
python -m py_compile frameworks/langgraph/nodes.py core/providers.py

# Dry run (no API calls)
python run.py team-a --dry-run

# Detect environment
python run.py detect
```
