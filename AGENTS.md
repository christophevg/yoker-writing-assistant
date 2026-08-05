# Writing Assistant Agent Guide

Essential context for working on the yoker-writing-assistant codebase. For
user-facing documentation, see [README.md](README.md). For shared quality
standards across both showcase packages, see [STANDARDS.md](STANDARDS.md).

## IMPORTANT CURRENT DEVELOPMENT PHASE

We are in a dogfooding phase, fixing problems in Yoker with Yoker. Code
changes to Yoker itself (at `../yoker`) require a stop/resume to become
active. If a tool is missing or fails, STOP and raise it — do not look for
workarounds.

C3 (`../c3`) provides heritage agent and skill definitions. Some are not
fully ported to Yoker yet. If you use them and hit unknown references, bash
commands, or unknown tools, raise the issue so it can be fixed in C3 too.
After a stop/resume, improvements are immediately available.

## Positioning

This is a **Yoker plugin** demonstrating the **yoker-as-runtime** mode: Yoker
is the entry point, and this package runs under it. It provides a writing
assistant agent with skills for developmental editing, voice checking,
continuity, mistake flagging, idiom correction, splitting, reordering, and
platform-specific copy adaptation.

The sister project `../yoker-assistant` demonstrates **yoker-as-SDK**: Python
owns the process and calls Yoker as a library. Both are showcase packages
for the Yoker 1.0 public release.

The shared quality bar for both projects is in
[STANDARDS.md](STANDARDS.md): ultra clean code, tight right-tool-for-the-right-job
separation, limited but useful tests, c3-to-Yoker adaptation, and showcase
quality. Both projects inherit it; each carries its own copy kept in sync.

## The Two Core Principles

1. **The author writes all prose.** The agent never writes, rewrites, or
   fills blanks. Every gap becomes `TODO:`, every proposal becomes
   `TODO PROPOSAL:`. This is the non-negotiable rule.

2. **Thin orchestrator.** The agent delegates to skills. The detailed
   methodologies live in the `writing-*` skills, each independently
   invocable. The agent holds the invariant and routes work.

## Conventions

- **Indentation**: Two spaces in all file types.
- **Package manager**: `uv` (see Makefile for standard targets).
- **Commit attribution**: `🤖 Implemented together with Yoker` as the trailer
  line on agent-made commits.
- **Fully qualified names**: In agent and skill definitions, use fully
  qualified names for tools (`yoker:read`), skills
  (`yoker_writing_assistant:writing-review`), and agents (`c3:researcher`).
  Yoker supports bare-name resolution, but fully qualified is preferred in
  definitions for clarity and correctness.

## Current Project State

The project is in early setup. The following exist from a previous Claude
Code (c3) implementation:

- `agents/writing-assistant.md` — the main agent definition (needs Yoker adaptation)
- `skills/` — 8 skill definitions (need Yoker adaptation)
- `STANDARDS.md` — shared quality bar with yoker-assistant
- `yoker.toml` — Yoker runtime config (references c3 dirs)
- `Makefile` — minimal, includes `~/.yoker/Makefile`

The following are **missing** and need to be created:

- `pyproject.toml` — Python package definition
- `src/yoker_writing_assistant/` — Python package with `__YOKER_MANIFEST__`
- Proper Makefile with standard targets (env-dev, test, check, etc.)
- `uv.lock`
- Tests
- Documentation (`docs/`)

## Namespace and Plugin Architecture

This package is named `yoker-writing-assistant` (distribution name) /
`yoker_writing_assistant` (Python import name). When loaded as a Yoker
plugin, the plugin loader uses the package name as the namespace for all
discovered agents and skills.

- Agents from this package are namespaced `yoker_writing_assistant:`
  (e.g., `yoker_writing_assistant:writing-assistant`)
- Skills from this package are namespaced `yoker_writing_assistant:`
  (e.g., `yoker_writing_assistant:writing-review`)
- C3 agents and skills are namespaced `c3:` (e.g., `c3:researcher`,
  `c3:writing-review`) — loaded from `../c3/agents` and `../c3/skills` via
  the `agents.directories` and `skills.directories` config in `yoker.toml`

Yoker supports bare-name resolution (a bare `writing-review` resolves to
any registered skill with that simple name), but in agent and skill
definitions, always use fully qualified names.

## Agent Definition Format (Yoker)

Agent definitions are Markdown files with YAML frontmatter:

```yaml
---
name: writing-assistant
description: |
  Short description for LLM tool definition.
tools:
  - yoker:read
  - yoker:list
  - yoker:search
  - yoker:write
  - yoker:update
  - yoker:file
  - yoker:existence
  - yoker:mkdir
  - yoker:skill
  - yoker:agent
  - yoker:websearch
  - yoker:webfetch
  - yoker:git
  - yoker:github
  - yoker:make
color: orange
model: optional-model-override
agents:  # allowlist of agents this one can spawn
  - c3:researcher
---
# System prompt body
```

Key fields:
- `tools`: Yoker-namespaced tool names. `ALL_TOOLS` (default) = all enabled
  tools. `[]` = no tools. Explicit list = filter to those.
- `agents`: Allowlist of agent names this agent can spawn. Default =
  ALL_AGENTS. Empty tuple = no spawns.
- `color`: UI display color.
- `model`: Optional model override.

## Skill Definition Format (Yoker)

Skill definitions are Markdown files with YAML frontmatter:

```yaml
---
name: writing-review
description: |
  Short description for the discovery block.
triggers: []  # optional natural-language triggers
tools: []  # optional tool names this skill uses
---
# Skill content (becomes the system prompt addition when invoked)
```

Skills live in directories (one per skill), can have a `references/`
subfolder for resource files, and are loaded by the skill loader.

## Tool Name Mapping (c3 → Yoker)

The existing definitions use Claude Code tool names. Here is the mapping:

| c3 / Claude Code | Yoker | Notes |
|------------------|-------|-------|
| `Read` | `yoker:read` | File contents with offset/limit |
| `Glob` | `yoker:list` | Directory listing with pattern |
| `Grep` | `yoker:search` | Content search (regex) + filename search |
| `Write` | `yoker:write` | Write file contents |
| `Edit` | `yoker:update` | Edit existing file (replace/insert/delete) |
| `Skill` | `yoker:skill` | Invoke a skill |
| `Agent` | `yoker:agent` | Spawn a sub-agent |
| `AskUserQuestion` | *(none)* | Just ask in the response text |
| `PushNotification` | *(none)* | No equivalent; omit |
| *(none)* | `yoker:file` | Filesystem operations: copy, move, delete |
| *(none)* | `yoker:existence` | Check file/folder existence |
| *(none)* | `yoker:mkdir` | Create directories |
| *(none)* | `yoker:send_message` | Send message to another active agent |
| *(none)* | `yoker:websearch` | Web search |
| *(none)* | `yoker:webfetch` | Web fetch |
| *(none)* | `yoker:git` | Git operations |
| *(none)* | `yoker:github` | GitHub operations |
| *(none)* | `yoker:make` | Makefile target execution |

## Agent Tool Set

The writing assistant gets the full set of Yoker tools:

- **File access**: `yoker:read`, `yoker:list`, `yoker:search`, `yoker:write`,
  `yoker:update`, `yoker:file`, `yoker:existence`, `yoker:mkdir`
- **Skills & agents**: `yoker:skill`, `yoker:agent`
- **Web**: `yoker:websearch`, `yoker:webfetch`
- **Git & GitHub**: `yoker:git`, `yoker:github`
- **Build**: `yoker:make`

The agent delegates research to `c3:researcher` but may also use web tools
directly when appropriate. The `c3:researcher` dependency is external — it
is only available when c3 is configured (via `agents.directories.c3` in
`yoker.toml`). If c3 is not configured, research delegation is not possible
and the agent should note this in "What this did NOT check."

## Skill Namespace Mapping (c3 → this project)

The existing agent references skills as `c3:writing-review` etc. Since the
skills now live in this project's `skills/` directory and will be loaded as
part of the `yoker_writing_assistant` plugin, they should be referenced with
the `yoker_writing_assistant:` namespace.

| c3 reference | This project | File |
|--------------|-------------|------|
| `c3:writing-review` | `yoker_writing_assistant:writing-review` | `skills/writing-review/SKILL.md` |
| `c3:writing-continuity` | `yoker_writing_assistant:writing-continuity` | `skills/writing-continuity/SKILL.md` |
| `c3:writing-voice` | `yoker_writing_assistant:writing-voice` | `skills/writing-voice/SKILL.md` |
| `c3:writing-mistakes` | `yoker_writing_assistant:writing-mistakes` | `skills/writing-mistakes/SKILL.md` |
| `c3:writing-idioms` | `yoker_writing_assistant:writing-idioms` | `skills/writing-idioms/SKILL.md` |
| `c3:writing-split` | `yoker_writing_assistant:writing-split` | `skills/writing-split/SKILL.md` |
| `c3:writing-order` | `yoker_writing_assistant:writing-order` | `skills/writing-order/SKILL.md` |

The `copy-writer` skill (`skills/copy-writer/SKILL.md`) is part of this
project and will be integrated into the writing-assistant agent as an
additional skill for platform-specific content adaptation.

## Agent References

The agent delegates research to `c3:researcher`. This is an external
dependency — the researcher agent definition lives at
`../c3/agents/researcher.md` and is loaded via the `agents.directories`
config in `yoker.toml` under the `c3` namespace. If c3 is not configured,
`c3:researcher` is not available and the agent handles this gracefully (see
error handling in the agent definition).

## Launch / Entry Point

A thin Python wrapper is needed because `pyproject.toml` `[project.scripts]`
entries must point to a Python callable, not a shell command. The wrapper
injects `--with` and `--agent` into `sys.argv` and delegates to Yoker's
`main()`:

```toml
[project.scripts]
yoker-writing-assistant = "yoker_writing_assistant.cli:main"
```

```python
# src/yoker_writing_assistant/cli.py
import sys
from yoker.__main__ import main as yoker_main

def main():
  sys.argv = [
    "yoker",
    "--with", "yoker_writing_assistant",
    "--agent", "yoker_writing_assistant:writing-assistant",
  ] + sys.argv[1:]
  yoker_main()
```

This loads the plugin (`--with yoker_writing_assistant` — the Python package
name) and selects the writing assistant as the primary agent
(`--agent yoker_writing_assistant:writing-assistant`). Any additional CLI
flags the user passes (e.g., `--ui-mode batch`, `--resume mysession`) are
appended after the injected args.

Users can also run the Yoker CLI directly with the same flags:

```bash
yoker --with yoker_writing_assistant --agent yoker_writing_assistant:writing-assistant
```

## Plugin Manifest

The package's `__init__.py` declares a `__YOKER_MANIFEST__`:

```python
from yoker.plugins import PluginManifest

__version__ = "0.1.0"

__YOKER_MANIFEST__ = PluginManifest(
  agents_dir="agents",
  skills_dir="skills",
  agent="yoker_writing_assistant:writing-assistant",  # default agent
)
```

This declares the agents and skills directories. Yoker's plugin loader
discovers agent and skill definitions automatically, namespacing them
under `yoker_writing_assistant:` (the package name).

## Module Structure (Target)

```text
src/yoker_writing_assistant/
├── __init__.py              # __YOKER_MANIFEST__, version, import-safe
├── cli.py                   # Entry point: injects --with/--agent, delegates to yoker main
├── py.typed                 # PEP 561 marker
├── agents/
│   └── writing-assistant.md # Main agent definition (Yoker-adapted)
└── skills/
    ├── copy-writer/         # Platform-specific content adaptation
    │   ├── SKILL.md
    │   └── REFERENCE.md
    ├── writing-continuity/  # Continuity and cross-reference checking
    │   └── SKILL.md
    ├── writing-idioms/       # Idiom/proverb misuse flagging
    │   └── SKILL.md
    ├── writing-mistakes/     # Common writing mistake flagging
    │   ├── SKILL.md
    │   └── references/
    │       └── mistakes-taxonomy.md
    ├── writing-order/        # Section reordering
    │   └── SKILL.md
    ├── writing-review/       # Developmental editing review
    │   └── SKILL.md
    ├── writing-split/        # Long-form → social post splitting
    │   └── SKILL.md
    └── writing-voice/        # Voice drift and ChatGPT smell checking
        ├── SKILL.md
        └── references/
            └── ai-tells.md
```

The `agents/` and `skills/` directories live inside the Python package
(`src/yoker_writing_assistant/`) because the plugin loader discovers them
via `importlib.resources`. The `[tool.hatch.build.targets.wheel]` config
includes the entire `src/yoker_writing_assistant` package, so these
directories are part of the built wheel.

## Tool Output Discipline

**Always use `post_filter` on every tool call** to keep only relevant lines.
Tool outputs can be very large and consume context budget rapidly.

- `make test` / `make check`: `post_filter="FAILED|ERROR|error|Traceback|assert"`
- `read` / `search` on large files: filter for structure markers
  (`class |def |import `) or specific patterns (`TODO|FIXME|HACK`).
- `git log` / `git diff`: filter for the specific file, author, or pattern.
- `list` on large directories: use `pattern` or `post_filter`.

## Adaptation Checklist

When adapting the existing definitions from c3 to Yoker:

### Agent definition (`agents/writing-assistant.md`)

- [ ] Replace tool names: `Read`→`yoker:read`, `Glob`→`yoker:list`,
      `Grep`→`yoker:search`, `Write`→`yoker:write`, `Edit`→`yoker:update`,
      `Skill`→`yoker:skill`, `Agent`→`yoker:agent`
- [ ] Add tools not in c3: `yoker:file`, `yoker:existence`, `yoker:mkdir`,
      `yoker:websearch`, `yoker:webfetch`, `yoker:git`, `yoker:github`,
      `yoker:make`
- [ ] Remove tools with no Yoker equivalent: `AskUserQuestion`,
      `PushNotification`
- [ ] Replace skill references: `c3:writing-*`→`yoker_writing_assistant:writing-*`
- [ ] Add `copy-writer` skill reference
- [ ] Keep `c3:researcher` reference (external dependency, gracefully handled)
- [ ] Update the `agents` frontmatter to list `c3:researcher` explicitly
- [ ] Replace `AskUserQuestion` usage in the body with plain text questions
- [ ] Replace `Agent(subagent_type="c3:researcher", prompt="...")` with
      `yoker:agent` invocation patterns
- [ ] Remove `PushNotification` references
- [ ] Update the Tool Usage table to reflect the Yoker tool set

### Skill definitions (`skills/*/SKILL.md`)

- [ ] Replace skill cross-references: `c3:writing-*`→`yoker_writing_assistant:writing-*`
- [ ] Replace `c3:researcher` references where skills mention it
- [ ] Replace tool names in any tool references within skill bodies
- [ ] No frontmatter changes needed for `name`/`description` (those are
      namespace-agnostic)