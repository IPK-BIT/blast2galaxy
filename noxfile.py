import nox
from nox_poetry import session

nox.options.sessions = ["tests"]
nox.options.default_venv_backend = "mamba"
nox.options.reuse_venv = True

@session(python=["3.10", "3.11", "3.12"], reuse_venv=True)
def tests(session):
    session.conda_install("python=" + session.python)

    #session.install("poetry")
    #session.run("poetry", "install")
    #session.run("poetry", "run", "pytest")

    session.install("pytest", ".")
    session.run("pytest")
