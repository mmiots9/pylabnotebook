# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added

- Sidebar with links to dates in order (to move easier throughout the document).
- Configuration command for cli.

## [0.3.0] - 2024-10-30

### Added

- Button to move faster from top to bottom of the notebook (useful for very long notebooks)

### Changed

- Changed the backend to Jinja2
- Changed the way how configurations are set
- From .pylabnotebook folder to a single .pylabnotebookrc config file

## [0.2.1] - 2024-09-11

### Added

- New notebook commit command that commits changes in .labnotebook folder.

### Fixed

- Remove link to non-existing analysis files (deleted or renamed in the commit).

## [0.2.0] - 2024-08-21

### Changed

- New default style for the output notebook.

### Fixed

- New behaviour for newlines in message section. It will now put a newline tag whenever it finds a newline sign from the original commit message which follows a fullstop, a question mark, an exclamation mark or a colon.
- Updated version of example page in documentation.

[unreleased]: https://github.com/mmiots9/pylabnotebook/compare/0.3.0...HEAD
[0.3.0]: https://github.com/mmiots9/pylabnotebook/compare/0.2.1...0.3.0
[0.2.1]: https://github.com/mmiots9/pylabnotebook/compare/0.2.0...0.2.1
[0.2.0]: https://github.com/mmiots9/pylabnotebook/compare/v0.1.11..v0.2.0
