"""Nox sessions."""
import nox
from nox.sessions import Session


locations = "trello_reports", "tests", "noxfile.py"
nox.options.sessions = "lint", "typing", "tests"


@nox.session(python=["3.9"])
def lint(session: Session) -> None:
    """Run project linters."""
    args = session.posargs or locations
    session.install("flake8", "black", "poetry")
    session.run("flake8", *args)
    session.run("black", "--check", "--diff", *args)
    session.run("poetry", "check")


@nox.session(python=["3.9"])
def typing(session: Session) -> None:
    """Run mypy typing checks."""
    args = session.posargs or locations
    session.install("mypy")
    session.run("mypy", *args)


@nox.session(python=["3.9"])
def tests(session: Session) -> None:
    """Run the test suite."""
    args = session.posargs or ["--cov", "-m", "not e2e"]
    session.run("poetry", "install", external=True)
    session.run("pytest", *args)


@nox.session
def format(session: Session) -> None:
    """Format project python files with black."""
    args = session.posargs or locations
    session.install("black")
    session.run("black", *args)


@nox.session(python="3.9")
def coverage(session: Session) -> None:
    """Upload coverage data to codecov."""
    session.install("coverage[toml]", "codecov")
    session.run("coverage", "xml", "--fail-under=0")
    session.run("codecov", *session.posargs)
