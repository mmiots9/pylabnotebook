.. Pylabnotebook documentation master file.

Welcome to pylabnotebook's documentation.
==============================================

Pylabnotebook is a small python package born by the need of having the git log history sharable in a prettier way to collegues who do not know anything about git or do not have access to the git folder.

As bioinformatician, I use it a lot for my analysis, as I always commit after each analysis and then I share my pylabnotebook to collegues and supervisors. I usually put the notebook in the root folder of a git repo, as it has direct links to analysis html notebooks (coming from rmd or jupyter notebooks for example).

View and example of labnotebook |example_link|.

For reporting bugs or other issues with pylabnotebook please use: https://github.com/mmiots9/pylabnotebook/issues.

For any other questions please contact us via miotsdata@gmail.com.

What's new in version 0.3.0
------------------------------------

Added
^^^^^^^^^^

-  Button to move faster from top to bottom of the notebook (useful for very long notebooks)

Changed
^^^^^^^^^

- Changed the backend to Jinja2
- Changed the way how configurations are set
- From .pylabnotebook folder to a single .pylabnotebookrc config file

.. |example_link| raw:: html

   <a href="./_static/example.html" target="_blank">here</a>

.. toctree::
   :caption: Tool Guide:

   user_guide

.. toctree::
   :maxdepth: 4
   :caption: API:

   src_code