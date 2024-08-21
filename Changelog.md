# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added

- Sidebar with links to dates in order (to move easier throughout the document).
- Configuration command for cli.
- Notebook commit command.

## [0.2.0] - 2024-08-21

### Changed

- New default style for the output notebook.

### Fixed

- New behaviour for newlines in message section. It will now put a newline tag whenever it finds a newline sign from the original commit message which follows a fullstop, a question mark, an exclamation mark or a colon.
- Updated version of example page in documentation.

[unreleased]: https://github.com/mmiots9/pylabnotebook/compare/v0.2.0...HEAD
[0.2.0]: https://github.com/mmiots9/pylabnotebook/compare/v0.1.11...v0.2.0
