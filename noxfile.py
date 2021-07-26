import nox

locations = "trello_reports", "tests", "noxfile.py"
nox.options.sessions = "lint", "typing", "tests"


@nox.session(python=["3.9"])
def lint(session):
    args = session.posargs or locations
    session.install("flake8", "black", "poetry")
    session.run("flake8", *args)
    session.run("black", "--check", "--diff", *args)
    session.run("poetry", "check")


@nox.session(python=["3.9"])
def typing(session):
    args = session.posargs or locations
    session.install("mypy")
    session.run("mypy", *args)


@nox.session(python=["3.9"])
def tests(session):
    args = session.posargs or ["--cov"]
    session.run("poetry", "install", external=True)
    session.run("pytest", *args)


@nox.session
def format(session):
    args = session.posargs or locations
    session.install("black")
    session.run("black", *args)
