"""Nox sessions."""

import nox
from nox.sessions import Session
from nox import session


# Default sessions to run with `nox` command
nox.options.sessions = "lint", "typing", "tests"
# Default packages and files to use within sessions
locations = "trello_reports", "tests", "noxfile.py"

# TODO: Get from configuration.
PYTHON_SUPPORTED_VERSIONS = ["3.11"]


@session(python=PYTHON_SUPPORTED_VERSIONS)
def lint(session: Session) -> None:
    """Run project linters."""
    args = session.posargs or locations
    session.install("flake8", "black", "poetry")
    session.run("flake8", *args)
    session.run("black", "--check", "--diff", *args)
    session.run("poetry", "check")


@session(python=PYTHON_SUPPORTED_VERSIONS)
def typing(session: Session) -> None:
    """Run mypy typing checks."""
    args = session.posargs or locations
    session.install("mypy")
    session.run("mypy", *args)


@session(python=PYTHON_SUPPORTED_VERSIONS)
def tests(session: Session) -> None:
    """Run the test suite."""
    args = session.posargs or ["--cov"]
    session.run_always("poetry", "install", external=True)
    session.run("pytest", *args)


@session
def format(session: Session) -> None:
    """Format project python files with black."""
    args = session.posargs or locations
    session.install("black")
    session.run("black", *args)


@session(python=PYTHON_SUPPORTED_VERSIONS)
def coverage(session: Session) -> None:
    """Upload coverage data to codecov."""
    session.install("coverage[toml]", "codecov")
    session.run("coverage", "xml", "--fail-under=0")
    session.run("codecov", *session.posargs)
