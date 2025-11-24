## Benchmark Dataset Construction

**Goal:** Build a labeled benchmark set of PyPI packages for training/evaluation.

**Inputs**
- `master_malicious_pypi_list.txt` — all unique malicious PyPI names (after merging all sources).
- `hugovk-top-pypi-packages-30-days.csv` — top downloaded PyPI projects (benign candidates).
- `benign_candidates_top_pypi.txt` — benign names after removing all malicious.
- `labeled_packages.csv` — final combined label file.

---

### 1. Build Benign Candidate Set

Script: `build_benign_candidates.py`

Logic:
1. Load `master_malicious_pypi_list.txt` into a `malicious` set.
2. Load `hugovk-top-pypi-packages-30-days.csv`.
3. Keep top 15,000 rows and normalize `project` to lowercase.
4. Drop any `project` that appears in `malicious`.
5. Deduplicate while preserving order → write to `benign_candidates_top_pypi.txt`.

Result:
- Malicious: **8,922**
- Benign candidates (Top PyPI after removal): **14,102**

---

### 2. Build Final Labeled Dataset

Script: `build_labeled_packages.py`

Logic:
1. Load malicious names → `df_mal` with:
   - `package_name`, `label = 1`
2. Load benign candidates → `df_ben` with:
   - `package_name`, `label = 0`
3. Concatenate `df_mal` and `df_ben`.
4. Drop duplicate `package_name` (malicious kept if overlap).
5. Shuffle rows and save as `labeled_packages.csv`.

Final dataset:
- Total packages: **24,925**
- Columns: `package_name`, `label` (1 = malicious, 0 = benign)
