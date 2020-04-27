import subprocess
import shutil
import git
from typing import List, Dict
from pathlib import Path
import sys
import contextlib
import os


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


@contextlib.contextmanager
def working_directory(path):
    """Changes working directory and returns to previous on exit."""
    prev_cwd = Path.cwd()
    os.chdir(str(path))
    try:
        yield
    finally:
        os.chdir(prev_cwd)
