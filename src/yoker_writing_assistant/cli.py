"""Entry point for yoker-writing-assistant.

Injects ``--with yoker-writing-assistant`` and
``--agent yoker_writing_assistant:writing-assistant`` into Yoker's CLI,
then delegates to Yoker's ``main()``. This allows running the writing
assistant via ``uvx yoker-writing-assistant`` or
``yoker-writing-assistant``.
"""

import sys

from yoker.__main__ import main as yoker_main


def main() -> None:
  sys.argv = [
    "yoker",
    "--with",
    "yoker_writing_assistant",
    "--agent",
    "yoker_writing_assistant:writing-assistant",
  ] + sys.argv[1:]
  yoker_main()
