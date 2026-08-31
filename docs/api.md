# API Reference

yoker-writing-assistant has a thin public API surface: a plugin manifest, a
CLI entry point, and the packaged agent and skill definitions. Most users
interact with the package via the CLI (`yoker-writing-assistant`) or as a
Yoker plugin loaded by another consumer. The items below are the
programmatic surface.

## `yoker_writing_assistant.__YOKER_MANIFEST__`

The Yoker plugin manifest. Exposed at the package top level so Yoker's
plugin loader discovers it. Declares the agents and skills directories and
the default agent.

```python
from yoker.plugins import PluginManifest

__YOKER_MANIFEST__ = PluginManifest(
  agents_dir="agents",
  skills_dir="skills",
  agent="yoker_writing_assistant:writing-assistant",
)
```

The `__init__.py` is import-safe: importing it does NOT trigger any Agent
construction or session logic. The manifest only declares directories — no
side effects at import time.

## `yoker_writing_assistant.cli.main()`

The CLI entry point. Injects `--with yoker_writing_assistant` and
`--agent-name yoker_writing_assistant:writing-assistant` into Yoker's CLI
and delegates to Yoker's `main()`. Also handles first-run bootstrap: if no
configuration is found, an interactive wizard runs before the CLI args are
injected.

```python
from yoker_writing_assistant.cli import main

main()
```

This is the function registered as the `yoker-writing-assistant` console
script in `pyproject.toml`:

```toml
[project.scripts]
yoker-writing-assistant = "yoker_writing_assistant.cli:main"
```

## `yoker_writing_assistant.__version__`

The package version string, matching the version in `pyproject.toml`.

```python
from yoker_writing_assistant import __version__

print(__version__)  # "0.1.3"
```

## CLI usage

The package is started as a console script or via the Yoker CLI:

```bash
yoker-writing-assistant                         # launch the writing assistant
yoker-writing-assistant --ui-mode batch         # batch mode
yoker-writing-assistant --resume mysession      # resume a session

# or via the Yoker CLI directly:
yoker --with yoker_writing_assistant --agent-name yoker_writing_assistant:writing-assistant
```

Additional CLI flags are appended after the injected args and passed
through to Yoker's CLI.

## Agent and skill definitions

The agent definition lives at
`src/yoker_writing_assistant/agents/writing-assistant.md` and is discovered
by Yoker's plugin loader. The eight skill definitions live at
`src/yoker_writing_assistant/skills/*/SKILL.md`. These are Markdown files
with YAML frontmatter — see [Architecture](architecture.md) for the
delegation model and [Skills](skills.md) for per-skill detail.

## Loading this plugin from another Yoker project

Any external Yoker consumer can load this package as a plugin:

```toml
# ~/.yoker.toml
[plugins]
enabled = true
packages = ["yoker_writing_assistant"]

[plugins.trusted]
yoker_writing_assistant = true
```

Or via the CLI:

```bash
yoker --with yoker_writing_assistant --agent-name yoker_writing_assistant:writing-assistant
```

The agent and all eight skills become available under the
`yoker_writing_assistant:` namespace.