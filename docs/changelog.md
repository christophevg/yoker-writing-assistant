# Changelog

## 0.1.5 (2026-11-23)

### Changed

- **Upgrade to yoker 0.13.0**: dependency relaxed from `yoker>=0.12,<0.13`
  to `yoker>=0.13` (#2). Yoker 0.13.0 requires Python ≥3.11, so the project
  floor moves from 3.10 to 3.11: `requires-python`, classifiers, mypy
  `python_version`, tox env list, and `install-pythons` updated; README,
  `PACKAGE.md`, and `docs/installation.md` synced (also fixed a stale
  `yoker>=0.11.0,<0.12` reference in `PACKAGE.md`).

### Added

- `yoker:send_message` added to the writing-assistant agent tool set
  (yoker 0.13.0 feature, agent definition only).

## 0.1.4 (2026-09-04)

### Changed

- **Upgrade to yoker 0.12**: dependency moved from `yoker>=0.11.0,<0.12`
  to `yoker>=0.12,<0.13`, with the local yoker config cleaned up
  (c3 directories → c4 packages) in the same release train.

## 0.1.3 (2026-08-31)

### Changed

- **Strict Yoker compatibility pin**: dependency tightened from
  `yoker>=0.10.1` to `yoker>=0.11.0,<0.12` (0.11.x only). The `--agent` →
  `--agent-name` CLI rename in yoker 0.11.0 breaks cross-minor-version
  compatibility, so the constraint now tracks the supported minor series.

### Fixed

- CLI wrapper injects `--agent-name` (was `--agent`), matching yoker
  0.11.0's Clevis-generated flag for `Config.agent.name`.
- Documentation updated everywhere: all functional `--agent` references
  (command examples, code snippets, architecture/tutorial text) now use
  `--agent-name`.

## 0.1.2 (2025-07-17)

### Fixed

- Corrected tool usage table in agent definition: loading skill bundled
  resources (`references/`) is done via `yoker:skill`, not `yoker:read`.
- Fixed `writing-voice` skill resource reference syntax from backtick path
  to `skill resource=` syntax for loading `references/ai-tells.md`.
- Added missing trailing newline in `writing-voice/SKILL.md`.

## 0.1.0 (2025-07-17)

### Added

- Initial release of yoker-writing-assistant, a Yoker plugin demonstrating
  the yoker-as-runtime mode.
- Writing assistant agent with 8 skills:
  - `writing-review` — developmental review, claim verification, gap/perspective analysis
  - `writing-continuity` — dangling references, cold terms, dropped themes, missing transitions
  - `writing-voice` — voice drift detection, ChatGPT smell flagging, voice profile checks
  - `writing-mistakes` — common writing mistakes (eggcorns, redundancies, non-native errors)
  - `writing-split` — long-form to sequential social post splitting
  - `writing-order` — section reordering for argument flow
  - `copy-writer` — platform-specific content adaptation (Twitter, LinkedIn, Mastodon)
- Python package with `__YOKER_MANIFEST__` for plugin auto-discovery.
- Thin CLI wrapper (`cli.py`) injecting `--with` and `--agent` flags.
- Non-negotiable rule: the agent never writes prose — every gap becomes `TODO:`,
  every proposal becomes `TODO PROPOSAL:`.
- Optional `c3:researcher` integration for research delegation.
- MIT license.