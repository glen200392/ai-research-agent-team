"""
Universal LLM Provider Factory
================================
Supports cloud APIs and local model servers with automatic detection.

Providers supported:
  - anthropic       : Claude via Anthropic API
  - openai          : GPT via OpenAI API
  - google          : Gemini via Google AI API
  - ollama          : Local models via Ollama (http://localhost:11434)
  - lmstudio        : Local models via LM Studio OpenAI-compatible API
  - openai_compatible: Any custom OpenAI-compatible endpoint

Resolution order (per call):
  1. Per-agent model override in config.llm.agent_models
  2. Global config.llm.provider
  3. DEFAULT_LLM_PROVIDER environment variable
  4. Auto-detect from available API keys / running local services
"""

import os
from typing import Optional


def get_llm(config: dict, agent_name: Optional[str] = None):
    """
    Return a configured LangChain chat model.

    Args:
        config:     Full pipeline config dict (from config.yaml)
        agent_name: Optional agent identifier for per-agent overrides
                    (e.g. 'intel_collector', 'tech_analyst')
    """
    llm_cfg = config.get("llm", {})
    temp = llm_cfg.get("temperature", 0.3)
    max_tokens = llm_cfg.get("max_tokens", 8192)
    timeout = llm_cfg.get("timeout_seconds", 120)

    provider = _resolve_provider(llm_cfg, agent_name)
    model = _resolve_model(llm_cfg, provider, agent_name)

    return _build_llm(provider, model, temp, max_tokens, timeout)


# ── Internal helpers ──────────────────────────────────────────────────────────

def _resolve_provider(llm_cfg: dict, agent_name: Optional[str]) -> str:
    # 1. Per-agent override
    if agent_name:
        override = llm_cfg.get("agent_models", {}).get(agent_name) or {}
        if isinstance(override, dict) and override.get("provider"):
            return override["provider"].lower()

    # 2. Global config
    configured = (llm_cfg.get("provider") or "").lower()
    if configured and configured != "auto":
        return configured

    # 3. Environment variable
    env_provider = os.getenv("DEFAULT_LLM_PROVIDER", "").lower()
    if env_provider and env_provider not in ("", "auto"):
        return env_provider

    # 4. Auto-detect
    return _auto_detect_provider()


def _resolve_model(llm_cfg: dict, provider: str, agent_name: Optional[str]) -> Optional[str]:
    # Per-agent model override
    if agent_name:
        override = llm_cfg.get("agent_models", {}).get(agent_name) or {}
        if isinstance(override, dict) and override.get("model"):
            return override["model"]

    # Provider env-var defaults
    _env_defaults = {
        "anthropic":        os.getenv("ANTHROPIC_MODEL",  "claude-opus-4-6"),
        "openai":           os.getenv("OPENAI_MODEL",     "gpt-4o"),
        "google":           os.getenv("GOOGLE_MODEL",     "gemini-2.0-flash"),
        "ollama":           os.getenv("OLLAMA_MODEL",     "llama3.2"),
        "lmstudio":         os.getenv("LMSTUDIO_MODEL",   "local-model"),
        "openai_compatible": os.getenv("CUSTOM_MODEL",   "default"),
    }
    return _env_defaults.get(provider)


def _auto_detect_provider() -> str:
    """Detect the best available provider from the current environment."""
    # Cloud keys take priority (deterministic)
    if os.getenv("ANTHROPIC_API_KEY"):
        return "anthropic"
    if os.getenv("OPENAI_API_KEY"):
        return "openai"
    if os.getenv("GOOGLE_API_KEY"):
        return "google"

    # Local services
    if _is_ollama_running():
        return "ollama"
    if _is_lmstudio_running():
        return "lmstudio"
    if os.getenv("CUSTOM_API_BASE_URL"):
        return "openai_compatible"

    raise RuntimeError(
        "No LLM provider available.\n"
        "  Cloud: set ANTHROPIC_API_KEY, OPENAI_API_KEY, or GOOGLE_API_KEY\n"
        "  Local: start Ollama (ollama serve) or LM Studio, or set CUSTOM_API_BASE_URL"
    )


def _build_llm(provider: str, model: Optional[str], temp: float, max_tokens: int, timeout: int):
    """Instantiate and return the appropriate LangChain chat model object."""

    if provider == "anthropic":
        from langchain_anthropic import ChatAnthropic
        return ChatAnthropic(
            model=model or "claude-opus-4-6",
            temperature=temp,
            max_tokens=max_tokens,
            timeout=timeout,
            api_key=os.getenv("ANTHROPIC_API_KEY"),
        )

    if provider == "openai":
        from langchain_openai import ChatOpenAI
        return ChatOpenAI(
            model=model or "gpt-4o",
            temperature=temp,
            max_tokens=max_tokens,
            timeout=timeout,
            api_key=os.getenv("OPENAI_API_KEY"),
        )

    if provider == "google":
        from langchain_google_genai import ChatGoogleGenerativeAI
        return ChatGoogleGenerativeAI(
            model=model or "gemini-2.0-flash",
            temperature=temp,
            google_api_key=os.getenv("GOOGLE_API_KEY"),
        )

    if provider == "ollama":
        from langchain_ollama import ChatOllama
        return ChatOllama(
            model=model or "llama3.2",
            temperature=temp,
            base_url=os.getenv("OLLAMA_BASE_URL", "http://localhost:11434"),
        )

    if provider == "lmstudio":
        from langchain_openai import ChatOpenAI
        base = os.getenv("LMSTUDIO_BASE_URL", "http://localhost:1234").rstrip("/")
        return ChatOpenAI(
            model=model or "local-model",
            temperature=temp,
            max_tokens=max_tokens,
            base_url=f"{base}/v1",
            api_key="lm-studio",  # LM Studio ignores the key value
        )

    if provider == "openai_compatible":
        from langchain_openai import ChatOpenAI
        base_url = os.getenv("CUSTOM_API_BASE_URL", "").rstrip("/")
        if not base_url:
            raise ValueError(
                "CUSTOM_API_BASE_URL env var is required for openai_compatible provider"
            )
        return ChatOpenAI(
            model=model or os.getenv("CUSTOM_MODEL", "default"),
            temperature=temp,
            max_tokens=max_tokens,
            base_url=base_url,
            api_key=os.getenv("CUSTOM_API_KEY", "none"),
        )

    raise ValueError(
        f"Unknown LLM provider: {provider!r}\n"
        "Valid values: anthropic, openai, google, ollama, lmstudio, openai_compatible"
    )


# ── Service discovery helpers ─────────────────────────────────────────────────

def _is_ollama_running(host: Optional[str] = None) -> bool:
    host = host or os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
    try:
        import httpx
        return httpx.get(f"{host}/api/tags", timeout=2.0).status_code == 200
    except Exception:
        return False


def _is_lmstudio_running(host: Optional[str] = None) -> bool:
    host = host or os.getenv("LMSTUDIO_BASE_URL", "http://localhost:1234")
    try:
        import httpx
        return httpx.get(f"{host}/v1/models", timeout=2.0).status_code == 200
    except Exception:
        return False


def list_available_providers() -> dict:
    """
    Probe the environment and return a dict of all reachable providers.
    Used by env_detector and the 'detect' CLI command.
    """
    available = {}

    if os.getenv("ANTHROPIC_API_KEY"):
        available["anthropic"] = {
            "status": "ready",
            "model": os.getenv("ANTHROPIC_MODEL", "claude-opus-4-6"),
        }
    if os.getenv("OPENAI_API_KEY"):
        available["openai"] = {
            "status": "ready",
            "model": os.getenv("OPENAI_MODEL", "gpt-4o"),
        }
    if os.getenv("GOOGLE_API_KEY"):
        available["google"] = {
            "status": "ready",
            "model": os.getenv("GOOGLE_MODEL", "gemini-2.0-flash"),
        }

    ollama_host = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
    if _is_ollama_running(ollama_host):
        available["ollama"] = {
            "status": "running",
            "host": ollama_host,
            "models": _get_ollama_models(ollama_host),
        }

    lmstudio_host = os.getenv("LMSTUDIO_BASE_URL", "http://localhost:1234")
    if _is_lmstudio_running(lmstudio_host):
        available["lmstudio"] = {"status": "running", "host": lmstudio_host}

    if os.getenv("CUSTOM_API_BASE_URL"):
        available["openai_compatible"] = {
            "status": "configured",
            "url": os.getenv("CUSTOM_API_BASE_URL"),
            "model": os.getenv("CUSTOM_MODEL", "default"),
        }

    return available


def _get_ollama_models(host: str) -> list:
    try:
        import httpx
        resp = httpx.get(f"{host}/api/tags", timeout=3.0)
        if resp.status_code == 200:
            return [m["name"] for m in resp.json().get("models", [])]
    except Exception:
        pass
    return []
