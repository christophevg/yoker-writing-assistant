# Yoker Writing Assistant

[![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)][pypi]
[![uv](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/uv/main/assets/badge/v0.json)][uv]
[![Yoker](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/christophevg/yoker/master/media/badge/v0.json)][yoker]
[![Agentic](https://img.shields.io/badge/workflow-agentic-blueviolet?style=flat-square)][agentic]


> A writing assistant that coaches and develops — but never writes for you.

This is a Yoker 1.0 pet-store showcase package. It demonstrates the
**yoker-as-runtime** mode: Yoker is the entry point, and this package
provides the main agent and skills for an interactive writing coaching
session. The agent interviews, challenges, reviews, and flags — but every
word of prose is written by the author.

## Status

Early setup phase. Agent and skill definitions exist from a prior
implementation (Claude Code / c3) and are being adapted to Yoker. The
Python package structure, plugin manifest, and entry point are pending.

## What It Does

The writing assistant is a **developmental editor + writing coach** for an
author who writes every word themselves. It operates on the
**declared-work scope**: it only acts on prose the author has already
written. It never generates prose, never rewrites, never fills blanks.

### Skills

| Skill | What it does |
|-------|-------------|
| `writing-review` | Developmental review, claim verification, gap/perspective analysis |
| `writing-continuity` | Dangling references, cold terms, dropped themes, missing transitions |
| `writing-voice` | Voice drift detection, ChatGPT smell flagging, voice profile checks |
| `writing-mistakes` | Common writing mistakes — eggcorns, redundancies, non-native errors, craft patterns |
| `writing-idioms` | Idiom/proverb misuse → canonical form as a proposal |
| `writing-split` | Long-form → sequential social post sequence |
| `writing-order` | Reorder raw material into smooth argument flow |
| `copy-writer` | Platform-specific content adaptation (Twitter, LinkedIn, Mastodon, etc.) |

### The Non-Negotiable Rule

The agent never writes prose. Every gap is marked `TODO:`, every proposal
is marked `TODO PROPOSAL:`. The author accepts, rejects, or writes. This is
the core design principle — friction is the value, not a bug.

## Quick Start

```bash
make env-dev                    # install all dependencies
make run                        # launch yoker chat with the writing assistant
```

Or run directly via the Yoker CLI:

```bash
yoker --with yoker_writing_assistant --agent yoker_writing_assistant:writing-assistant
```

A Yoker backend is a prerequisite — either a local
[Ollama](https://ollama.com) install or a cloud LLM provider API key. If
you do not already have one, run `uv run yoker init` once to write
`~/.yoker.toml` with a backend of your choice.

## Configuration

Runtime configuration lives in `~/.yoker.toml` (never committed). A
reference template is provided as `yoker.toml` in this repo. The key
sections:

- `[backend]` — LLM provider and model
- `[agents.directories]` — directories to scan for agent definitions
  (e.g., `c3 = "../c3/agents"` for the optional researcher agent)
- `[skills.directories]` — directories to scan for skill definitions
  (e.g., `c3 = "../c3/skills"` for c3 heritage skills)
- `[plugins]` — plugin registration (this package is loaded via
  `--with yoker-writing-assistant`)

### Optional: c3 Researcher

The writing assistant can delegate research tasks to `c3:researcher`, an
external agent from the [c3](../c3) project. To enable it, add to
`yoker.toml`:

```toml
[agents.directories]
c3 = "../c3/agents"
```

If c3 is not configured, research delegation is unavailable and the agent
notes this in its output. All other functionality works without c3.

## Architecture

This package is a **Yoker plugin**: it declares an `__YOKER_MANIFEST__`
that points Yoker to its `agents/` and `skills/` directories. Yoker's plugin
loader discovers the agent and skill definitions automatically, namespacing
them under `yoker_writing_assistant:`. The entry point is a thin Python
wrapper (`cli.py`) that injects `--with yoker-writing-assistant` and
`--agent yoker_writing_assistant:writing-assistant` into Yoker's CLI, so
`uvx yoker-writing-assistant` launches the writing assistant directly.

The sister project
[`yoker-assistant`](https://github.com/christophevg/yoker-assistant)
demonstrates the complementary mode — **yoker-as-SDK** — where Python owns
the process and calls Yoker as a library.

Both projects share a common quality bar documented in
[STANDARDS.md](STANDARDS.md).

## Documentation

Full documentation will live in `docs/` (pending).

## License

[MIT](LICENSE)


[pypi]: https://pypi.org/project/yoker/
[uv]: https://docs.astral.sh/uv/
[agentic]: https://christophe.vg/about/Agentic-Workflow
[yoker]: https://yoker.dev
[ci]: https://github.com/christophevg/yoker/actions
[coveralls]: https://coveralls.io/github/christophevg/yoker
[license]: https://github.com/christophevg/yoker/blob/main/LICENSE
