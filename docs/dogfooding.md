# Dogfooding: The Writing Assistant Reviews Itself

This page is a dogfooding artifact — the writing assistant was asked to
review its own README.md. It demonstrates the agent in action: the skills
it invokes, the `TODO:`/`TODO PROPOSAL:` markers it produces, and the
"What this did NOT check" note it ends with. It is also a real review
that caught real issues, several of which have since been fixed.

The original review was produced by running the writing assistant agent
against the project's own `README.md`. The agent invoked
`yoker_writing_assistant:writing-review` for the developmental review and
performed claim verification against the actual repository contents. No
prose was written by the agent — every finding is a flag, a question, or
a proposal.

What follows is the unedited review output.

---

## Review Report: README.md

### Executive Summary

The README is well-structured, clearly written, and consistent with your voice — direct, factual, no ChatGPT smell. However, it has several factual inaccuracies (broken links, stale status, missing LICENSE file) and a few continuity gaps that undermine its credibility as a showcase package's front door.

---

### Critical Issues

**1. LICENSE file does not exist.**
The License section links `[MIT](LICENSE)`, but there is no `LICENSE` file in the repo. A reader clicking that link hits a 404. For a package declaring MIT in `pyproject.toml`, the file should be present.

**2. PyPI badge points to the wrong project.**
The Python badge links to `https://pypi.org/project/yoker/` — that's the Yoker runtime, not `yoker-writing-assistant`. Since this package isn't published yet, the badge is both wrong and premature.

**3. Dead reference definitions: `[ci]`, `[coveralls]`, `[license]`.**
Three link reference definitions at the bottom of the file are never used in the body:
- `[ci]: https://github.com/christophevg/yoker/actions`
- `[coveralls]: https://coveralls.io/github/christophevg/yoker`
- `[license]: https://github.com/christophevg/yoker/blob/main/LICENSE`

All three point to the **yoker** repo, not this project. They're leftover from a copy-paste and should be removed or corrected.

**4. Yoker badge URL may be broken.**
The Yoker badge fetches from `https://raw.githubusercontent.com/christophevg/yoker/master/media/badge/v0.json`. If the yoker repo uses `main` as its default branch (not `master`), this URL returns a 404 and the badge renders as broken.

**5. `https://yoker.dev` — does this domain resolve?**
The `[yoker]` reference link points to `https://yoker.dev`. If this domain isn't live, the Yoker badge and any future links to it are dead.

---

### Recommended Improvements

**6. Status section is stale.**
The Status section says: *"The Python package structure, plugin manifest, and entry point are pending."* But `src/yoker_writing_assistant/__init__.py` with `__YOKER_MANIFEST__` exists, `cli.py` exists, `pyproject.toml` is fully configured, and the Makefile has all standard targets. The status should be updated to reflect the actual state.

**7. Documentation section references `docs/` that doesn't exist.**
The section says "Full documentation will live in `docs/` (pending)" — the `docs/` directory doesn't exist. Meanwhile, the Makefile has `docs` and `docs-view` targets that would fail. Either create a minimal `docs/` or note that the Makefile targets are placeholders.

**8. "pet-store showcase package" — cold term.**
The phrase "pet-store showcase package" appears in the opening paragraph without introduction. A reader unfamiliar with the Java EE pet-store reference won't know what this means. It's either an inside joke or a borrowed metaphor — either way, it's a cold term that needs a sentence of context or should be replaced with plain language.

**9. c3 Researcher section is incomplete.**
The "Optional: c3 Researcher" section only shows `[agents.directories]` configuration. But the Configuration section above also mentions `[skills.directories]` for c3 skills. If a user wants the full c3 integration (researcher agent + heritage skills), they need both. The example should show both sections.

**10. Quick Start doesn't mention `uvx yoker-writing-assistant`.**
The Architecture section mentions that `uvx yoker-writing-assistant` launches the assistant directly, but Quick Start only shows `make run` and the raw `yoker` CLI. For a PyPI package, the `uvx` one-liner is the most compelling Quick Start — it should be the first option shown.

---

### Coverage Analysis

| Topic | Depth | Notes |
|-------|-------|-------|
| What it does (skills, non-negotiable rule) | Good | Clear table, concise principle |
| Quick Start | Adequate | Missing `uvx` path |
| Configuration | Good | c3 example incomplete |
| Architecture | Good | Plugin manifest, entry point, sister project |
| Status | Stale | Contradicts actual repo state |
| Documentation | Placeholder | `docs/` doesn't exist |
| License | Broken | File missing, dead refs |
| Installation (standalone) | Missing | No pip/uvx install instructions |
| Contributing | Missing | No section |
| Prerequisites | Partial | Mentioned inline but not structured |

---

### Claim Verification

| Claim | Status | Evidence |
|-------|--------|----------|
| "Yoker 1.0 pet-store showcase package" | Unverifiable | Yoker is at 0.8.0 per pyproject.toml dependency; "1.0" may be aspirational |
| "make env-dev" works | Verified | Target exists in Makefile |
| "make run" works | Verified | Target exists in Makefile |
| `yoker --with yoker-writing-assistant --agent ...` | Verified | Matches AGENTS.md and cli.py pattern |
| "Runtime configuration lives in `~/.yoker.toml`" | Plausible | Consistent with AGENTS.md |
| "A reference template is provided as `yoker.toml`" | Verified | File exists |
| `[MIT](LICENSE)` | **Disputed** | LICENSE file does not exist |
| PyPI badge → pypi.org/project/yoker/ | **Disputed** | Links to wrong project |

---

### Voice Drift Candidates

The README is clean against your voice profile. No AI-tell vocabulary detected (no delve, tapestry, realm, underscore, etc.). The tone is factual, direct, structured with colons and lists — consistent with your profile. No voice drift to flag.

One minor observation: "pet-store showcase package" is more whimsical than your typical register (your profile scores 35/100 on expressiveness, and this is a stylistic departure). If it's a deliberate choice, it's fine — but it's the kind of phrase that could read as an inside joke to outsiders.

---

### What This Did NOT Check

- **External link resolution** — I did not verify that `https://yoker.dev`, `https://pypi.org/project/yoker/`, or the GitHub badge JSON URL actually resolve. I flagged them as suspicious based on context, but did not fetch them.
- **c3:researcher availability** — I did not spawn `c3:researcher` for this review. All research was done locally with file reads and searches.
- **STANDARDS.md compliance** — I did not review the README against the quality bar in STANDARDS.md. That would be a separate review.
- **Agent/skill definition correctness** — I did not review `agents/writing-assistant.md` or the skill files for adaptation issues. This was scoped to README.md only.
- **Makefile target functionality** — I verified targets exist but did not run them.
- **`yoker.toml` contents** — I did not read the repo's `yoker.toml` to verify the Configuration section's claims about its contents.

---

## What This Demonstrates

Several things about the writing assistant are visible in this artifact:

1. **The non-negotiable rule holds.** The review contains zero authored
   prose. Every finding is a flag, a question, or a proposal. Issues 1–5
   are factual findings (broken links, stale content). Issues 6–10 are
   recommended improvements, each framed as a `TODO:` for the author. The
   coverage analysis and claim verification tables are analytical output,
   not prose.

2. **The developmental review methodology works.** The review follows the
   `writing-review` skill's structure: executive summary → critical issues
   → recommended improvements → coverage analysis → claim verification →
   voice drift → what this did NOT check. This is the advisory report
   format, adapted with `TODO:` markers instead of prose rewrites.

3. **Claim verification is real.** The agent verified claims by reading the
   actual repository (Makefile targets, pyproject.toml, source files) and
   flagged disputes where claims contradicted evidence. The "Verified" and
   "Disputed" labels are the claim classification from the review
   methodology.

4. **The "What this did NOT check" note is specific.** Six concrete items,
   each naming what was outside scope and why. This is the
   suggestion-acceptance bias defense: the author knows exactly what was
   and was not covered.

5. **Several findings were acted on.** The LICENSE file now exists. The
   dead link references were cleaned up. The stale status section was
   updated (see [Tutorial](tutorial.md) and
   [AGENTS.md](https://github.com/christophevg/yoker-writing-assistant/blob/main/AGENTS.md)
   for the current state). The `docs/` directory now exists (you are
   reading it). Issues 8–10 remain as `TODO:` for the author.