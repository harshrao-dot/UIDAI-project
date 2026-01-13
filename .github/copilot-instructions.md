# Copilot / AI Agent Instructions — Aadhaar Identity Stress System

Purpose
- Give an AI coding agent the minimal, actionable knowledge to be productive quickly in this repo.
- Focus on the _how_, _where_, and notable project-specific patterns rather than general coding advice.

Quick commands
- Install deps: `pip install -r requirements.txt`
- Run full pipeline: `python main_pipeline.py` (outputs saved to `processed_data/`)
- Run quick script/tests: `python test_pipeline.py`, `python test_map.py`, `python test_map_display.py`, `python test_shaded_map.py`
- Launch dashboard locally: `streamlit run app.py`

Big picture (architecture & data flow)
- Source data: three ZIPs expected in project root: `api_data_aadhar_enrolment.zip`, `api_data_aadhar_biometric.zip`, `api_data_aadhar_demographic.zip`.
- Data loader (`data_loader.py`) extracts CSVs in-memory and concatenates them — ZIPs are treated as authoritative.
- Pipeline (`main_pipeline.py`) does: load → aggregate (state/district) → feature engineering → transformations → composite index (AISI) → advanced analytics → forecasting → save outputs.
- Outputs saved to `processed_data/`: `processed_data.csv`, `persistence_index.csv`, `rank_volatility.csv`, `shock_detection.csv`, `early_warnings.csv`, and `results.pkl` (pickled results dict used by `app.py`).

Important project-specific patterns & gotchas
- Minimal abstraction style: functions are small and data-centric; prefer returning DataFrames rather than mutating global state.
- Data transformations: many functions expect columns like `ESS`, `MSP`, `YCR`, `DPI` — ensure these names are preserved if modifying feature engineering.
- AISI implementation: `composite_index.calculate_aisi` uses PCA on available features and falls back to a simple average if fewer than 2 features are present.
- Geo mapping: `india_map_helper.py` normalizes state/district names (`normalize_state_name`, `normalize_district_name`), provides coordinates, and tries to load a local GeoJSON using common filenames: `india_states.geojson`, `data/india_states.geojson`, `processed_data/india_states.geojson`.
  - GeoJSON property detection expects keys like `ST_NM`, `NAME` or first string property as fallback. When adding a new GeoJSON, check the property key.
- Streamlit: `app.py` uses `@st.cache_data` for `load_processed_data()` and will display an error and fallback to CSV reads if `results.pkl` is missing.

Tests & debugging strategy
- Tests are simple script-style smoke checks (print-based), not pytest. Use `python test_pipeline.py` to exercise the end-to-end pipeline.
- For interactive debugging of the dashboard, run `streamlit run app.py` and ensure `processed_data/` contains required CSVs or `results.pkl`.
- When reproducing data issues, run `test_pipeline.py` to see step-by-step printed outputs to identify where rows/columns drop.

When changing code or adding features
- If you introduce new dependencies, add them to `requirements.txt`.
- If you change output column names or produced files, update `main_pipeline.py` saving logic and `app.py` loading logic accordingly.
- Maintain the in-memory ZIP-loading behavior unless there is a clear reason to change it; downstream code assumes it.
- Add/keep short docstrings and small comments explaining *why* (this repo values brief, human-oriented comments).
- Add or update a test script that demonstrates the change (follow current style — script that prints success checks).

Examples (copy-paste friendly)
- Run only pipeline (same as CI smoke): `python main_pipeline.py`
- Check PCA fallback behavior quickly: run `python -c "from composite_index import calculate_aisi; import pandas as pd; print(calculate_aisi(pd.DataFrame({'ESS':[0.1]})))"`
- Validate map loading: ensure `processed_data/india_states.geojson` exists or place a GeoJSON in repo root and run `python test_map.py`.

Permissions & data
- ZIP files are expected to be present locally; no network downloads are implemented by default (see `scripts/` for geojson helpers).

PR / code review tips for agents
- Check that `requirements.txt` is updated if new libs are added.
- Ensure `results.pkl` and CSV saving remains consistent so `app.py` can load either `results.pkl` (preferred) or CSV fallbacks.
- Prefer small, focused changes and include a smoke-check script demonstrating the new behavior.

If anything is unclear
- Ask the maintainer which ZIP files are canonical (the repo treats the three ZIPs as authoritative). If adding/removing features that change the public schema of `processed_data.csv`, ask for a confirmation before altering downstream code such as the dashboard.

---
Please review these notes and tell me if you'd like me to add project-specific CI examples, pre-commit hooks, or more granular coding/naming rules (I can draft those too).