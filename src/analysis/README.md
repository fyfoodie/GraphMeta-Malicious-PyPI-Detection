### 🛠️ Feature Extraction (Static Analysis)

Script: `extract_features.py` Purpose: To safely extract behavioral indicators from Python packages (source archives) without executing them.   

Methodology: This script iterates through both benign and malicious datasets (archives like `.tar.gz`, `.zip`, `.whl`) and performs keyword-based static analysis on the contained .py files. It generates a CSV dataset (`final_dataset_features.csv`) suitable for machine learning.    

---   
Extracted Features:    

- Metadata: Package Name, Total Size, File Count.   
- Suspicious APIs: Usage of `socket`, `subprocess`, `requests` (Network/System interaction).  
- Execution Hazards: Counts of `exec()`, `eval()`, `os.system()` (Arbitrary code execution).   
- Obfuscation: Detection of `base64` decoding (often used to hide payloads).   
- Network Indicators: Presence of hardcoded IP addresses.   
