"""Entry point for yoker-writing-assistant.

Injects ``--with yoker-writing-assistant`` and
``--agent yoker_writing_assistant:writing-assistant`` into Yoker's CLI,
then delegates to Yoker's ``main()``. This allows running the writing
assistant via ``uvx yoker-writing-assistant`` or
``yoker-writing-assistant``.

Pre-flight bootstrap: before injecting any CLI args (which would mask the
no-config case), we check ``config_provided()``. When no configuration is
found, the interactive bootstrap wizard runs so the user can create one.
After the wizard writes ``~/.yoker.toml`` the user must manually edit it to
set ``enabled = true`` — completing the wizard does not enable Yoker.
"""

import asyncio
import sys

from yoker.__main__ import main as yoker_main
from yoker.bootstrap import BootstrapResult, BootstrapWizard, config_provided
from yoker.bootstrap.steps import DOCS_HOME_URL
from yoker.ui import InteractiveUIHandler

from yoker_writing_assistant import __version__


def _run_bootstrap_wizard() -> None:
  """Run the first-run bootstrap wizard when no config is found.

  Interactive (TTY): runs ``BootstrapWizard`` so the user can configure a
  provider and model. The wizard writes ``~/.yoker.toml`` with ``enabled =
  false`` (Config defaults) — the user must then manually set ``enabled =
  true`` and re-run.

  Non-interactive (no TTY): aborts with a message pointing to the docs.
  """
  if not sys.stdin.isatty():
    sys.stderr.write(
      f"No yoker configuration found at ~/.yoker.toml or ./yoker.toml.\n"
      f"Run `yoker-writing-assistant` interactively to configure, "
      f"or see {DOCS_HOME_URL}\n"
      "Aborting (non-interactive mode).\n"
    )
    sys.exit(1)

  # history_file="none" prevents bootstrap prompts (including API keys) from
  # being persisted to ~/.yoker_history.
  ui = InteractiveUIHandler(history_file="none", show_prompts=False)
  try:
    result = asyncio.run(BootstrapWizard(ui).run())
  except KeyboardInterrupt:
    sys.stderr.write("Aborted. No configuration written.\n")
    sys.exit(0)

  if result == BootstrapResult.WRITTEN:
    sys.stdout.write(
      "\nConfiguration written to ~/.yoker.toml.\n"
      "Edit it and set `enabled = true` to acknowledge the risks of running\n"
      "an LLM-powered agent, then re-run `yoker-writing-assistant`.\n"
    )
    sys.exit(0)

  # MANUAL or ABORTED: the wizard already emitted its message.
  sys.exit(0)


def main() -> None:
  # Pre-flight: detect missing configuration before injecting CLI args.
  # Our injected flags (--agent, --harness-*, --plugins-enabled) would make
  # config_provided() always return True, masking the no-config case.
  if not config_provided():
    _run_bootstrap_wizard()

  sys.argv = (
    [
      "yoker",
      "--with",
      "yoker_writing_assistant",
      "--agent",
      "yoker_writing_assistant:writing-assistant",
      "--harness-name",
      "yoker-writing-assistant",
      "--harness-version",
      __version__,
      "--harness-author",
      "Christophe VG",
      "--motd-title",
      "WritingAssistant",
      "--motd-version",
      __version__,
      "--motd-font",
      "small",
      "--plugins-enabled",  # you wanted to run it, so...
      # "--plugins-trusted-yoker_writing_assistant"  # plugins can't self-trust ;-)
    ]
    + sys.argv[1:]
  )
  yoker_main()
