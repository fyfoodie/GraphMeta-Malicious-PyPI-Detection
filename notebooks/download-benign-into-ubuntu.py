
import pandas as pd
import subprocess
import os
import sys
import concurrent.futures
import time

# --- CONFIGURATION ---
CSV_PATH = "/media/sf_VM_Share/benign_metadata.csv"
HOME_DIR = os.path.expanduser("~") 
SAVE_DIR = os.path.join(HOME_DIR, "malware_research/data/benign")
LOG_FILE = os.path.join(HOME_DIR, "malware_research/data/success_log.txt")
FAILURE_FILE = os.path.join(HOME_DIR, "malware_research/data/failed_log.csv")

MAX_WORKERS = 10 
TIMEOUT_SECONDS = 100

os.makedirs(SAVE_DIR, exist_ok=True)

# --- 1. SETUP LOGS ---
if not os.path.exists(FAILURE_FILE):
    with open(FAILURE_FILE, "w") as f:
        f.write("Package,Reason\n")

downloaded_packages = set()
if os.path.exists(LOG_FILE):
    with open(LOG_FILE, "r") as f:
        downloaded_packages = set(line.strip() for line in f)

print(f"🔄 Resuming... Found {len(downloaded_packages)} already downloaded.")

# --- 2. LOAD CSV ---
print(f"📖 Reading CSV from {CSV_PATH}...")
try:
    df = pd.read_csv(CSV_PATH)
except FileNotFoundError:
    print(f"❌ Error: Could not find '{CSV_PATH}'")
    sys.exit(1)

all_packages = df['Name'].unique().tolist()
remaining_packages = [p for p in all_packages if p not in downloaded_packages]

print(f"📊 Total packages: {len(all_packages)}")
print(f"⏭️  Skipping: {len(downloaded_packages)}")
print(f"📥 Remaining to download: {len(remaining_packages)}")
print("-" * 40)

# --- 3. INTELLIGENT DOWNLOAD FUNCTION ---
def download_package(pkg):
    # ATTEMPT 1: PREFER SOURCE CODE (--no-binary :all:)
    try:
        subprocess.run(
            ["pip", "download", pkg, "--no-binary", ":all:", "--no-deps", "--dest", SAVE_DIR],
            check=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            timeout=TIMEOUT_SECONDS
        )
        with open(LOG_FILE, "a") as log:
            log.write(f"{pkg}\n")
        return (pkg, "SUCCESS_SOURCE") # We got the best version!
        
    except subprocess.TimeoutExpired:
        return (pkg, "TIMEOUT")
    
    except subprocess.CalledProcessError:
        # ATTEMPT 2: FALLBACK TO BINARY (Allow Wheels)
        # If strict mode failed, maybe the package only exists as a .whl?
        try:
            subprocess.run(
                ["pip", "download", pkg, "--no-deps", "--dest", SAVE_DIR], # Flag removed here
                check=True,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                timeout=TIMEOUT_SECONDS
            )
            with open(LOG_FILE, "a") as log:
                log.write(f"{pkg}\n")
            return (pkg, "SUCCESS_WHEEL") # We got the fallback version
            
        except subprocess.CalledProcessError:
            return (pkg, "NOT_FOUND") # Truly gone
        except Exception as e:
            return (pkg, f"ERROR: {str(e)}")

# --- 4. PARALLEL EXECUTION ---
if not remaining_packages:
    print("✅ All packages already downloaded!")
    sys.exit(0)

print(f"🚀 Starting download with {MAX_WORKERS} threads...")

with concurrent.futures.ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
    future_to_pkg = {executor.submit(download_package, pkg): pkg for pkg in remaining_packages}
    
    for future in concurrent.futures.as_completed(future_to_pkg):
        pkg = future_to_pkg[future]
        try:
            pkg_name, status = future.result()
            
            if "SUCCESS" in status:
                # Print cleaner output distinguishing Source vs Wheel
                if status == "SUCCESS_SOURCE":
                    print(f"✅ {pkg_name}")
                else:
                    print(f"🆗 {pkg_name} (Wheel only)")
            else:
                # HANDLE ERRORS
                if status == "TIMEOUT":
                    print(f"⏳ {pkg_name} (Skipped - Timeout)")
                elif status == "NOT_FOUND":
                    print(f"🚫 {pkg_name} (Deleted from PyPI)")
                else:
                    print(f"⚠️  {pkg_name} ({status})")
                
                with open(FAILURE_FILE, "a") as fail_log:
                    fail_log.write(f"{pkg_name},{status}\n")
                
        except Exception as exc:
            print(f"💥 Critical Error on {pkg}: {exc}")

print("-" * 40)
print("🏁 Batch finished.")
print(f"Files saved in: {SAVE_DIR}")
print(f"Failures logged in: {FAILURE_FILE}")