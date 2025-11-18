3. PyPI Metadata Extraction (`metadata_pypi.csv`)
=================================================

**Goal of this phase:**
- Enrich every labeled package with structured metadata from the PyPI JSON API.
- Produce a resumable metadata table that downstream stages (filtering, graph building, modelling) can use directly.

---

### Input

- `labeled_packages.csv`  
  - `package_name` — PyPI project name  
  - `label` — `1` (malicious), `0` (benign)

---

### Script name

- `fetch_metadata_resumable.py`

---

### Core logic (summary)

1. Load `labeled_packages.csv`.
2. Normalise package names:
   - lowercase + strip
   - drop duplicate `(package_name, label)` rows.
3. Build a “done” set:
   - read `metadata_pypi.csv` (if present) → existing `package_name`s.
   - read `metadata_missing_pypi.csv` (if present) → already-missing `package_name`s.
   - exclude all names in this set from the current run.
4. For each remaining package:
   - query `https://pypi.org/pypi/<package_name>/json` with a bounded timeout.
   - on success, extract:
     - `latest_version`, `num_releases`
     - `first_release_time`, `last_release_time`
     - `summary`, `summary_len`, `description_len`
     - `license`
     - `author`, `author_email`
     - `maintainer`, `maintainer_email`
     - `home_page`, `project_urls_count`
     - `requires_python`
     - `keywords_raw`, `keywords_count`
     - `classifiers_count`
     - plus `package_name`, `label`.
   - on failure (HTTP, timeout, JSON, etc.), record `package_name`, `label`, and `error`.
5. Append results:
   - merge new metadata rows into `metadata_pypi.csv`, de-duplicate on `package_name`.
   - merge new failures into `metadata_missing_pypi.csv`, de-duplicate on `package_name`.

---

### Output files

- `metadata_pypi.csv`  
  Structured PyPI metadata for all successfully resolved packages.

- `metadata_missing_pypi.csv`  
  Packages not resolved via the PyPI API, with the associated error reason.
