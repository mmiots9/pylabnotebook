.. Pylabnotebook documentation master file.

Welcome to pylabnotebook's documentation.
==============================================

For reporting bugs or other issues with pylabnotebook please use: https://github.com/mmiots9/pylabnotebook/issues.

For any other questions please contact us via miotsdata@gmail.com.

View and example of labnotebook |example_link|.

What's new in version 0.2.0
------------------------------------

Changed
^^^^^^^^^^

- New default style for the output notebook.

Fixed
^^^^^^^^^

- New behaviour for newlines in message section. It will now put a newline tag whenever it finds a newline sign from the original commit message which follows a fullstop, a question mark, an exclamation mark or a colon.
- Updated version of example page in documentation.

.. |example_link| raw:: html

   <a href="./_static/example.html" target="_blank">here</a>

.. toctree::
   :caption: Tool Guide:

   user_guide

.. toctree::
   :maxdepth: 4
   :caption: API:

   src_code