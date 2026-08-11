"""Entry point for yoker-writing-assistant.

Injects ``--with yoker-writing-assistant`` and
``--agent yoker_writing_assistant:writing-assistant`` into Yoker's CLI,
then delegates to Yoker's ``main()``. This allows running the writing
assistant via ``uvx yoker-writing-assistant`` or
``yoker-writing-assistant``.
"""

import sys

from yoker.__main__ import main as yoker_main

from yoker_writing_assistant import __version__


def main() -> None:
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
