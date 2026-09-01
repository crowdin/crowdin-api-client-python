# AGENTS.md

Python client for the Crowdin API v2 and Crowdin Enterprise API v2 (PyPI: `crowdin-api-client`, import: `crowdin_api`).

Supports Python 3.8+, so write 3.8-compatible code: no `X | Y` unions, no `match`, and import `TypedDict` from `crowdin_api.typing`.

## Layout

- `crowdin_api/client.py` — `CrowdinClient`; one hand-written `@property` per resource
- `crowdin_api/api_resources/<resource>/` — one package per API resource: `resource.py`, `types.py` (request TypedDicts), `enums.py`, `tests/test_<resource>_resources.py`
- `crowdin_api/api_resources/abstract/resources.py` — `BaseResource`
- `crowdin_api/requester.py` — `APIRequester` (session, retries, error mapping)

## Commands

- Install: `pip install -r requirements/requirements-dev.txt`
- Test (all): `pytest` — `setup.cfg` addopts enforce a 95% coverage gate
- Test (one file): `pytest crowdin_api/api_resources/<resource>/tests/test_*.py --no-cov` — without `--no-cov` the coverage gate fails any partial run even when all tests pass
- Lint (what CI runs): `flake8 . --count --show-source --statistics`
- Format: `pre-commit run --all-files` (black `-l 100`, isort, flake8, xenon)

`--doctest-modules` is active: pytest imports every module in `crowdin_api/`, and any `>>>` in a docstring runs as a test.

## Adding or changing an endpoint

Fetch the endpoint spec first (see Crowdin API reference below). Then:

1. Implement the method on the `*Resource` class in `crowdin_api/api_resources/<resource>/resource.py`:
   - List endpoints call `self._get_entire_data(method="get", path=..., params=...)` so `with_fetch_all()` pagination works; everything else calls `self.requester.request(...)`.
   - Project-scoped methods take `projectId: Optional[int] = None` and resolve it via `projectId or self.get_project_id()`.
   - Request body shapes go in `types.py` as TypedDicts; enum values in `enums.py`. Enums and `Sorting` objects can be passed straight into `params`/`request_data` — the custom JSON encoder serializes them, and `None` values are stripped before sending.
   - End the docstring with `Link to documentation:` and the developer.crowdin.com operation URL (pdoc publishes these).
2. For a new resource, register it in three places: an import plus `__all__` entry in `crowdin_api/api_resources/__init__.py` (alphabetical), a `@property` on `CrowdinClient` in `client.py` (copy an existing property; use the enterprise-guard or per-platform variant when the API is Enterprise-only or differs by platform), and one tuple in each of the two parametrize lists in `crowdin_api/tests/test_client.py`. Some resource classes exist but were never registered (e.g. `BranchesResource`, `StringCorrectionsResource`) — "adding" one of those is exactly this registration work.
3. Test in the resource's `tests/` dir: patch the requester with `@mock.patch("crowdin_api.requester.APIRequester.request")`, call the method, then `m_request.assert_called_once_with(method=..., path=..., ...)` with the exact kwargs. The `base_absolut_url` fixture (spelled without the second "e") provides the base URL. No test performs real HTTP.

A complete new resource touches ~8 files: the four package files (`__init__.py` is one line: `__pdoc__ = {'tests': False}`), the resource's test file, and the three registration files.

## Crowdin API reference

Before implementing or changing any endpoint, fetch its spec from the llms.txt indexes (pick by environment, then project type):

- https://support.crowdin.com/_llms-txt/api/crowdin/file-based.txt — Crowdin API, file-based projects (start here)
- https://support.crowdin.com/_llms-txt/api/crowdin/string-based.txt — Crowdin API, string-based projects
- https://support.crowdin.com/_llms-txt/api/enterprise/file-based.txt — Crowdin Enterprise API, file-based projects
- https://support.crowdin.com/_llms-txt/api/enterprise/string-based.txt — Crowdin Enterprise API, string-based projects

Each index links one spec file per route (e.g. `.../api.projects.strings.get.txt`) with the exact request and response shapes.

## Conventions

- Conventional Commits for commit messages and PR titles; CI lints PR titles.
- PRs target `main`.
- Keep the public API backward compatible; mark removals with `@deprecated(...)` (from the `deprecated` package) instead of deleting.
- Never edit `__version__` in `crowdin_api/__init__.py` — the Release workflow bumps it.

## PR checklist

A change is ready when:

1. `pytest` passes, including the 95% coverage gate,
2. `flake8 . --count --show-source --statistics` is clean,
3. every new or changed endpoint method has a test asserting the exact requester call, and
4. every new or changed public method's docstring ends with its documentation link.
