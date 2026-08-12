# Skills Reference

This page covers each of the eight skills in detail: what it does, when to
use it, when not to use it, and how it enforces the non-negotiable rule
locally. For the delegation model and plugin mechanics, see
[Architecture](architecture.md). For the build story, see
[Tutorial](tutorial.md).

All skills are packaged inside the Python package at
`src/yoker_writing_assistant/skills/` and discovered by Yoker's plugin
loader. Each is independently invocable via `yoker:skill` with its fully
qualified name.

---

## writing-review

**Invocation:** `yoker:skill` with `yoker_writing_assistant:writing-review`

The analytical engine for developmental editing and research validation.
Every recommendation becomes a `TODO:` or `TODO PROPOSAL:` — never prose.

### What it does

- Extracts and classifies claims (factual, opinion, assumption, definition)
- Verifies factual claims against authoritative sources (minimum 2
  independent sources for cross-validation)
- Analyzes coverage gaps and missing perspectives
- Handles the author's opinions (surfaces them, does not resolve them)
- Produces a structured advisory report

### When to use

- The author requests a review or advisory report
- Verifying factual claims in a draft
- Analyzing coverage gaps and missing perspectives
- Framing research findings (paired with `c3:researcher`)

### When NOT to use

- Continuity / dangling references → `writing-continuity`
- Sentence-level mistakes → `writing-mistakes`
- Voice drift → `writing-voice`
- Idiom misuse → `writing-idioms`

### Local guardrail

Every recommendation becomes a `TODO:` or `TODO PROPOSAL:` marker — never
prose. The skill's claim extraction and verification standards produce
analytical output; no prose is generated.

---

## writing-continuity

**Invocation:** `yoker:skill` with `yoker_writing_assistant:writing-continuity`

Catches the structural leaks that a close reading would find but the author
missed during drafting.

### What it does

- Dangling references: something mentioned but never introduced
- Cold terms: jargon used without context or definition
- Dropped themes: a thread raised early and never resolved
- Missing transitions between sections or parts
- Cross-part continuity: reads across multiple files and tracks whether
  themes and references resolve

### When to use

- "check continuity" / "do cross-references resolve?"
- After structural reorganization (things may have drifted)
- When working across multiple parts or chapters

### When NOT to use

- Single-claim verification → `writing-review`
- Voice issues → `writing-voice`

### Local guardrail

Flags continuity issues as `TODO:` markers with location references
(section, paragraph). Never rewrites transitions. The author writes the
fix.

---

## writing-voice

**Invocation:** `yoker:skill` with `yoker_writing_assistant:writing-voice`

Voice drift detection and ChatGPT smell flagging. Uses the author's voice
profile at `~/VOICE.md` as a measurement instrument.

### What it does

- Reads the voice profile from `$HOME/VOICE.md` via `yoker:read`
- Checks the draft against the profile's quantitative metrics and
  anti-patterns
- Flags AI-tell vocabulary from the bundled `references/ai-tells.md`
  catalog
- Distinguishes voice drift from intellectual evolution: new words or
  concepts in the author's own voice are NOT drift — only wrong-register
  language (corporate, hype, AI-tell) is flagged

### When to use

- "check my voice" / "flag ChatGPT smell"
- After a drafting session where the author suspects AI influence
- Quarterly drift check (the skill supports periodic review)

### When NOT to use

- Structural issues → `writing-review` or `writing-continuity`
- Mistakes → `writing-mistakes`

### Local guardrail

The voice profile is a **measurement instrument only** — never used to
generate text "in the author's voice." Drift candidates are flagged as
`TODO:` citing the exact profile rule violated. The author decides whether
to revise.

### Bundled resource

`references/ai-tells.md` — a catalog of AI-tell vocabulary and patterns
("delve", "tapestry", "realm", "underscore", etc.) loaded via
`yoker:skill` with `skill resource=` syntax.

---

## writing-mistakes

**Invocation:** `yoker:skill` with `yoker_writing_assistant:writing-mistakes`

Common writing mistakes with a two-category taxonomy.

### What it does

- **CANONICAL** — a correct form exists (eggcorns, redundancies,
  non-native errors). The skill names the recognized form in a `TODO:` note
  for the author to accept or reject. It never rewrites the sentence.
- **CRAFT** — judgment calls, not correctable forms (passive voice
  overuse, nominalization, vague pronouns). The skill flags and explains;
  the author fixes.

### When to use

- "check my writing for mistakes"
- After a draft is structurally sound but needs a craft pass

### When NOT to use

- Idiom/proverb misuse → `writing-idioms`
- Structural issues → `writing-review`

### Local guardrail

CANONICAL items are the sanctioned exception to the no-prose rule: naming
the correct form is a factual correction, not authoring prose. The
correction is always a `TODO:` or `TODO PROPOSAL:` note — the skill never
rewrites the author's sentence. CRAFT items are flagged with explanation
only.

### Bundled resource

`references/mistakes-taxonomy.md` — the full reference catalog synthesized
from Strunk, Orwell, Williams, Pinker, Zinsser, and non-native-English
references. Loaded via `yoker:skill` with `skill resource=` syntax.

---

## writing-idioms

**Invocation:** `yoker:skill` with `yoker_writing_assistant:writing-idioms`

Idiom and proverb misuse detection.

### What it does

- Detects misused idioms (e.g., "for all intensive purposes" → "for all
  intents and purposes")
- Names the canonical form as a `TODO PROPOSAL:` for the author to accept
  or reject
- Proposes better proverbs when the used one is correct but a stronger
  alternative exists for the context
- Handles ambiguous cases (misuse vs. deliberate creative choice) by asking
  the author rather than asserting

### When to use

- "check my idioms"
- When the author suspects non-native idiom usage

### When NOT to use

- General writing mistakes → `writing-mistakes`
- Voice issues → `writing-voice`

### Local guardrail

Canonical forms are the sanctioned exception: naming the correct idiom is a
factual correction. The correction is always a `TODO PROPOSAL:` — the
skill never rewrites the author's sentence.

---

## writing-split

**Invocation:** `yoker:skill` with `yoker_writing_assistant:writing-split`

Long-form to sequential social post splitting.

### What it does

- Proposes a post sequence from a long article
- Handles platform-specific constraints (character limits, thread
  patterns, hook zones)
- Structures the split — the posts are the author's prose

### When to use

- "split this into posts"
- When the author wants to break a long article into a Twitter/X thread or
  social post sequence

### When NOT to use

- Reordering sections within a single document → `writing-order`
- Platform-specific adaptation of existing content → `copy-writer`

### Local guardrail

The post sequence is proposed as `TODO PROPOSAL:` — the posts are the
author's prose, the skill only structures the split. The skill never
writes post content.

---

## writing-order

**Invocation:** `yoker:skill` with `yoker_writing_assistant:writing-order`

Section reordering for argument flow.

### What it does

- Maps section roles (setup, claim, evidence, counter, resolution, etc.)
- Interviews the author for the argument arc
- Proposes a reordering as persistent text
- Iterates on feedback
- Applies section moves only — no content changes

### When to use

- "reorder this draft" / "the flow doesn't work"
- When the author has a draft with sections in the wrong order

### When NOT to use

- Splitting into multiple posts → `writing-split`
- Structural review (gaps, missing sections) → `writing-review`

### Local guardrail

The reorder proposal is structural — section moves only, no content
changes. The skill works with written sections and `TODO:` stubs alike,
treating both as raw material to arrange. The author writes any new content
needed to fill gaps.

---

## copy-writer

**Invocation:** `yoker:skill` with `yoker_writing_assistant:copy-writer`

Platform-specific content adaptation.

### What it does

- Transforms existing content into platform-specific adaptations
- Preserves the author's personal voice
- Applies platform conventions: character limits, hook zones, hashtag
  norms, content mix ratios, tone adjustments
- Supports: Twitter/X, LinkedIn, Mastodon, Newsletter, Blog
- Supports English and Dutch

### When to use

- "adapt this for LinkedIn" / "adapt for Twitter"
- When the author wants to adapt existing content for specific platforms

### When NOT to use

- Splitting a long article into a post sequence → `writing-split`
- Developmental review → `writing-review`

### Local guardrail

The original content must already exist — the skill transforms, it does
not create. The adaptation preserves the author's voice while applying
platform conventions. Output is presented for review and iteration.

### Bundled resource

`REFERENCE.md` — platform-specific reference with character limits, hook
zones, and key features per platform.