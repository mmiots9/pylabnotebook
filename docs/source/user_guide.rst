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



Create a notebook
--------------------------------

To create a new notebook, in the root folder of the project (the one that has the .git folder), type this command:

.. code-block:: console

   (.venv) $ labnotebook create -n "my project"

A message that confirms the creation of the .labnotebook folder should appear on the console as stout.

.. note::
    Remember to never change the name of .labnotebook folder or any file inside of it.

Update a notebook
--------------------------------

Prior to export the final .html version of the notebook, you have to update the file inside .labnotebook folder through this command (from the root folder of the project):

.. code-block:: console

   (.venv) $ labnotebook update

This command will evaluate git history from the last commit stored in .labnotebook/config.json. This means that, if the git history has changed and the last commit in .labnotebook/config.json is *not* in the new git history, this will raise an error. To prevent this error, you could force labnotebook update to start from the beginning of git history through the `-f/--force` flag.

Link to analysis files
^^^^^^^^^^^^^^^^^^^^^^^^

When updating the notebook, it automatically create a list of analysis files for each commit with direct links to them. By default, it takes all the .html files changed/added in that commit.
If you want to add different extensions, you can update the .labnotebook config.json file by adding/removing extensions in the ANALYSIS_EXT variable. Each extension should be separated by a comma, as it is considered an array (eg. "ANALYSIS_EXT": ['.html', '.txt']): just type the extension, not wildcards or other special characters.
Moreover, by creating a ".labignore" file, you can exclude some files/folders to be recognized as analysis files (as for a standard .gitignore file it will use wildcards).

Export an html notebook
--------------------------------

To export the notebook as a single .html file, from the root of the project type:

.. code-block:: console

   (.venv) $ labnotebook export -o my_project.html

It will create a my_project.html file with the notebook. You can then share the notebook with peers.

.. note:: 
    You can customize the style of your notebook by either edit style.css file in .labnotebook folder, or provide a custom.css file and reference it in .labnotebook/config.json file (as a path starting from the root of your project).
