"""
INIT MODULE

This module contains notebook init functions.
"""

import subprocess
import os
import json

from .exceptions import NotGitRepoError

# useful values
GREEN: str = '\033[0;32m'


def init_labnotebook(name: str) -> None:
    """Create new labnotebook.

    This function creates a new labnotebook by creating a new .labnotebook folder with all the 
    necessary files included.

    :param name: Name of the project.
    :type name: str
    """

    # 1. Go to git root dir
    try:
        git_root: str = subprocess.check_output(["git", "rev-parse", "--show-toplevel"],
                                        universal_newlines = True, stderr=subprocess.PIPE).strip()
    except subprocess.CalledProcessError:
        raise NotGitRepoError("fatal: not a git repository (or any of the parent directories): .git") from None # pylint: disable=line-too-long

    os.chdir(git_root)

    # 2. Get useful variables
    aut: str = subprocess.check_output(["git", "config", "--get", "user.name"],
                                       universal_newlines = True).strip()

    # 3. Create config file
    create_config_json(name = name, aut = aut)

    # 4. Return messages
    print(f"\n{GREEN}Created .labnotebookrc in {git_root}. Please edit it if you want to change labnotebook export behaviour.") # pylint: disable=line-too-long


def create_config_json(name: str, aut: str) -> None:
    """Create configuration file.

    This function creates the config.json file of the notebook inside .labnotebook folder.

    :param name: Name of the notebook.
    :type name: str
    :param aut: Author of the notebook.
    :type aut: str
    """
    script_dir: str = os.path.dirname(os.path.abspath(__file__))

    config: dict = {"NOTEBOOK_NAME": f"{name}",
                    "LAB_AUTHOR": f"{aut}",
                    "REVERSE_HISTORY": False,
                    "SHOW_ANALYSIS_FILES": True,
                    "LAB_CSS": f"{script_dir}/templates/style.css",
                    "ANALYSIS_EXT": ['.html'],
                    "ANALYSIS_IGNORE": []}

    filename: str = '.labnotebookrc'
    with open(filename, 'w', encoding = 'utf8') as file:
        json.dump(config, file, indent = 4)
