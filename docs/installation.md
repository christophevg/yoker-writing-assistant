# Installation

## Prerequisites

- Python 3.10 or newer
- [uv](https://docs.astral.sh/uv/) for dependency management
- A Yoker backend: either a local [Ollama](https://ollama.com) install or a
  cloud LLM provider API key

## Install the package

### Option A: Run directly with uvx (no checkout needed)

```bash
uvx yoker-writing-assistant
```

This downloads the package from PyPI and launches the writing assistant in
one command. Additional CLI flags (e.g., `--ui-mode batch`) can be appended.

### Option B: From a local checkout

```bash
git clone https://github.com/christophevg/yoker-writing-assistant.git
cd yoker-writing-assistant
make env-dev        # uv sync --all-extras (runtime + dev + docs)
make test           # sanity check
make run            # launch the writing assistant
```

### Option C: Via the Yoker CLI directly

```bash
yoker --with yoker_writing_assistant --agent-name yoker_writing_assistant:writing-assistant
```

This loads the plugin (`--with yoker_writing_assistant`) and selects the
writing assistant as the primary agent (`--agent-name`). Any additional CLI
flags can be appended.

## Backend setup

Yoker needs a configured backend before the writing assistant can reason.
The backend (provider, base URL, API key, model) lives in `~/.yoker.toml`.
If you do not already have one, run Yoker's bootstrap wizard once:

```bash
uv run yoker init    # writes ~/.yoker.toml with a backend of your choice
```

Alternatively, the first time you run `yoker-writing-assistant` without an
existing `~/.yoker.toml`, the built-in bootstrap wizard launches
interactively to guide you through configuration.

The `yoker.toml` in this repo is a reference template — it shows the shape
of the config but is not an active runtime config. Copy the relevant
sections into `~/.yoker.toml` (never committed) and adjust for your
backend.

## Optional: researcher integration

The writing assistant can delegate research tasks to `c3:researcher`, an
external research agent. To enable it, add to `~/.yoker.toml`:

```toml
[agents.directories]
c3 = "../c3/agents"
```

If the researcher is not configured, research delegation is unavailable.
The agent falls back to direct web search (`yoker:websearch` /
`yoker:webfetch`) and notes the limitation in its output. All other
functionality works without it. See [Configuration](configuration.md) for
the full reference.

## Verify the install

```bash
make run
```

The writing assistant launches and presents its interactive prompt. If no
configuration is found, the bootstrap wizard runs first. Once configured,
the agent is ready for a writing coaching session.

See [Quickstart](quickstart.md) for a worked example.