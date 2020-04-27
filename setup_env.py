from pathlib import Path
import json
import subprocess
import re

# Install Dependencies
subprocess.check_output(["poetry", "install"])

# Setup venv path
vscode_settings_filepath = Path("./.vscode/settings.json")

with open(vscode_settings_filepath, "r+") as vscode_settings_file:

    vscode_settings_contents = vscode_settings_file.read()

    poetry_venv_path = subprocess.check_output(["poetry", "env", "info", "-p"], encoding="UTF-8")
    venv_python_path = "{0}/bin/python".format(poetry_venv_path)

    key = "python.pythonPath"
    match = re.compile('"{0}":.*'.format(key))
    replacement = '"{0}": "{1}",'.format(key, venv_python_path)

    # Do the replacement
    vscode_settings_contents = re.sub(match, replacement, vscode_settings_contents)

    vscode_settings_file.seek(0)
    vscode_settings_file.truncate()

    vscode_settings_file.write(vscode_settings_contents)
