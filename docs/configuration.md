# Configuration

yoker-writing-assistant has two configuration concerns, kept strictly
separate: the Yoker runtime (`~/.yoker.toml`) and the optional researcher
integration. Neither is committed to the repo; a reference template
(`yoker.toml`) is shipped for documentation only.

## Yoker runtime — `~/.yoker.toml`

The backend, model, permissions, plugin registration, and UI settings all
live in `~/.yoker.toml`. This file is created by Yoker's bootstrap wizard
(`uv run yoker init`) or by the writing assistant's built-in bootstrap on
first run. It is never committed to the repo.

### The `enabled` kill-switch

Yoker requires `enabled = true` at the top level of `~/.yoker.toml`. This
is a global kill-switch: when set to `false` (or absent), Yoker refuses to
run. The bootstrap wizard writes it as `enabled = false` — you must
manually set it to `true` to acknowledge the risks of running an
LLM-powered agent before Yoker will start.

### Required sections

The minimal `~/.yoker.toml` for the writing assistant:

```toml
enabled = true

[backend]
provider = "ollama"

[backend.ollama]
base_url = "https://ollama.com"
api_key = "${OLLAMA_API_KEY}"
model = "glm-5.2:cloud"

[plugins]
enabled = true

[plugins.trusted]
yoker_writing_assistant = true
```

The `[plugins.trusted]` block marks this package as a trusted plugin. When
running interactively, Yoker's trust gate prompts on first load; when
running unattended, the trust must be pre-configured. Marking the package
trusted admits all agent and skill code from this package with no per-call
gate — pin the installed version and verify the source.

### Reference template

The `yoker.toml` file in this repo is a reference template showing the full
configuration shape. It includes:

- `[backend]` — LLM provider and model
- `[context]` — session persistence and context-window management
- `[permissions]` — filesystem paths, network access, protected files
- `[tools]` — per-tool configuration (enabled, limits, guardrails)
- `[agents.directories]` — external agent directories (e.g., for the
  optional researcher)
- `[skills.directories]` — external skill directories
- `[plugins]` — plugin registration and trust
- `[logging]` — log level and format
- `[ui]` — UI mode and display options

Copy the sections you need into `~/.yoker.toml` and adjust for your
backend. Do not use the repo `yoker.toml` as an active runtime config — it
would clobber your backend settings during local development.

## Optional: researcher integration

The writing assistant can delegate research tasks to `c3:researcher`, an
external research agent. To enable it, add to `~/.yoker.toml`:

```toml
[agents.directories]
c3 = "../c3/agents"
```

### What the researcher adds

- `c3:researcher` — a research agent with web search, content fetching, and
  provenance tracking. The writing assistant delegates all research tasks
  to this agent via `yoker:agent`.

### What happens without the researcher

If the researcher is not configured, research delegation is unavailable.
The agent falls back to direct web search using `yoker:websearch` and
`yoker:webfetch`. The limitation is noted in the "What this did NOT check"
section of the agent's output. All other functionality (review, continuity,
voice, mistakes, idioms, split, reorder, copy-writer) works without it.

## The voice profile — `~/VOICE.md`

The voice profile at `~/VOICE.md` is created by the author and contains:

- Quantitative metrics (function-word frequencies, sentence-length
  distributions)
- Explicit anti-patterns (words and patterns to avoid)
- Voice characteristics and register markers

The profile is a **measurement instrument only** — the skill uses it to
detect drift, never to generate text "in the author's voice." If the file
is absent, the voice pass is skipped entirely and the agent tells the
author no voice checks ran.

The profile is a snapshot: it may not include the author's most recent
work. Flagged terms are cross-referenced against the source material before
reporting drift. The agent may propose updating the profile as a
`TODO PROPOSAL:` for the author to decide.