## Phase 5: Structural Integrity & Complexity Assessment

This module implements Section 4.6 of the thesis. It validates the physical viability of packages archives and extracts increasingly granular topological graph metrics to test the "Complexity Hypothesis" (benign modularity vs. malicious minimalism).

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

#Output: parsing_integrity_report.csv
```

## 4.6.2 Structural Complexity Assessment


Objective: transform valid source code into Function Call Graphs (FCG) to quantify topological complexity.   
- Key Metrics Extracted:Node Count ($|V|$): Total functional units (functions/classes).
- Edge Count ($|E|$): Total invocation relationships (calls).
- Graph Density: A measure of code linearity.


Research Findings (N=23,842):   
- Benign Packages: High complexity (Mean Nodes: ~513).   
- Malicious Packages: Low complexity "Micro-Graphs" (Mean Nodes: ~42).   

Usage:
```
# Run the Graph Extraction (Supports recursive malicious path mapping)
python3 fix_malicious_paths.py

# Output: graph_complexity_metrics.csv
```
---
## 4.6.3 Topological Intent Analysis (Advanced Feature Extraction)   
Objective: Go beyond simple node counts to analyze the shape and intent of the code structure. This module applies advanced graph theory to distinguish between the "flat" linear execution of malware and the "clustered" modular design of benign engineering.   

Methodology (The 3 Layers):   
- Macroscopic (Shape): Calculates Global Efficiency to detect if the code acts like a simple linear script (Malicious) or a complex library (Benign).   
- Mesoscopic (Modularity): Uses Clustering Coefficients to measure how well the code is organized into logical modules and communities.
- Microscopic (Risk Intent): Maps specific "Risk APIs" (e.g., `exec`, `socket`, `obfuscation`) and calculates their Centrality and Attack Distance (hops from entry point).   

Usage:
```
# Run the Advanced Topology Extractor
# (Requires input from 4.6.2)
python3 run_topology_analysis.py

# Output: graph_advanced_topology.csv
```

📊 VisualizationTo visualize the "Complexity Gap" between benign and malicious clusters, use the generated CSV with the analysis notebooks provided in "/notebooks".

