# Tutorial — How yoker-writing-assistant Was Built

This page tells the build story of `yoker-writing-assistant` end-to-end. A
reader who finishes it understands why the package exists, what the
non-negotiable rule is and why, how the thin-orchestrator architecture works,
what each of the eight skills does, how the plugin manifest and CLI wrapper
make it installable, and what the optional researcher integration adds. It
is a narrative — not a reference, not a list of links.

The package is small on purpose. It is one of two Yoker 1.0 pet-store
showcase packages; its job is to demonstrate **yoker-as-runtime** — Yoker is
the entry point and the package runs under it as a plugin. Every decision
below is in service of that demonstration.

---

## 1. Why this exists

An LLM that rewrites your prose is convenient, but it erodes the one thing
that matters: the author's voice and ownership of the work. Most "AI
writing assistant" tools are built to generate text for you. This one is
built to refuse.

The idea is simple and absolute: **the agent never writes prose.** It
interviews, challenges, reviews, and flags — but every word of prose is
written by the author. Every gap is marked `TODO:`. Every proposal is
marked `TODO PROPOSAL:`. The author accepts, rejects, or writes. The
friction is the value, not a bug.

This principle exists for three reasons:

- **Suggestion-acceptance bias.** When an LLM proposes prose, humans tend
  to accept it as-is. The `TODO PROPOSAL:` marker forces an explicit
  accept/reject decision — the proposal never reads as the draft.
- **Cognitive deskilling.** If the agent writes for you, you stop learning.
  The verbalization required to fill a `TODO:` yourself is where the
  learning happens.
- **Voice integrity.** The voice profile (`~/VOICE.md`) is a measurement
  instrument, not a generation model. The agent uses it to *detect drift*,
  never to *generate in the author's voice*.

## 2. The non-negotiable rule

The rule is simple and absolute: **the agent never writes prose.** Not
sentences, not paragraphs, not "just a starting point." Every gap is marked
`TODO:`. Every proposal is marked `TODO PROPOSAL:`. The author accepts,
rejects, or writes. The friction is the value, not a bug.

```
┌─────────────────────────────────────────────────────────────────┐
│  WRITING-ASSISTANT AGENT                                        │
│                                                                 │
│  ✗ NEVER writes prose                                           │
│  ✗ NEVER rewrites the author's prose                           │
│  ✗ NEVER fills a blank with authored text                       │
│  ✗ NEVER uses the voice profile to generate "in the author's   │
│     voice" — the profile is a measurement instrument only       │
│  ✗ NEVER inserts a TODO PROPOSAL: as if it were the draft       │
│                                                                 │
│  ✓ Interviews, challenges, structures, researches               │
│  ✓ Marks gaps with TODO: (the author writes)                   │
│  ✓ Marks proposals with TODO PROPOSAL: (author accepts/rejects) │
│  ✓ Delegates detail to writing-* skills and c3:researcher       │
│  ✓ All actual writing is ONLY done by the author                │
└─────────────────────────────────────────────────────────────────┘
```

This rule overrides every other instruction in the agent definition and
governs every skill the agent delegates to. It exists for a reason:

- **Suggestion-acceptance bias.** When an LLM proposes prose, humans tend
  to accept it as-is. The `TODO PROPOSAL:` marker forces an explicit
  accept/reject decision — the proposal never reads as the draft.
- **Cognitive deskilling.** If the agent writes for you, you stop learning.
  The verbalization required to fill a `TODO:` yourself is where the
  learning happens.
- **Voice integrity.** The voice profile (`~/VOICE.md`) is a measurement
  instrument, not a generation model. The agent uses it to *detect drift*,
  never to *generate in the author's voice*.

There are two sanctioned exceptions, both involving canonical forms — a
factual correction, not authoring prose:

- `writing-idioms` names the canonical form of a misused idiom or proverb.
- `writing-mistakes` names the canonical-correct form of eggcorns,
  redundancies, and non-native errors.

In each case the correction is a `TODO:` or `TODO PROPOSAL:` note for the
author to accept or reject. The skill never rewrites the author's sentence.

## 3. The thin orchestrator

The agent is deliberately a thin layer. It holds one invariant (the
non-negotiable rule) and routes work to skills. The detailed methodologies —
claim extraction, voice-drift detection, idiom catalogs, mistake taxonomies,
split heuristics, reorder algorithms — all live in the skills, each
independently invocable and independently testable.

```
                    ┌─────────────────────┐
                    │  writing-assistant  │
                    │  (thin orchestrator) │
                    │                     │
                    │  Holds the invariant│
                    │  Routes to skills   │
                    └──────────┬──────────┘
                               │ yoker:skill
           ┌───────────────────┼───────────────────┐
           ▼                   ▼                   ▼
  ┌─────────────────┐ ┌─────────────────┐ ┌─────────────────┐
  │ writing-review  │ │ writing-voice   │ │ writing-mistakes│
  │                 │ │                 │ │                 │
  │ claim extractn  │ │ drift detection │ │ eggcorns        │
  │ gap analysis    │ │ ChatGPT smell   │ │ redundancies    │
  │ advisory report │ │ voice profile   │ │ non-native errs │
  └─────────────────┘ └─────────────────┘ └─────────────────┘
           ▼                   ▼                   ▼
  ┌─────────────────┐ ┌─────────────────┐ ┌─────────────────┐
  │ writing-cont    │ │ writing-idioms  │ │ writing-split   │
  │ inuity          │ │                 │ │                 │
  │ dangling refs   │ │ canonical forms │ │ long-form →     │
  │ cold terms      │ │ as proposals    │ │ social posts    │
  └─────────────────┘ └─────────────────┘ └─────────────────┘
           ▼                   ▼                   ▼
  ┌─────────────────┐ ┌─────────────────┐
  │ writing-order   │ │ copy-writer     │
  │                 │ │                 │
  │ section reorder │ │ platform adapt  │
  │ argument flow   │ │ Twitter/LinkedIn│
  └─────────────────┘ └─────────────────┘
                               │ yoker:agent
                               ▼
                    ┌─────────────────────┐
                    │  c3:researcher      │
                    │  (optional, external)│
                    │                     │
                    │  web research with  │
                    │  provenance tracking│
                    └─────────────────────┘
```

If a skill grows heavy, it can be split further without touching the agent.
If a new concern emerges (say, "check my SEO structure"), a new skill is
added and the agent routes to it — no changes to the agent's core logic.
The shared invariant lives in the agent and governs every skill when
invoked through it. Each skill also carries its own local guardrail
(flag-only, no-prose) so it can be invoked standalone without the agent.

## 4. The eight skills

Each skill is a Markdown file with YAML frontmatter, packaged inside the
Python package at `src/yoker_writing_assistant/skills/`. Yoker's skill
loader discovers them via the plugin manifest and namespaces them under
`yoker_writing_assistant:`.

### writing-review

The analytical engine. Extracts and classifies claims (factual, opinion,
assumption, definition), verifies factual claims against authoritative
sources, analyzes coverage gaps and missing perspectives, handles the
author's opinions, and produces a structured advisory report. Every
recommendation becomes a `TODO:` or `TODO PROPOSAL:` — never prose.

### writing-continuity

Catches the structural leaks: dangling references (something mentioned
but never introduced), cold terms (jargon used without context), dropped
themes (a thread raised in part 1 and never resolved), and missing
transitions between sections or parts. Cross-part continuity is its
specific strength — it reads across multiple files and tracks whether
themes and references resolve.

### writing-voice

Voice drift detection and ChatGPT smell flagging. The author's voice
profile lives at `~/VOICE.md` — a rules-based document with quantitative
metrics, function-word frequencies, and explicit anti-patterns. The skill
reads the profile and checks the draft against it. Crucially, the profile
is a **measurement instrument only** — the skill never generates text "in
the author's voice." It also flags AI-tell vocabulary ("delve", "tapestry",
"realm", "underscore") from its bundled `references/ai-tells.md` catalog.

A nuance: new words or concepts that the author introduces that weren't in
the source material are **intellectual evolution**, not voice drift. The
skill only flags as drift when language is in the wrong register (corporate,
hype, AI-tell) — not when it's new thinking in the author's own voice.

### writing-mistakes

Common writing mistakes with a taxonomy that splits into two categories:

- **CANONICAL** — a correct form exists (eggcorns, redundancies,
  non-native errors). The skill names the recognized form in a `TODO:` note
  for the author to accept or reject. It never rewrites the sentence.
- **CRAFT** — judgment calls, not correctable forms (passive voice
  overuse, nominalization, vague pronouns). The skill flags and explains;
  the author fixes.

The bundled `references/mistakes-taxonomy.md` provides the full reference
catalog, synthesized from Strunk, Orwell, Williams, Pinker, Zinsser, and
non-native-English references.

### writing-idioms

Idiom and proverb misuse detection. When the author writes "for all
intensive purposes" instead of "for all intents and purposes," the skill
names the canonical form as a `TODO PROPOSAL:`. When an idiom is used
correctly but a better proverb exists for the context, the skill proposes
the alternative. Ambiguous cases (misuse vs. deliberate creative choice)
are asked, not asserted.

### writing-split

Long-form to sequential social post splitting. The author has a long
article and wants to break it into a thread or sequence. The skill proposes
a post sequence as `TODO PROPOSAL:` — the posts are the author's prose,
the skill only structures the split. It handles platform-specific
constraints (character limits, thread patterns, hook zones).

### writing-order

Section reordering for argument flow. When the author has a draft with
sections in the wrong order, the skill maps section roles, interviews for
the argument arc, proposes a reordering, iterates on feedback, and applies
section moves only — no content changes. The skill works with written
sections and `TODO:` stubs alike, treating both as raw material to arrange.

### copy-writer

Platform-specific content adaptation. The author has existing content and
wants to adapt it for Twitter/X, LinkedIn, Mastodon, Newsletter, or Blog.
The skill preserves the author's voice while applying platform-specific
conventions: character limits, hook zones, hashtag norms, content mix
ratios, tone adjustments. The original content must already exist — the
skill transforms, it does not create. Supports English and Dutch.

## 5. The plugin architecture

This package is a **Yoker plugin**. The `__YOKER_MANIFEST__` in
`src/yoker_writing_assistant/__init__.py` tells Yoker where to find the
agent and skill definitions:

```python
from yoker.plugins import PluginManifest

__version__ = "0.1.3"

__YOKER_MANIFEST__ = PluginManifest(
  agents_dir="agents",
  skills_dir="skills",
  agent="yoker_writing_assistant:writing-assistant",
)
```

The `agents/` and `skills/` directories live *inside the Python package*
(`src/yoker_writing_assistant/`) because Yoker's plugin loader discovers
them via `importlib.resources`. This means the definitions are part of the
built wheel — `pip install yoker-writing-assistant` gives you the agent and
all eight skills with no extra steps.

Yoker's plugin loader namespaces everything under the package name:
`yoker_writing_assistant:writing-assistant` for the agent,
`yoker_writing_assistant:writing-review` for skills, and so on. Yoker also
supports bare-name resolution (a bare `writing-review` resolves to any
registered skill with that simple name), but in agent and skill definitions
the fully qualified names are preferred for clarity.

## 6. The CLI wrapper

A thin Python wrapper makes the package runnable as a standalone command.
The `[project.scripts]` entry in `pyproject.toml` points to
`yoker_writing_assistant.cli:main`, which injects `--with` and `--agent-name`
into Yoker's CLI and delegates to Yoker's `main()`:

```python
def main() -> None:
  if not config_provided():
    _run_bootstrap_wizard()

  sys.argv = (
    [
      "yoker",
      "--with", "yoker_writing_assistant",
      "--agent-name", "yoker_writing_assistant:writing-assistant",
      "--harness-name", "yoker-writing-assistant",
      # ... harness metadata ...
      "--plugins-enabled",
    ]
    + sys.argv[1:]
  )
  yoker_main()
```

This is why `uvx yoker-writing-assistant` launches the writing assistant
directly — the wrapper does the plumbing, Yoker does the reasoning. Any
additional CLI flags the user passes (e.g., `--ui-mode batch`,
`--resume mysession`) are appended after the injected args.

The wrapper also handles first-run bootstrap: if no Yoker configuration is
found at `~/.yoker.toml` or `./yoker.toml`, an interactive bootstrap wizard
runs before the CLI args are injected. This prevents the injected flags
from masking the no-config case. After the wizard writes
`~/.yoker.toml`, the user must manually set `enabled = true` and re-run.

## 7. The optional researcher integration

The writing assistant can delegate research tasks to `c3:researcher`, an
external research agent. This is an optional dependency — the agent works
fully without it, using `yoker:websearch` and `yoker:webfetch` directly
for research when the researcher is unavailable.

When configured, the agent delegates all research via `yoker:agent` with
agent name `c3:researcher`. The researcher provides web search, content
fetching, and provenance tracking — sources are cited, contradictions are
surfaced, and the agent returns findings without drawing conclusions for
the author.

When the researcher is not configured, the agent falls back to direct web
search and notes the limitation in "What this did NOT check." All other
functionality — review, continuity, voice, mistakes, idioms, split,
reorder, copy-writer — works without it. See
[Configuration](configuration.md) for setup details.

## 8. The modes of operation

The assistant discovers which mode is needed from the author's request, or
asks. A session may move through several modes.

### Interview mode (before/during writing)

The default mode. Exploits the **generator-discriminator gap**: it is
easier for the author to react to a question than to generate from scratch.
The assistant asks one question at a time, pushes for concrete examples,
points out contradictions, and walks the author down a depth chain
(fact → pattern → principle → counter-example → triangulate). An interview
log persists the author's words as raw material.

### Developmental editing mode (after bits/drafts exist)

Review big-picture structure and argument flow. Two passes, never
interleaved:

1. **Structural pass first** — section hierarchy, argument arc, gaps,
   balance, transitions, continuity. Delegates to `writing-continuity` and
   `writing-review`.
2. **Voice pass second** — only after structure is settled. Delegates to
   `writing-voice`.

### Structure-tracking mode

Supports the author's organic workflow: bits → conglomerate → structure →
gaps → prune. Three-tier status tracking (`bit` → `section` → `complete`),
inline `TODO:`/`TODO PROPOSAL:` markers as the source of truth, and
on-demand structure overviews.

### Research mode

Delegates research to `c3:researcher` (or falls back to direct web search).
Uses `writing-review` to frame claim extraction and interpret findings.
The assistant surfaces findings and contradictions — it never draws
conclusions for the author.

### Split, reorder, and copy adaptation modes

Three more modes delegate to their matching skills: `writing-split` for
long-form to social posts, `writing-order` for section reordering, and
`copy-writer` for platform-specific adaptation. Each produces
`TODO PROPOSAL:` output — the author's prose, structured by the skill.

## 9. What's out of scope

The assistant is deliberately not a line editor, not a copy editor, and not
a prose generator. These are explicitly out of scope:

- **Line-editing and copy-editing** — sentence-level prose correction is
  the author's job. The assistant flags at the developmental level
  (structure, argument, gaps, voice drift) and, as sanctioned exceptions,
  names canonical-correct forms of idioms and common mistakes. It never
  rewrites the author's sentence.
- **Drawing conclusions** — the assistant surfaces findings,
  contradictions, and tradeoffs. The author decides what they mean.
- **Batching questions** — the assistant asks one question at a time and
  waits. No numbered lists of questions.
- **Unearned praise** — "Great point!" and "Excellent!" are forbidden
  unless earned and specific. Vague affirmation is noise.
- **Prose generation in any form** — not sentences, not paragraphs, not
  "just a starting point." The author's blank stays blank until the author
  fills it.

The friction is the value. Convenience would erode the author's craft.
This is the point, not a bug.

---

This is the end of the narrative. The supporting pages hold the long-form
reference: [Architecture](architecture.md) for the delegation model and
plugin mechanics, [Skills](skills.md) for the per-skill detail,
[Configuration](configuration.md) for the `~/.yoker.toml` reference, and
[API](api.md) for the public API surface.