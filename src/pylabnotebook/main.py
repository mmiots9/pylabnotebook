"""PYLABNOTEBOOK
This module is the main module where all the functions to run the cli of pylabnotebook are defined.
"""
import argparse
import os
from datetime import datetime
import subprocess
import json
import sys
import re
from jinja2 import Environment, FileSystemLoader
from .version import __version__

# Useful values
YELLOW: str = '\033[0;33m'
GREEN: str = '\033[0;32m'
NCOL: str = '\033[0m'
RED: str = '\033[0;31m'


### TODO!! Fix exceptions and errors

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
                                        universal_newlines = True).strip()
    except subprocess.CalledProcessError:
        print("fatal: not a git repository (or any of the parent directories): .git")
        return

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

def export_labnotebook(output_file: str, force: bool, link: bool) -> None:
    """Export labnotebook to html.

    This function exports the labnotebook into a single html file ready to read and share.

    :param output_file: path of the file to create
    :type output_file: str
    :param force: whether to force the overwriting of output_file if exists.
    :type force: bool
    :param link: whether to create links to analysis files in analysis files bullet list. These links can be used to open the analysis files directly from the notebook. # pylint: disable=line-too-long
    :type link: bool

    """

    # 1. Go to git root dir
    try:
        git_root: str = subprocess.check_output(["git", "rev-parse", "--show-toplevel"],
                                        universal_newlines = True).strip()
    except subprocess.CalledProcessError:
        print("fatal: not a git repository (or any of the parent directories): .git")
        return

    os.chdir(git_root)

    # 2. Check for .labnotebookrc
    if not os.path.exists(".labnotebookrc"):
        print(f"{RED}Error: There is no .labnotebookrc file in git repository root folder. Please, run labnotebook create -n <name_of_the_project>") # pylint: disable=line-too-long
        return

    with open(".labnotebookrc", "r", encoding = 'utf8') as config_file:
        config: dict = json.load(config_file)

    # 3. Check if file already exists and force is False
    if os.path.exists(output_file) and not force:
        print(f"{RED}Error: {output_file} already exists. Use -f/--force to overwrite it.")
        return

    # 5. Get list of commits sha
    sha_list: list[str] = get_sha_list(config.get("REVERSE_HISTORY"))

    # 6. Get info about each commit
    analysis_ext: list[str] = config.get('ANALYSIS_EXT')
    excluded_patterns: list[str] = config.get('ANALYSIS_IGNORE')
    commits_info: dict = {sha: get_commit_info(sha, analysis_ext, excluded_patterns) for sha
                          in sha_list}

    # 7. Read style.css
    with open(config.get('LAB_CSS'), 'r', encoding='utf-8') as css_file:
        style_css = css_file.read()

    script_dir: str = os.path.dirname(os.path.abspath(__file__))
    environment = Environment(loader=FileSystemLoader(f"{script_dir}/templates/"))
    template = environment.get_template("base.html")
    content = template.render(config = config,
                              create_date = datetime.today().strftime('%Y-%m-%d'),
                              link = link,
                              commits_info = commits_info,
                              style_css = style_css)

    with open(output_file, mode="w", encoding="utf-8") as message:
        message.write(content)
        print("... wrote test.html")


def get_sha_list(reverse_history: bool) -> list[str]:
    """Get sha list.

    This functions returns a list of commits sha (from oldest to newest) that have not been already 
    included in the notebook.

    :param reverse_history: Whether commits should be returned from first to last.
    :type reverse_history: bool
    :return: list of the commits not included in the notebook since last_commit.
    :rtype: list[str]
    """

    # 1. Get list of all commits
    git_command = ["git", "log", "--pretty=format:%h"]
    if reverse_history:
        git_command.append("--reverse")
    git_sha: list[str] = subprocess.check_output(git_command, text = True).split('\n') # pylint: disable=line-too-long

    # 2. Subset for new commits
    # 2.1 If git history is empty, return error
    if git_sha == ['']:
        print(f"{RED}Error: Git history is empty")
        sys.exit(5)

    return git_sha


def get_commit_info(commit_sha: str, analysis_ext: list[str], excluded_patterns: list[str]) -> dict:
    """Get commit info.

    This function returns a dictionary of the information about the commit specified in commit_sha. 
    These info are: date, author, title, message, changed files and analysis_files (based on both
    analysis_ext and excluded_patterns).

    :param commit_sha: sha of the commit of interest.
    :type commit_sha: str
    :param analysis_ext: list of the file extensions used as reference for analysis files.
    :type analysis_ext: list[str]
    :param excluded_patterns: list of the pattern to be excluded from the analysis files.
    :type excluded_patterns: list[str]
    
    :return: information about the commit specified in commit_sha: date, author, title, message, 
    changed files and analysis_files (based on both analysis_ext and excluded_patterns).
    :rtype: dict
    """
    date, author, title = subprocess.check_output(['git', 'log', '-n', '1', '--pretty=format:%cs%n%an%n%s', commit_sha], text = True).strip().split('\n') # pylint: disable=line-too-long

    # Get message and replace newlines with html breaks
    message: str = subprocess.check_output(['git', 'log', '-n', '1', '--pretty=format:%b', commit_sha], text=True).strip() # pylint: disable=line-too-long
    pattern: str = r"(\.|:|!|\?)\n"
    replacement: str = r"\1<br>\n"
    message = re.sub(pattern, replacement, message).replace('\n\n', '\n<br>\n')

    changed_files: str = subprocess.check_output(['git', 'show', '--pretty=%n', '--name-status', commit_sha], text=True).strip().split('\n') # pylint: disable=line-too-long
    if changed_files == ['']:
        changed_files = {}
    else:
        changed_files: dict = {file.split('\t')[1] : file.split('\t')[0] for file in changed_files}
    analysis_files: list[str] = [key for key, _ in changed_files.items()
                                 if any(ext in key for ext in analysis_ext) and
                                 os.path.isfile(key) and not
                                 any(re.search(pattern, key) for pattern in excluded_patterns)]
    commit_info: dict = {'date': date,
                         'author': author,
                         'title': title,
                         'message': message,
                         'changed_files': changed_files,
                         'analysis_files': analysis_files}

    return commit_info


def main():
    """Main cli function handler.

    This function is the main function of the module, which handles command line input values to run
    the different functions of the labnotebook.
    """
    parser: argparse.ArgumentParser = argparse.ArgumentParser(description="Lab Notebook Tool")
    parser.add_argument('--version', action = 'version', version = '%(prog)s ' + __version__,
                        help = "Show package version")

    subparsers: argparse._SubParsersAction = parser.add_subparsers(dest = "command")

    init_parser: argparse.ArgumentParser = subparsers.add_parser("init",
                                                                 help = "Init labnotebook by creating .labnotebookrc in git root folder.") # pylint: disable=line-too-long
    init_parser.add_argument("-n", "--name", required = True,
                               help="Name of the lab notebook. If the name should contain more words, wrap them into quotes") # pylint: disable=line-too-long

    export_parser: argparse.ArgumentParser = subparsers.add_parser("export", help = "Export lab notebook to an html file") # pylint: disable=line-too-long
    export_parser.add_argument("-o", "--output", required = True,
                               help = "Path/name of the output HTML file")
    export_parser.add_argument("-f", "--force",
                               help = "Force the overwriting of the output file if already present",
                               default = False, action = "store_true")
    export_parser.add_argument("-l", "--link", default = False, action = "store_true",
                               help = "Link style file in head. By default style file is copied in <style></style> tags in head") # pylint: disable=line-too-long

    args = parser.parse_args()

    if args.command == "init":
        init_labnotebook(args.name)
    elif args.command == "export":
        export_labnotebook(args.output, args.force, args.link)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
