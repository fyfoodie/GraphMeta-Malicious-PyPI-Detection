# Data Acquisition: Malicious PyPI Packages

Goal of this phase:

- Build a unified, deduplicated list of malicious PyPI package names.
- Final output: `master_malicious_pypi_list.txt` (one package name per line).

---

## 1. MALOSS (`pypi-mal-pkgs.txt`)

Source:

- GitHub repo: **`osssanitizer/maloss`**
- File in repo: `malware/pypi-mal-pkgs.txt`

Steps:

1. Open the MALOSS GitHub repo in a browser.
2. Navigate to `malware/pypi-mal-pkgs.txt`.
3. Click **Raw** → **Save As…**.
4. Save the file as `pypi-mal-pkgs.txt` in your data folder.

Output file:

- `pypi-mal-pkgs.txt` — malicious PyPI package names (one per line).

---

## 2. MalRegistry (`malregistry_pypi_names.txt`)

Goal:

- Extract all **top-level directory names** (each directory name = one malicious package).

Script name:

- `fetch_malregistry_names.py`

Core logic (summary):

- Call GitHub API for the `lxyeternal/pypi_malregistry` tree.
- Keep entries where:
  - `type == "tree"`
  - `path` contains **no `/`** (top-level only).
- Drop `.github`.
- Deduplicate and sort package names.
- Write one name per line to `malregistry_pypi_names.txt`.

Output file:

- `malregistry_pypi_names.txt` — MalRegistry malicious PyPI package names.

---

## 3. Backstabber’s Knife Collection (`bkc_pypi_names.txt`)

Input:

- `backstabber-package_index.jsonl` (provided by the Backstabber dataset)

Script name:

- `extract_bkc_names.py`

Core logic (summary):

- For each JSON line:
  - Parse into `obj`.
  - Read `purl = obj["purl"]["value"]`.
  - Keep only if `purl` starts with `pkg:pypi/`.
  - Extract `<name>` between `pkg:pypi/` and `@`.
  - Normalize: `lower()` + `strip()`.
- Deduplicate and sort names.
- Write one name per line to `bkc_pypi_names.txt`.

Output file:

- `bkc_pypi_names.txt` — Backstabber malicious PyPI package names.

---

## 4. QUT-DV25 (`qutdv25_pypi_names.txt`)

Input:

- Excel file: `MaliciousPackageNameAndVersion.xlsx`  
  (columns: `Malicious Package Name`, `Malicious Package Version`)

Script name:

- `extract_qut_excel.py`

Core logic (summary):

1. Read the Excel file with pandas.
2. Use the first column as the package name.
3. Normalize each name:
   - lowercase
   - strip spaces
4. Filter to PyPI-style names:
   - Reject if name contains `/`, `@`, `:`, or spaces.
   - Enforce regex: `^[a-z0-9\-\._]+$`.
5. Deduplicate, sort, write one name per line to `qutdv25_pypi_names.txt`.

Output file:

- `qutdv25_pypi_names.txt` — QUT-DV25 malicious PyPI package names.

---

## 5. Threat-Intel DOCX (`threatreport_pypi_names.txt`)

Input:

- DOCX file:  
  `Malicious PyPI Packages (2023–2025) in Threat Intelligence Reports.docx`  
  (manually curated from Sonatype, JFrog, Checkmarx, ReversingLabs, etc.)

Script name:

- `extract_threatreport_names.py`

Core logic (summary):

1. Treat the DOCX as a ZIP archive.
2. Read `word/document.xml` inside the archive.
3. Parse XML and collect all text nodes.
4. For each text chunk:
   - lowercase + strip
   - reject if it has spaces
   - reject if non-ASCII
   - enforce regex: `^[a-z0-9\-\._]+$`
5. Deduplicate and sort.
6. Write one name per line to `threatreport_pypi_names.txt`.

Output file:

- `threatreport_pypi_names.txt` — threat-intel malicious PyPI package names.

---

## 6. Merge All Sources (`master_malicious_pypi_list.txt`)

Input files:

- `pypi-mal-pkgs.txt`
- `malregistry_pypi_names.txt`
- `bkc_pypi_names.txt`
- `qutdv25_pypi_names.txt`
- `threatreport_pypi_names.txt`

Script name:

- `merge_all_malicious.py`

Final output:

- `master_malicious_pypi_list.txt` — final malicious PyPI list used for:
  - benign selection
  - metadata extraction
  - call-graph analysis
  - model training
