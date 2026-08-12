# Changelog

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
  - `writing-idioms` — idiom/proverb misuse flagging with canonical form proposals
  - `writing-split` — long-form to sequential social post splitting
  - `writing-order` — section reordering for argument flow
  - `copy-writer` — platform-specific content adaptation (Twitter, LinkedIn, Mastodon)
- Python package with `__YOKER_MANIFEST__` for plugin auto-discovery.
- Thin CLI wrapper (`cli.py`) injecting `--with` and `--agent` flags.
- Non-negotiable rule: the agent never writes prose — every gap becomes `TODO:`,
  every proposal becomes `TODO PROPOSAL:`.
- Optional `c3:researcher` integration for research delegation.
- MIT license.