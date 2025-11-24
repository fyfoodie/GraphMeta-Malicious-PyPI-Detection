
# Malicious Python Package Analysis

This repository contains the workflow, scripts, and environment configuration for analyzing malicious Python packages.

## 📋 Prerequisites

**System Requirements:**
* **Host:** Windows (with VirtualBox installed)
* **Guest:** Ubuntu Linux
* **Network:** Ability to toggle between NAT (Internet) and Host-only (Isolated) adapters.

**System Dependencies (Ubuntu):**
```bash
sudo apt update
sudo apt install python3-pip git build-essential dkms linux-headers-$(uname -r) bzip2 tar
```

Python Dependencies:

```Bash
pip install pandas numpy scikit-learn xgboost requests
```
---

# ⚙️ VM & Environment Setup

## 1. VirtualBox Guest Additions
To enable clipboard sharing and file transfers between Windows and Ubuntu:

  1. Insert Image: In VirtualBox menu, select `Devices -> Insert Guest Additions CD image`.
  2. Manual Install (if auto-run fails):

```Bash
sudo mkdir -p /mnt/cdrom
sudo mount /dev/cdrom /mnt/cdrom
cd /mnt/cdrom
sudo ./VBoxLinuxAdditions.run
sudo reboot
```

## 2. Shared Folder Configuration
Set up a bridge to transfer data between the Windows Host and Ubuntu Guest.

  1. Windows: Create a folder named `VM_Share`.
  2. VirtualBox Manager: Go to `Settings -> Shared Folders`.   
    - Path: Select your Windows `VM_Share` folder.   
    - Options: Check `[x] Auto-mount` and `[x] Make Permanent`.    

3. Ubuntu Permission: Grant access to the shared folder.

```Bash
sudo usermod -aG vboxsf $USER
# Log out and log back in for changes to take effect.
# Folder will appear at: /media/sf_VM_Share/
```

--- 

# 🚀 Workflow Checklist
Follow this sequence to replicate the data acquisition and analysis pipeline.

## Phase 1: Data Acquisition (Network: NAT/Enabled)
*Use temporary internet access to fetch datasets.*

   - [ ] Clone Malicious Registry:

```Bash
mkdir -p ~/malware_research/data
git clone [https://github.com/lxyeternal/pypi_malregistry.git](https://github.com/lxyeternal/pypi_malregistry.git) ~/malware_research/data/pypi_malregistry
```

   - [ ] Download Benign Packages: Run the download_benign.py script to safely download the top 200 PyPI packages (without installing them).

```Bash
python3 download_benign.py
```

## Phase 2: Analysis (Network: Disabled/Host-Only)
*Secure the environment before handling live malware samples.*

   - [ ] Import Dataset: Copy existing "Backstabber" packages or metadata from the Shared Folder to the local workspace.

```Bash
cp -r /media/sf_VM_Share/packages/* ~/malware_research/data/packages/
```

   - [ ] Run Feature Extraction: Execute the extraction script to analyze package structure and code.

```Bash
python3 extract_features.py
```

## Phase 3: Exfiltration
   - [ ] Export Results: Copy the generated CSV file back to Windows for merging and reporting.

```Bash
cp code_features.csv /media/sf_VM_Share/
```

--- 

📂 Project Structure
```Bash
malware_research/
├── data/
│   ├── packages/          # Directory containing .tar.gz/.whl files
│   └── pypi_malregistry/  # Cloned malicious registry
├── download_benign.py     # Script to fetch top PyPI packages
├── extract_features.py    # Main GMD feature extraction script
└── README.md              # This documentation
```
