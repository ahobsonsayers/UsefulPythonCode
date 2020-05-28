
import contextlib
import os
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Dict, List

import git


def execute(cmd: List[str], cwd: str = None, env: Dict = {}):
    print(" ".join(cmd))

    env_dict = {**os.environ, **env}
    env_dict["SYSTEMD_COLORS"] = "1"

    # universal_newlines makes sure outputs strings instead of byits
    with subprocess.Popen(
        cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        bufsize=-1,
        universal_newlines=True,
        cwd=cwd,
        env=env_dict,
    ) as process:
        for line in process.stdout:
            print(line, end="")  # Print line here. End print with empty string instead of newline

    if process.returncode != 0:
        print("Command '{0}' failed with exit code {1}".format(" ".join(process.args), process.returncode))
        sys.exit(process.returncode)


def check_requirements(programs: List[str]):

    for program in programs:
        if shutil.which(program) is None:
            raise Exception("{0} not installed or accessable on the commandline. Exiting".format(program))


@contextlib.contextmanager
def working_directory(path):
    """Changes working directory and returns to previous on exit."""
    prev_cwd = Path.cwd()
    os.chdir(str(path))
    try:
        yield
    finally:
        os.chdir(prev_cwd)


# Get the go communication package
def get_repo(repo: str, directory: Path):

    # Determine whether we need to clone the repo
    clone = False

    # check if directory exists
    if directory.exists() and directory.is_dir():
        # if directory exists, check if it is empty
        if not os.listdir(directory):
            # if directory exits but is empty, clone
            clone = True
    else:
        # if folder doesnt esits, we watn to clone
        clone = True

    # if need to clone the repo, clone it
    if clone:
        git_repo = git.Repo.clone_from(repo, directory)
    else:
        git_repo = git.Repo(directory)
        git_repo.git.reset("--hard")
        git_repo.git.pull("origin", "master")


# See https://bugs.python.org/issue26660
# Took from https://github.com/python/cpython/commit/e9b51c0ad81da1da11ae65840ac8b50a8521373c
# Required for windows as src folder in temp fil refuses to be deleted
def rm_temp(name):
    def onerror(func, path, exc_info):
        if issubclass(exc_info[0], PermissionError):

            def resetperms(path):
                try:
                    os.chflags(path, 0)
                except AttributeError:
                    pass
                os.chmod(path, 0o700)

            try:
                if path != name:
                    resetperms(os.path.dirname(path))
                resetperms(path)

                try:
                    os.unlink(path)
                # PermissionError is raised on FreeBSD for directories
                except (IsADirectoryError, PermissionError):
                    rm_temp(path)
            except FileNotFoundError:
                pass
        elif issubclass(exc_info[0], FileNotFoundError):
            pass
        else:
            raise

    shutil.rmtree(name, onerror=onerror)
