# Quickstart

This page walks through a first session end-to-end. You should have already
finished [Installation](installation.md) — `~/.yoker.toml` configured with a
backend and `enabled = true`, and `make env-dev` green (or `uvx` ready).

## Launch the assistant

```bash
make run
# or
uvx yoker-writing-assistant
# or
yoker --with yoker_writing_assistant --agent yoker_writing_assistant:writing-assistant
```

The assistant starts with an interactive prompt. On first run without
configuration, the bootstrap wizard guides you through backend setup.

## A first session: reviewing a draft

Here is a worked example showing what the assistant does with a draft
article. Save this as `my-draft.md`:

```markdown
# The Case Against AI-Generated Code

AI is transforming software development. Everyone is using it. It's really
amazing. In this article I argue that we should be cautious.

## The Promise

Copilot can write boilerplate fast. This is a game-changer for
productivity. Developers can focus on the interesting parts.

## The Problem

The problem is that AI doesn't understand context. It generates code
that looks right but might be wrong.
```

Now tell the assistant:

```
Review the structure of my-draft.md — is the argument coherent?
```

The assistant will:

1. **Read the draft** and present a plan — which skills it will invoke and
   what it will check — then wait for your go-ahead.
2. **Execute the plan** — invoke `writing-review` for developmental review
   and `writing-continuity` for continuity checking, in parallel.
3. **Insert `TODO:` and `TODO PROPOSAL:` markers** inline into your draft
   as HTML comments, and produce an advisory report.
4. **End with "What this did NOT check"** — the scope limits of the review.

Here is what the assistant produces (abridged from a real session):

### The plan

```
I've read the draft. Here's my plan before I touch anything:

 1. Structural pass — I'll delegate to writing-continuity for dangling
    refs / cold terms / dropped themes, and writing-review for claim
    extraction, gap analysis, and an advisory report. Every finding
    becomes a TODO: or TODO PROPOSAL: marker in your draft.
 2. Voice pass — I'll check if ~/VOICE.md exists and, if so, delegate
    to writing-voice for drift detection.

I will not write or rewrite any prose. I'll insert inline TODO: /
TODO PROPOSAL: markers only.

Shall I go ahead?
```

### The advisory report

After you say "yes," the assistant invokes the skills, applies both
methodologies, and inserts markers into your draft. The advisory report
looks like this:

```
Review Report: "The Case Against AI-Generated Code"

Executive summary
The draft has a clear two-section skeleton (Promise → Problem) but the
argument never lands. The title promises a dismantling case; the thesis
promises caution — these are different stances. The promise section is
uncritical and evidence-free; the problem section raises a claim but
never tests it. There is no resolution section that synthesizes the two
into the cautious recommendation the thesis announces.

Critical issues

 #  Location          Issue
 1  Title + Intro     Title–thesis mismatch. "The Case Against" ≠ "we
                      should be cautious." The first is a prosecution;
                      the second is a guardrail. Pick one.
 2  Intro             "Everyone is using it" — overstatement presented as
                      fact. If you mean widespread adoption, say so and
                      cite a statistic.
 3  Intro             "It's really amazing" — opinion as fact. Is this
                      your genuine position or throat-clearing?
 4  "The Problem"     "AI doesn't understand context" — cold term, never
                      defined, and potentially outdated. Needs definition
                      + verification.
 5  Whole draft       No resolution section. The argument arc is promise →
                      problem → nothing. Where does the argument land?

Coverage analysis

 Topic                        Depth    Note
 Productivity benefits        Shallow  Claimed, not evidenced
 Failure modes                Shallow  Asserted, not demonstrated
 Mitigation strategies        Missing  How do teams work with AI safely?
 Evidence / studies           Missing  No citations anywhere
 Resolution / recommendation  Missing  Thesis never developed
 Counter-perspective          Missing  No steelman of the pro-AI position

Perspective analysis

Steelman of the opposition to your argument: AI-generated code is
reviewed by humans, tested by CI, and caught by type systems — the same
guardrails that catch human errors. The "looks right but might be wrong"
problem is not unique to AI; it describes junior developers too. Why is
AI-caused wrongness categorically different from human-caused wrongness,
rather than a difference of degree? You need to answer this for the
"case against" to hold.

What this did NOT check
 • Voice drift / ChatGPT smell — no voice profile available. Consider
   creating ~/VOICE.md so future reviews can check drift.
 • Idiom / proverb misuse — not checked in this pass.
 • Common writing mistakes — not checked in this pass.
 • Factual claim verification via external sources — claims were flagged
   for verification but not verified.
 • Sentence-level copy-editing — outside scope. The author fixes prose.
```

### The marked-up draft

The assistant inserts `TODO:` and `TODO PROPOSAL:` markers as HTML
comments directly into your draft file. Your prose is untouched — only
markers are added:

```markdown
# The Case Against AI-Generated Code

AI is transforming software development. Everyone is using it. It's really
amazing. In this article I argue that we should be cautious.

<!-- TODO: Title–thesis mismatch. The title "The Case Against AI-Generated
Code" promises a dismantling argument. The thesis "we should be cautious"
promises a moderation argument. These are different stances — decide which
one this article is. -->
<!-- TODO: "Everyone is using it" is an overstatement — not literally true.
If you mean "adoption is widespread," say that and consider citing an
adoption statistic. -->
<!-- TODO PROPOSAL: Consider whether the intro should preview the argument
arc (promise → problem → ???). Right now the reader has no map of where the
article is going. -->

## The Promise

Copilot can write boilerplate fast. This is a game-changer for
productivity. Developers can focus on the interesting parts.

<!-- TODO: "game-changer" is a hype-vocabulary flag — vague superlative with
no specifics. What concrete productivity gain are you claiming? -->
<!-- TODO: This section has no evidence. "Copilot can write boilerplate fast"
is a factual claim that needs verification (min. 2 independent sources). -->

## The Problem

The problem is that AI doesn't understand context. It generates code
that looks right but might be wrong.

<!-- TODO: "doesn't understand context" is a strong factual claim. What does
"understand context" mean precisely? This is a cold term — used as if
established, never defined. -->
<!-- TODO: Coverage gap — the article has "The Promise" and "The Problem" but
no resolution. Where does the argument land? -->
<!-- TODO PROPOSAL: Consider a third section — e.g., "The Practice" or "The
Middle Ground" — that takes the promise and the problem and delivers the
cautious stance the thesis promises. -->
```

The key thing to notice: **the assistant never wrote a single sentence of
prose.** Every gap is a `TODO:` for you to fill. Every proposal is a
`TODO PROPOSAL:` for you to accept, reject, or ignore. The friction is the
value — you do the thinking, the assistant surfaces where the thinking is
incomplete.

## On-demand single checks

You can invoke any individual skill directly:

| Request | Skill invoked |
|---------|---------------|
| "check my voice" | `writing-voice` |
| "check my writing for mistakes" | `writing-mistakes` |
| "check my idioms" | `writing-idioms` |
| "check continuity" | `writing-continuity` |
| "review this draft" | `writing-review` |
| "split this into posts" | `writing-split` |
| "reorder this draft" | `writing-order` |
| "adapt this for LinkedIn" | `copy-writer` |

## Interview mode

Before you have a draft, the assistant can interview you to extract and
structure your thinking:

```
Interview me about my positioning for an article on agent safety.
```

The assistant asks one question at a time, pushes for concrete examples,
points out contradictions, and keeps an interview log. Your answers become
the raw material for the draft — but the assistant never writes the draft
for you.

## Next

Read the [Tutorial](tutorial.md) for the full build story — why this package
exists, the non-negotiable rule, the thin-orchestrator architecture, the
eight skills, and the optional researcher integration.