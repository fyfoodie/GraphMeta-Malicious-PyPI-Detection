Section 4.6.1: Structural Integrity Assessment   
Objective This stage validates the physical viability of software archives before graph construction. It filters out "junk" data to ensure the GraphMeta-Detect (GMD) model only learns from functional code.

---
Core Methodology

Multimodal Archive Support: Automatically processes .tar.gz, .whl, and .zip artifacts.

AST Validation: Uses Python’s ast module to verify syntax and ensure files can be modeled as directed graphs.

Integrity Filtering: Categorizes packages into VALID, EMPTY, or CORRUPT.

Key Integrity Metrics


- Parsing Success Rate: Percentage of packages successfully converted to Abstract Syntax Trees.
- SLOC Count: Total Source Lines of Code per package to measure implementation complexity.
- Structural Validity: Confirmation of at least one executable .py entry point.

```
# Ensure your virtual environment is active
source venv/bin/activate

# Execute the integrity scan
python3 parsing_check.py
```
