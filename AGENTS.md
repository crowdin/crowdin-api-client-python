# AGENTS.md

## Project Overview

Python client library for Crowdin API v2 and Crowdin Enterprise API v2.

Main structure:
- Source code: `crowdin_api/`
- Tests: `crowdin_api/tests/` and `crowdin_api/api_resources/**/tests/`

## Setup Commands

- Install dependencies: `python -m pip install --upgrade pip && pip install -r requirements/requirements-dev.txt`
- Run tests: `pytest`
- Run one test file: `pytest crowdin_api/api_resources/.../tests/test_*.py`
- Lint: `flake8 . --count --show-source --statistics`

## Code And Testing Expectations

- Add or update unit tests for behavior changes.
- Keep public API and model changes backward compatible unless explicitly intended.
- Follow existing style and lint configuration (`setup.cfg`, `flake8`).
- Keep changes focused and consistent with existing resource patterns.

## Notes For API Details

Always use Crowdin/Crowdin Enterprise `llms.txt` index files for API method details. Choose the correct index by environment first, then project type.

Use these URLs:

- https://support.crowdin.com/_llms-txt/api/crowdin/file-based.txt - Crowdin API (file-based projects, preferred first)
- https://support.crowdin.com/_llms-txt/api/crowdin/string-based.txt - Crowdin API (string-based projects)
- https://support.crowdin.com/_llms-txt/api/enterprise/file-based.txt - Crowdin Enterprise API (file-based projects)
- https://support.crowdin.com/_llms-txt/api/enterprise/string-based.txt - Crowdin Enterprise API (string-based projects)

Each index contains links to method details (for example, `.../api.projects.strings.get.txt`).

## Pull Requests And Commits

- Use Conventional Commits for commit messages and PR titles.
- Before opening a PR, run lint and tests locally.
