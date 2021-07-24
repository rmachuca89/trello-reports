import click.testing
import pytest

from trello_reports import __version__, cli


def test_version():
    assert __version__ == "0.1.0"


@pytest.fixture
def runner():
    return click.testing.CliRunner()


def test_cli_main_succeeds():
    runner = click.testing.CliRunner()
    result = runner.invoke(cli.main)
    assert result.exit_code == 0
