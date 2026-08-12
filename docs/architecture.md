# Architecture

This page is the reference for the writing assistant's architecture: the
delegation model, the plugin mechanics, and the namespace system. It is the
long-form companion to the [Tutorial](tutorial.md) (which tells the story)
and the [Skills](skills.md) page (which covers each skill in detail).

## The delegation model

The agent is a thin orchestrator. It holds one invariant — the author writes
all prose — and routes work to skills. The detailed methodologies live in
the skills, each independently invocable.

### Agent → skill delegation

When the author asks for a review, a voice check, or a continuity scan,
the agent invokes the matching skill via `yoker:skill` with the skill's
fully qualified name:

| Skill | Invoked for | Invoke pattern |
|-------|-------------|----------------|
| `writing-review` | Developmental review, claim verification, advisory reports | `yoker:skill` with `yoker_writing_assistant:writing-review` |
| `writing-continuity` | Dangling refs, cold terms, dropped themes, transitions | `yoker:skill` with `yoker_writing_assistant:writing-continuity` |
| `writing-voice` | Voice drift, ChatGPT smell, voice profile checks | `yoker:skill` with `yoker_writing_assistant:writing-voice` |
| `writing-mistakes` | Eggcorns, redundancies, non-native errors, craft patterns | `yoker:skill` with `yoker_writing_assistant:writing-mistakes` |
| `writing-idioms` | Idiom/proverb misuse → canonical form proposals | `yoker:skill` with `yoker_writing_assistant:writing-idioms` |
| `writing-split` | Long-form → sequential social post sequence | `yoker:skill` with `yoker_writing_assistant:writing-split` |
| `writing-order` | Section reordering for argument flow | `yoker:skill` with `yoker_writing_assistant:writing-order` |
| `copy-writer` | Platform-specific content adaptation | `yoker:skill` with `yoker_writing_assistant:copy-writer` |

Each skill carries its own local guardrail (flag-only, no-prose) and may be
invoked standalone without the agent. The non-negotiable rule governs all
skills when invoked through the agent.

### Agent → sub-agent delegation

Research is delegated to `c3:researcher` via `yoker:agent`:

```
yoker:agent with agent_name "c3:researcher"
```

The `c3:researcher` agent is an optional external dependency. It is only
available when the researcher agent is configured in `~/.yoker.toml` under
`[agents.directories]`. If not configured, the agent falls back to
direct web search (`yoker:websearch` / `yoker:webfetch`) and notes the
limitation in "What this did NOT check."

### Skill bundled resources

Some skills ship bundled reference files in a `references/` subfolder:

| Skill | Resource | Loaded via |
|-------|----------|------------|
| `writing-mistakes` | `references/mistakes-taxonomy.md` | `yoker:skill` with `skill resource=` syntax |
| `writing-voice` | `references/ai-tells.md` | `yoker:skill` with `skill resource=` syntax |

These are deep-sweep catalogs — the taxonomy of common mistakes, the
vocabulary of AI-tells — that the skill reads when doing a full analysis.

## The plugin mechanics

### Plugin manifest

The package declares a `__YOKER_MANIFEST__` in
`src/yoker_writing_assistant/__init__.py`:

```python
__YOKER_MANIFEST__ = PluginManifest(
  agents_dir="agents",
  skills_dir="skills",
  agent="yoker_writing_assistant:writing-assistant",
)
```

This tells Yoker's plugin loader where to find the agent and skill
definitions. The `agents/` and `skills/` directories live inside the Python
package because the plugin loader discovers them via `importlib.resources`.
This means the definitions are part of the built wheel — no extra files to
install, no paths to configure.

### Import safety

The `__init__.py` is import-safe: importing it must NOT trigger any Agent
construction or session logic. The manifest only declares directories — no
side effects at import time. This discipline avoids circular imports and
ensures the package can be loaded as a plugin without starting a session.

### Namespace system

When loaded as a Yoker plugin, the plugin loader uses the package name as
the namespace for all discovered agents and skills:

- Agents: `yoker_writing_assistant:writing-assistant`
- Skills: `yoker_writing_assistant:writing-review`, etc.
- External agents: `c3:researcher` (optional, loaded from an external
  agent directory configured in `~/.yoker.toml`)

Yoker supports bare-name resolution (a bare `writing-review` resolves to
any registered skill with that simple name), but fully qualified names are
preferred in agent and skill definitions for clarity and correctness.

### CLI wrapper

The entry point at `src/yoker_writing_assistant/cli.py` injects `--with`
and `--agent` into Yoker's CLI and delegates to Yoker's `main()`. This
allows running the writing assistant via `uvx yoker-writing-assistant` or
`yoker-writing-assistant` directly. The wrapper also handles first-run
bootstrap: if no configuration is found, an interactive wizard runs before
the CLI args are injected.

## The tool set

The agent's tools are declared in the `tools:` frontmatter of
`src/yoker_writing_assistant/agents/writing-assistant.md`. The set is
curated — named, guardrailed tools, no open shell:

| Tool | Use for |
|------|---------|
| `yoker:read` | Reading drafts, `~/VOICE.md`, prior published work |
| `yoker:list` | Finding draft files, TODO markers, post directories |
| `yoker:search` | Scanning for `TODO:`/`TODO PROPOSAL:` markers across files |
| `yoker:write` | Creating interview logs or artifacts the author asked for |
| `yoker:update` | Inserting `TODO:`/`TODO PROPOSAL:` markers into drafts |
| `yoker:file` | Copying, moving, or deleting draft files |
| `yoker:mkdir` | Creating directories for organizing drafts |
| `yoker:existence` | Checking if a file (e.g., `~/VOICE.md`) exists |
| `yoker:skill` | Delegating to `writing-*` skills, loading skill resources |
| `yoker:agent` | Delegating research to `c3:researcher` |
| `yoker:websearch` | Fallback research when c3:researcher unavailable |
| `yoker:webfetch` | Fetching URLs for fact-checking (fallback) |
| `yoker:git` | Committing and pushing changes when the author requests |
| `yoker:github` | Viewing PRs, issues, or workflow status |
| `yoker:make` | Running Makefile targets if the project has them |

The safety model: agents get a curated set of safe, named tools, never an
open shell. Each tool has guardrails (path restrictions, URL validation,
complexity limits). The agent cannot escape them because the tool itself
enforces them, not a prompt.

## Error handling

The agent handles several error cases gracefully:

- **Profile missing or unreadable:** The voice profile at `~/VOICE.md` is
  read directly with `yoker:read`. If the file is absent, the voice pass
  is skipped entirely. The agent tells the author no voice checks ran and
  why. Never assumes a profile or substitutes another.
- **Profile is a snapshot:** The voice profile may not include the author's
  most recent work. Flagged terms are cross-referenced against the source
  material before reporting drift. Article-native terms are not reported as
  drift.
- **Skill not available:** Falls back to applying the concern directly from
  the agent's own knowledge, notes the limitation, and recommends
  installing the skill for the full reference.
- **c3:researcher not available:** Falls back to direct web search, notes
  the limitation in "What this did NOT check."
- **Contradictory sources:** Surfaces the conflict with both sources cited;
  does not pick a winner. Resolution is marked as `TODO:`.
- **Ambiguous idiom:** Asks the author rather than asserting. Defaults to
  question, not correction.