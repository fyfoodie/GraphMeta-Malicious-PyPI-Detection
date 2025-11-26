
import os
import pandas as pd
import tarfile
import zipfile
import re
import csv

# --- CONFIGURATION ---
# Path to Benign Packages (Flat folder in Shared Drive)
BENIGN_DIR = "/media/sf_Vm_Share/benign_packages"

# Path to Malicious Packages (The Git Repo - We will search recursively here)
MALICIOUS_DIR = "/home/afiqahkh/malware_research/data/pypi_malregistry"

# Output file (Saved to Windows/Shared folder for safety)
OUTPUT_FILE = "/media/sf_Vm_Share/final_dataset_features.csv"

# Regex patterns for "Suspicious Features"
PATTERNS = {
    "suspicious_imports": re.compile(r'(import\s+(socket|subprocess|os|sys|shutil|requests|base64|cryptography))'),
    "shell_execution": re.compile(r'(os\.system|subprocess\.Popen|subprocess\.call|subprocess\.run)'),
    "network_activity": re.compile(r'(socket\.socket|urllib\.request|requests\.get|requests\.post)'),
    "encoding": re.compile(r'(base64\.b64decode|codecs\.decode)'),
    "file_access": re.compile(r'(open\(|file\()'),
    "eval_exec": re.compile(r'(eval\(|exec\()'),
    "ip_address": re.compile(r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}')
}

def analyze_content(content):
    """Scans a single file's text content for malicious patterns."""
    features = {k: 0 for k in PATTERNS.keys()}
    
    for key, pattern in PATTERNS.items():
        if pattern.search(content):
            features[key] = 1
            
    return features

def process_package(filepath, label):
    """Opens a package safely (without running it) and extracts features."""
    
    # Default features
    package_features = {k: 0 for k in PATTERNS.keys()}
    package_features['pkg_name'] = os.path.basename(filepath)
    package_features['label'] = label # 0 for benign, 1 for malicious
    package_features['file_count'] = 0
    package_features['total_size'] = os.path.getsize(filepath)
    
    try:
        # Handle Tar Files (.tar.gz)
        if filepath.endswith(('.tar.gz', '.tgz')):
            with tarfile.open(filepath, "r:gz") as tar:
                # Security: Only look at the first 50 files to avoid "Zip Bombs"
                members = tar.getmembers()[:50]
                package_features['file_count'] = len(members)
                
                for member in members:
                    if member.isfile() and member.name.endswith('.py'):
                        f = tar.extractfile(member)
                        if f:
                            content = f.read().decode('utf-8', errors='ignore')
                            # Merge features found in this file
                            file_feats = analyze_content(content)
                            for k in file_feats:
                                package_features[k] = max(package_features[k], file_feats[k])

        # Handle Zip Files (.zip, .whl)
        elif filepath.endswith(('.zip', '.whl')):
            with zipfile.ZipFile(filepath, 'r') as z:
                members = z.namelist()[:50]
                package_features['file_count'] = len(members)
                
                for member in members:
                    if member.endswith('.py'):
                        with z.open(member) as f:
                            content = f.read().decode('utf-8', errors='ignore')
                            file_feats = analyze_content(content)
                            for k in file_feats:
                                package_features[k] = max(package_features[k], file_feats[k])
                                
    except Exception as e:
        # If a file is corrupt/unreadable, we just skip it to keep going
        pass

    return package_features

# --- MAIN EXECUTION ---
print("🚀 Starting Safe Static Analysis...")

# Prepare CSV output
fieldnames = ['pkg_name', 'label', 'file_count', 'total_size'] + list(PATTERNS.keys())

# Open CSV in write mode
with open(OUTPUT_FILE, 'w', newline='') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    
    # 1. Process Benign (Flat Directory)
    if os.path.exists(BENIGN_DIR):
        print(f"Scanning Benign Folder: {BENIGN_DIR}")
        benign_files = [f for f in os.listdir(BENIGN_DIR) if f.endswith(('.tar.gz', '.tgz', '.zip', '.whl'))]
        total = len(benign_files)
        
        for i, filename in enumerate(benign_files):
            if i % 500 == 0: print(f"  Processed {i}/{total} benign packages...")
            
            path = os.path.join(BENIGN_DIR, filename)
            feats = process_package(path, label=0) # Label 0 = Benign
            writer.writerow(feats)
            
    # 2. Process Malicious (Recursive Search in Git Repo)
    if os.path.exists(MALICIOUS_DIR):
        print(f"Scanning Malicious Repo: {MALICIOUS_DIR}")
        
        mal_count = 0
        # os.walk allows us to look inside all the date/name subfolders
        for root, dirs, files in os.walk(MALICIOUS_DIR):
            for filename in files:
                if filename.endswith(('.tar.gz', '.tgz', '.zip', '.whl')):
                    path = os.path.join(root, filename)
                    feats = process_package(path, label=1) # Label 1 = Malicious
                    writer.writerow(feats)
                    mal_count += 1
                    
                    if mal_count % 100 == 0: print(f"  Processed {mal_count} malicious packages...")

print(f"✅ Done! Features saved to {OUTPUT_FILE}")