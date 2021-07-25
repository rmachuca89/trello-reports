import nox

locations = "trello_reports", "tests", "noxfile.py"
nox.options.sessions = "lint", "typing", "tests"


@nox.session(python=["3.9", "3.8", "3.7"])
def tests(session):
    args = session.posargs or ["--cov"]
    session.run("poetry", "install", external=True)
    session.run("pytest", *args)


@nox.session
def lint(session):
    args = session.posargs or locations
    session.install("flake8", "black")
    session.run("flake8", *args)
    session.run("black", "--check --diff", *args)


@nox.session
def format(session):
    args = session.posargs or locations
    session.install("black")
    session.run("black", *args)


@nox.session
def typing(session):
    args = session.posargs or locations
    session.install("mypy")
    session.run("mypy", *args)
