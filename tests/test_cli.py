"""
CLI Integration Tests
"""

import os

import pytest
from click.testing import CliRunner, Result

from trello_reports import __version__, cli
from trello_reports.reports import (
    ILLEGALSTATEERROR_MSG,
    _test_only_get_todo_board_name,
    _test_only_set_todo_board_name,
)


@pytest.fixture
def runner():
    return CliRunner()


def test_version():
    assert __version__ == "0.1.0"


def test_cli_main_help_succeeds(runner):
    result: Result = runner.invoke(cli.main, ["--help"])

    assert result.exit_code == 0
    assert "Usage:" in result.output


def test_cli_main_succeeds(runner):
    result: Result = runner.invoke(cli.main)

    # TODO: Add coverage for card output. Requires to seed a card first.
    assert result.exit_code == 0
    assert "TODO List Weekly Report" in result.output
    assert "Date:" in result.output


def test_cli_main_invalid_api_keys_displays_error(runner):
    _og_trello_api_key: str = ""
    if os.environ.get("TRELLO_API_KEY"):
        _og_trello_api_key = os.environ.pop("TRELLO_API_KEY")
    _og_trello_api_secret: str = ""
    if os.environ.get("TRELLO_API_SECRET"):
        _og_trello_api_secret = os.environ.pop("TRELLO_API_SECRET")

    result: Result = runner.invoke(cli.main)

    assert result.exit_code == 1
    assert ILLEGALSTATEERROR_MSG in result.output

    os.environ["TRELLO_API_KEY"] = _og_trello_api_key
    os.environ["TRELLO_API_SECRET"] = _og_trello_api_secret


def test_cli_main_no_todo_board_displays_error(runner):
    _test_only_set_todo_board_name("NON-EXISTENT")

    result: Result = runner.invoke(cli.main)

    assert result.exit_code == 1
    assert f"'{_test_only_get_todo_board_name()}' board not found." in result.output
