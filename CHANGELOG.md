# 📜 Wordloom Changelog

## [0.2.0] - 2025-10-17
- feat(frontend): unify admin panel toolbar

## [0.4.0] - 2025-10-17
### Added
- Unified project: backend (FastAPI), frontend (Streamlit), assets, and toolkit are now in one repo.
- Added version tracking (`VERSION` files for backend/frontend/assets).
- Introduced .gitignore optimized for multi-language project.
- Added toolkit folder for auxiliary utilities.

### Changed
- Streamlit frontend renamed and reorganized under `WordloomFrontend/streamlit/`.
- Backend refactored for clearer structure (`routers/`, `core/`, `schemas.py`).
- Updated asset path structure with thumbnails and GIF previews.

### Fixed
- Path normalization issue in markdown conversion (`fixpaths.py`).
- Backend database duplication bug during migration.

---

## [0.3.0] - 2025-10-10
### Added
- Initial backend setup with FastAPI.
- Initial frontend migration plan from Streamlit.
