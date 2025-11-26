# Graph-Based Feature Extraction (Static Analysis)  

## Overview   
[cite_start]This module implements a structural static analysis approach inspired by **MALGUARD (Gao et al., 2025)**[cite: 4, 14]. [cite_start]Instead of simple keyword counting, this script constructs an **Function Call Graph (FCG)** [cite: 146] for each Python package to analyze the *centrality* and *influence* of dangerous APIs.   

---
## 📋 Prerequisites  
To run the graph extraction algorithms, the following Python libraries are required.   

**Install via pip:**  
```bash  
pip install networkx pandas numpy   
```  
---   

## Methodology

### 1. Abstract Syntax Tree (AST) Parsing
We utilize Python's `ast` module to parse the source code of `.py` files (extracted from `.tar.gz`, `.zip`, or `.whl` archives) into a tree structure. [cite_start]This allows us to understand the code's execution flow without running it[cite: 98, 175].

### 2. Graph Construction   
For each package, we build a **Directed Graph ($G = (V, E)$)**:  
* **Nodes ($V$):** Represent functions, modules, and API calls (e.g., `main()`, `subprocess.Popen`).   
* [cite_start]**Edges ($E$):** Represent invocation relationships (e.g., `main()` $\to$ calls $\to$ `subprocess.Popen`)[cite: 147].  

### 3. Centrality Metrics Extraction   
[cite_start]To detect malware, we measure the topological importance of specific "Sensitive APIs" (execution, network, obfuscation) using four graph centrality metrics proposed in the MALGUARD framework[cite: 193]:

1.  [cite_start]**Degree Centrality:** Measures the immediate connectivity of an API (how many functions directly call it?)[cite: 198].   
    $$C_D(v) = \frac{deg(v)}{N-1}$$
       
2.  [cite_start]**Closeness Centrality:** Measures how "close" an API is to all other nodes (efficiency of information spread)[cite: 195].   
    $$C_C(v) = \frac{N-1}{\sum_{u \neq v} d(v, u)}$$
      
3.  [cite_start]**Harmonic Centrality:** A variation of closeness that handles disconnected graphs (common in Python scripts)[cite: 226].   
4.  [cite_start]**Katz Centrality:** Measures influence by considering neighbors and "neighbors of neighbors" (global influence)[cite: 223].   

---  
## Targeted Sensitive APIs
We calculate the metrics above for high-risk API categories including:
* **Execution:** `subprocess`, `os.system`, `exec`, `eval`   
* **Network:** `socket`, `requests`, `urllib`   
* **Obfuscation:** `base64.b64decode`, `codecs.decode`   
* **Evasion:** `os.getenv`, `os.environ`   

## Usage
Run the extraction script from the project root:   

```bash   
python3 src/analysis/extract_graph_features.py
```   

Output Columns:   

- `pkg_name`: Unique identifier.  
- `label`: 0 (Benign) or 1 (Malicious).   
- `num_nodes`, `num_edges`: Graph structural metadata.   
- `[API]_degree`, `[API]_closeness`, ... : Calculated metrics for each sensitive API.    