"""yoker-writing-assistant — a writing coach plugin for Yoker.

This package is yoker-as-runtime: Yoker is the entry point, and this package
provides the main agent and skills for an interactive writing coaching
session. It is also a Yoker plugin: the ``__YOKER_MANIFEST__`` below
declares the agents and skills directories.

This module is import-safe: importing it must NOT trigger any Agent
construction or session logic. The manifest only declares directories —
no side effects at import time.
"""

from yoker.plugins import PluginManifest

__version__ = "0.1.1"

__YOKER_MANIFEST__ = PluginManifest(
  agents_dir="agents",
  skills_dir="skills",
  agent="yoker_writing_assistant:writing-assistant",
)

__all__ = ["__YOKER_MANIFEST__", "__version__"]
