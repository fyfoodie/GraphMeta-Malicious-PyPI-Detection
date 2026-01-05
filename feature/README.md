## Phase 5: Structural Integrity & Complexity Assessment

This module implements **Section 4.6** of the thesis. It validates the physical viability of downloaded software archives and extracts topological graph metrics to test the "Complexity Hypothesis" (benign modularity vs. malicious minimalism).

### 📋 4.6.1 Structural Integrity Assessment (Pre-Analysis)
**Objective:** validate that source code artifacts (`.tar.gz`, `.whl`, `.zip`) are uncorrupted and parseable before attempting graph construction. This step filters out "junk" data to ensure the GraphMeta-Detect (GMD) model receives only valid inputs.

**Methodology:**
* **Multimodal Parsing:** Recursively handles nested directories and multiple archive formats.
* **AST Validation:** Uses Python’s `ast` module to verify syntax and ensure files can be modeled as directed graphs.
* **Integrity Filtering:** Categorizes packages into `VALID` (parseable), `EMPTY` (no code), or `CORRUPT`.

**Usage:**
```
# 1. Activate Virtual Environment
source venv/bin/activate

# 2. Run the Integrity Scan
python3 parsing_check.py
```

# Output: parsing_integrity_report.csv

---

🕸️4.6.2 Structural Complexity Assessment

Objective: transform valid source code into Function Call Graphs (FCG) to quantify topological complexity.   
Key Metrics Extracted:Node Count ($|V|$): Total functional units (functions/classes).
Edge Count ($|E|$): Total invocation relationships (calls).
Graph Density: A measure of code linearity.

Research Findings (N=23,842):
Benign Packages: High complexity (Mean Nodes: ~513).
Malicious Packages: Low complexity "Micro-Graphs" (Mean Nodes: ~42).

Usage:
```
# Run the Graph Extraction (Supports recursive malicious path mapping)
python3 fix_malicious_paths.py

# Output: graph_complexity_metrics.csv
```

📊 VisualizationTo visualize the "Complexity Gap" between benign and malicious clusters, use the generated CSV with the analysis notebooks provided in "/notebooks".
---
