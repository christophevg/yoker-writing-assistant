"""Tests for yoker_writing_assistant package import safety and manifest."""

import importlib


def test_import_safe():
  """Importing the package must not trigger side effects."""
  mod = importlib.import_module("yoker_writing_assistant")
  assert hasattr(mod, "__YOKER_MANIFEST__")
  assert hasattr(mod, "__version__")


def test_manifest_declares_directories():
  """The manifest must declare agents and skills directories."""
  from yoker_writing_assistant import __YOKER_MANIFEST__

  assert __YOKER_MANIFEST__.agents_dir == "agents"
  assert __YOKER_MANIFEST__.skills_dir == "skills"


def test_manifest_declares_default_agent():
  """The manifest must declare the default agent."""
  from yoker_writing_assistant import __YOKER_MANIFEST__

  assert __YOKER_MANIFEST__.agent == "yoker_writing_assistant:writing-assistant"


def test_version():
  """Version is defined and matches a semver pattern."""
  from yoker_writing_assistant import __version__

  assert __version__ == "0.1.0"
