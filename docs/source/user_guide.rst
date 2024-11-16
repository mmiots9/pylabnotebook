|PyPI version fury.io| |PyPI license|

.. |PyPI version fury.io| image:: https://badge.fury.io/py/pylabnotebook.svg
   :target: https://pypi.org/project/pylabnotebook/

.. |PyPI license| image:: https://img.shields.io/pypi/l/pylabnotebook.svg
   :target: https://pypi.org/project/pylabnotebook/

CLI Documentation
=======================

This is the official documentation for the CLI version of pylabnotebook. All commands explained here have a corresponding function (see API), but I highly reccomend to run this package from the command line, as it was created for.

Installation
----------------

Pylabnotebook can be installed via `pip` in an isolated environment (suggested):

.. code-block:: console

   (.venv) $ pip install pylabnotebook

To check the installation:

.. code-block:: console

   (.venv) $ labnotebook --version

.. warning::
    Whilst the python dependencies are automatically downloaded and installed, this package highly relies on git. Therefore, there are some git requirements that need to be fullfilled:

    * **git version** >= 2.40.1, otherwise some functionalities do not work
    * **git author and git email** set, otherwise the tool cannot create a notebook, as it checks for git author.



Init a notebook
--------------------------------

To init a new notebook, just type the following code in any folder of a git directory:

.. code-block:: console

   (.venv) $ labnotebook init -n "my project"

A message that confirms the creation of the .labnotebookrc file should appear on the console as stout.

.. note::
    Remember to never change the name of .labnotebookrc file.

Export a notebook
--------------------------------

To export the notebook as a single .html file, from the root of the project type:

.. code-block:: console

   (.venv) $ labnotebook export -o my_project.html

It will create a my_project.html file with the notebook. You can then share the notebook with peers.

Notebook customization
--------------------------------

There are several customization that can be applied to the notebook:

* you can provide your personal css file by setting it in the `.labnotebookrc` file in *LAB_CSS* variable.

* you can decide to show commits from last to first (default) or from first to last (changing *REVERSE_HISTORY* variable in `.labnotebookrc` to True).

* you can change name and author of the notebook in `.labnotebookrc`, it will be passed to file when exporting the notebook.

Link to analysis files
^^^^^^^^^^^^^^^^^^^^^^^^

When exporting the notebook, it automatically create a list of analysis files for each commit with direct links to them (starting from git folder root directory). By default, it takes all the .html files changed/added in that commit (not the deleted or renamed ones).

If you want to add different extensions, you can update the `.labnotebookrc` file by adding/removing extensions in the ANALYSIS_EXT variable. Each extension should be separated by a comma, as it is considered a list (eg. "ANALYSIS_EXT": ['.html', '.txt']): just type the extension, not wildcards or other special characters.

Moreover, changing values inside "ANALYSIS_IGNORE" list, you can exclude some files/folders to be recognized as analysis files (as for a standard .gitignore file it will use wildcards).

If you want to disable all links, pass the `no-link` flag to the export command.

