# Metadata Feature Engineering

## 📌 Overview
This module focuses on transforming raw metadata (such as package names, descriptions, author details, and version strings) into quantitative features. By applying **Entropy Analysis** and **Heuristic Rules**, we convert unstructured text fields into numerical signals suitable for machine learning models (ETM/DTM).

This step is critical for distinguishing benign packages from malicious ones (e.g., Typosquatting) based on statistical anomalies rather than deep code inspection.

---   
## 📊 Data Distribution
Before processing, an initial check of the dataset balance was performed:
* **Benign Packages (0):** ~14k samples
* **Malicious Packages (1):** ~8k samples
* **Visualization:** A count plot is generated to verify the class ratio.

--- 
## 🛠 Feature Engineering Strategy

We engineered **21 distinct features** categorized into three groups:

### 1. Textual & Entropy Features (ETM Proxies)
These features analyze the randomness and structure of text fields to detect gibberish (DGA) or obfuscation.
* **Entropy:** calculated for `Name` and `Summary` (Shannon entropy). High entropy often indicates random names used by bots.
* **Lengths:** Character counts for `Name`, `Summary`, `Author`, and `Description`.
* **Typosquatting Indicators:** Counts of dots (`.`) and hyphens (`-`) in package names.
* **Web Indicators:** Count of URLs and presence of `<script>` tags in summaries.

### 2. Identity & Trust Features (DTM Proxies)
These features assess the legitimacy of the package maintainer.
* **Suspicious Email:** Flags missing emails or placeholder domains (e.g., `example.com`, `nan`).
* **Free Domain:** Checks if the author uses free email providers (Gmail, Proton) vs. corporate/institutional domains.
* **Missing Author:** Binary flag for empty author fields.

### 3. Complexity & Transparency
These features measure adherence to standard software development practices.
* **Version Depth:** Counts segments in version strings (e.g., `1.0.2` vs `1`).
* **Transparency:** Presence of a `Homepage` link and a valid `License`.
* **Classification:** Number of PyPI classifiers (tags) used.

--- 
## Quick Start

### Dependencies
Ensure you have the required Python libraries installed:
```bash
pip install pandas matplotlib seaborn regex
```

---
Running the Extraction
Run the feature engineering script to process your raw metadata CSV:
```Bash
python generate_metadata_features.py
```

📂 Output
The script generates a clean dataset ready for training:

File: `metadata_features_engineered_full.csv`

Columns: 21 numeric/binary feature columns + Label.

