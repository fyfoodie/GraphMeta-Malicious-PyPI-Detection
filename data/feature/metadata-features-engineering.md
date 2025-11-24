# 🛠️ Feature Engineering
 
**Input Data:** `full_metadata_merged_clean_final.csv`  
**Output Data:** `metadata_features_engineered_full.csv`

## 📋 Overview
This module implements a robust feature engineering pipeline designed to differentiate between legitimate and malicious Python packages based on PyPI metadata. 

Following the methodology proposed by **Halder et al.**, features are categorized into two distinct classes:
1.  **ETM (Easy-To-Manipulate):** Lexical and textual features that attackers can easily randomize or generate (e.g., name randomness, description length).
2.  **DTM (Difficult-To-Manipulate):** Features representing project maturity, identity, and effort, which are costly for attackers to fake at scale (e.g., versioning history, valid corporate emails).

---

## 📊 Feature Set Dictionary

### 1. ETM Features (Textual & Lexical)
*Captures the "look and feel" of the package. High entropy or gibberish often indicates automated malware generation.*

| Feature Name | Type | Description & Rationale |
| :--- | :--- | :--- |
| **Name_Entropy** | `Float` | Shannon entropy of the package name. Detects random strings (e.g., `x8z9q`) vs. semantic names (e.g., `requests`). |
| **Name_Length** | `Int` | Length of the package name. Used to detect unusually short/long generated names. |
| **Name_Dots / Hyphens** | `Int` | Structural analysis to detect typosquatting attempts (e.g., `request-lib` vs `requests`). |
| **Summary_Entropy** | `Float` | Measures randomness in the summary text. High entropy indicates obfuscation or gibberish. |
| **Summary_Has_Script** | `Binary` | Flags the presence of HTML `<script>` or `javascript:` tags in the summary (XSS vectors). |
| **Desc_Length** | `Int` | Length of the full description. Malware often has zero or near-zero description length. |

### 2. DTM Features (Identity & Complexity)
*Captures the author's effort and identity. These proxy for "trustworthiness."*

| Feature Name | Type | Description & Rationale |
| :--- | :--- | :--- |
| **Suspicious_Email** | `Binary` | Flags missing emails (`NaN`) or placeholders (e.g., `example.com`, `me.com`). |
| **Free_Email_Domain** | `Binary` | Checks if the author uses free providers (Gmail, ProtonMail) vs. verifiable corporate/university domains. |
| **Num_Classifiers** | `Int` | Count of PyPI classifiers (OS, License, Audience). Legitimate projects usually invest time tagging these; malware often has 0. |
| **Version_Depth** | `Int` | Counts dots in version string (e.g., `1.0.2`). Proxies adherence to Semantic Versioning. |
| **Has_Homepage** | `Binary` | Checks for the existence of a project homepage/repository link. |
| **Has_License** | `Binary` | Checks if a license is declared, a standard for legitimate open-source software. |

---

Dependencies  
`pandas`   
`numpy`   

Code Logic Snippet (Entropy Calculation)
The core logic for detecting randomness uses Shannon Entropy:

Python

```
def calc_entropy(text):
    """Calculates Shannon entropy to detect randomness/gibberish."""
    if pd.isna(text) or text == "":
        return 0
    text = str(text)
    prob = [freq / len(text) for freq in Counter(text).values()]
    return -sum(p * math.log(p, 2) for p in prob)
```
---
## 🚀 Usage

To generate the engineered dataset, ensure `full_metadata_merged_clean_final.csv` is in the root directory and run the script:

```bash
python feature_engineering_metadata.py
