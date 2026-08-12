# PACKAGE.md

> AI-optimized package documentation for `yoker-writing-assistant`.

## What This Package Provides

A Yoker plugin that provides a writing assistant agent and eight skills for
developmental editing, voice checking, continuity, mistake flagging, idiom
correction, splitting, reordering, and platform-specific copy adaptation.

The core design principle: **the agent never writes prose.** Every gap
becomes `TODO:`, every proposal becomes `TODO PROPOSAL:`. The author
accepts, rejects, or writes. The friction is the value, not a bug.

## Installation

```bash
pip install yoker-writing-assistant
# or
uv add yoker-writing-assistant
```

Requires `yoker>=0.10.1` and Python 3.10+.

## Plugin Manifest

```python
from yoker_writing_assistant import __YOKER_MANIFEST__

# PluginManifest(
#   agents_dir="agents",
#   skills_dir="skills",
#   agent="yoker_writing_assistant:writing-assistant",
# )
```

## Loading as a Yoker Plugin

### Via `~/.yoker.toml`

```toml
[plugins]
enabled = true
packages = ["yoker_writing_assistant"]

[plugins.trusted]
yoker_writing_assistant = true
```

### Via CLI

```bash
yoker --with yoker_writing_assistant --agent yoker_writing_assistant:writing-assistant
```

## Provided Agents

| Agent | Namespace | Description |
|-------|-----------|-------------|
| `writing-assistant` | `yoker_writing_assistant:writing-assistant` | Thin orchestrator: interviews, challenges, reviews, flags — never writes prose |

## Provided Skills

| Skill | Namespace | Description |
|-------|-----------|-------------|
| `writing-review` | `yoker_writing_assistant:writing-review` | Developmental review, claim verification, advisory reports |
| `writing-continuity` | `yoker_writing_assistant:writing-continuity` | Dangling refs, cold terms, dropped themes, transitions |
| `writing-voice` | `yoker_writing_assistant:writing-voice` | Voice drift, ChatGPT smell, voice profile checks |
| `writing-mistakes` | `yoker_writing_assistant:writing-mistakes` | Eggcorns, redundancies, non-native errors, craft patterns |
| `writing-idioms` | `yoker_writing_assistant:writing-idioms` | Idiom/proverb misuse → canonical form proposals |
| `writing-split` | `yoker_writing_assistant:writing-split` | Long-form → sequential social post sequence |
| `writing-order` | `yoker_writing_assistant:writing-order` | Section reordering for argument flow |
| `copy-writer` | `yoker_writing_assistant:copy-writer` | Platform-specific content adaptation (Twitter, LinkedIn, Mastodon, Newsletter, Blog) |

## CLI Entry Point

```bash
yoker-writing-assistant                    # launch the writing assistant
yoker-writing-assistant --ui-mode batch    # batch mode
```

Registered as `[project.scripts]` in `pyproject.toml`, pointing to
`yoker_writing_assistant.cli:main`. The wrapper injects `--with` and
`--agent` flags into Yoker's CLI and delegates to Yoker's `main()`.

## Optional Dependency: c3:researcher

Research delegation to `c3:researcher` requires an external agent
directory to be configured in `~/.yoker.toml`:

```toml
[agents.directories]
c3 = "../c3/agents"
```

Without the researcher, the agent falls back to direct web search and
notes the limitation in its output.

## Public API Surface

| Symbol | Description |
|--------|-------------|
| `yoker_writing_assistant.__YOKER_MANIFEST__` | Plugin manifest (agents/skills dirs, default agent) |
| `yoker_writing_assistant.__version__` | Package version string |
| `yoker_writing_assistant.cli.main()` | CLI entry point (injects flags, delegates to Yoker) |

The package is import-safe: importing it does not trigger Agent
construction or session logic.

## Modes of Operation

| Mode | Description |
|------|-------------|
| Interview | Ask one question at a time, push for concrete examples, depth chain |
| Developmental editing | Structural pass then voice pass, delegates to skills |
| Structure tracking | Three-tier status (bit → section → complete), TODO inventory |
| Research | Delegate to c3:researcher (or fallback to web search) |
| Split | Long-form → social post sequence |
| Reorder | Section reordering for argument flow |
| Copy adaptation | Platform-specific content transformation |

## Further Documentation

Full documentation lives in `docs/` and is published to ReadTheDocs.

- [Tutorial](docs/tutorial.md) — how this package was built
- [Architecture](docs/architecture.md) — delegation model and plugin mechanics
- [Skills](docs/skills.md) — per-skill reference
- [Configuration](docs/configuration.md) — `~/.yoker.toml` reference

## License

MIT — see [LICENSE](LICENSE).