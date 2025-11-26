import pandas as pd
import subprocess
import os
import sys
import concurrent.futures
import shutil

# --- CONFIGURATION ---
SHARED_FOLDER = "/media/sf_Vm_Share"

CSV_PATH = os.path.join(SHARED_FOLDER, "benign_metadata.csv")
SAVE_DIR = os.path.join(SHARED_FOLDER, "benign_packages")
TEMP_DIR = os.path.join(SHARED_FOLDER, "pip_temp_workspace") 
LOG_FILE = os.path.join(SHARED_FOLDER, "success_log.txt")     
FAILURE_FILE = os.path.join(SHARED_FOLDER, "failed_log.csv")  

MAX_WORKERS = 8 
TIMEOUT_SECONDS = 180 

# --- FORCE PIP TO USE WINDOWS TEMP ---
os.environ["TMPDIR"] = TEMP_DIR
os.environ["TEMP"] = TEMP_DIR
os.environ["TMP"] = TEMP_DIR

os.makedirs(SAVE_DIR, exist_ok=True)
os.makedirs(TEMP_DIR, exist_ok=True)

# --- SETUP LOGS ---
if not os.path.exists(FAILURE_FILE):
    with open(FAILURE_FILE, "w") as f:
        f.write("Package,Reason\n")

downloaded_packages = set()
if os.path.exists(LOG_FILE):
    with open(LOG_FILE, "r") as f:
        downloaded_packages = set(line.strip() for line in f)

print(f"🔄 Resuming... Found {len(downloaded_packages)} successful downloads.")
print(f"📂 Saving to: {SAVE_DIR}")

# --- LOAD CSV ---
try:
    df = pd.read_csv(CSV_PATH)
except FileNotFoundError:
    print(f"❌ Error: Could not find '{CSV_PATH}'")
    sys.exit(1)

all_packages = df['Name'].unique().tolist()
remaining_packages = [p for p in all_packages if p not in downloaded_packages]

print(f"📊 Total packages: {len(all_packages)}")
print(f"⏭️  Skipping: {len(downloaded_packages)}")
print(f"📥 Remaining: {len(remaining_packages)}")
print("-" * 40)

# --- SMART DOWNLOAD FUNCTION (With Dot-Swap) ---
def download_package(pkg_original):
    
    # GENERATE CANDIDATE NAMES
    candidates = [pkg_original]
    
    # 1. Try swapping dashes to dots (Fixes autogluon-tabular -> autogluon.tabular)
    if '-' in pkg_original:
        candidates.append(pkg_original.replace('-', '.'))
        
    # 2. Try swapping dashes to underscores (Fixes some old pkgs)
    if '-' in pkg_original:
        candidates.append(pkg_original.replace('-', '_'))
        
    # Remove duplicates while keeping order
    candidates = list(dict.fromkeys(candidates))

    last_error = ""

    # Try every name variation
    for pkg_name in candidates:
        
        # DEFINE DOWNLOAD METHODS (Source -> Wheel -> Generic)
        attempts = [
            (["pip", "download", pkg_name, "--no-binary", ":all:", "--no-deps", "--no-cache-dir", "--dest", SAVE_DIR], "SUCCESS_SOURCE"),
            (["pip", "download", pkg_name, "--only-binary", ":all:", "--no-deps", "--no-cache-dir", "--dest", SAVE_DIR], "SUCCESS_WHEEL"),
            (["pip", "download", pkg_name, "--no-deps", "--no-cache-dir", "--dest", SAVE_DIR], "SUCCESS_GENERIC")
        ]

        for cmd, success_status in attempts:
            try:
                subprocess.run(
                    cmd, 
                    check=True, 
                    stdout=subprocess.DEVNULL, 
                    stderr=subprocess.DEVNULL, 
                    timeout=TIMEOUT_SECONDS 
                )
                
                # Log success (We log the ORIGINAL name so we don't retry it)
                with open(LOG_FILE, "a") as log:
                    log.write(f"{pkg_original}\n")
                
                return (pkg_original, success_status + f" ({pkg_name})")
                
            except subprocess.TimeoutExpired:
                last_error = "TIMEOUT"
                continue
            except subprocess.CalledProcessError:
                last_error = "NOT_FOUND"
                continue
            except Exception as e:
                last_error = f"ERROR: {str(e)}"
                break 
        
        # If we succeeded with this candidate name, stop trying others!
        if "SUCCESS" in last_error: 
            break

    return (pkg_original, last_error)

# --- EXECUTION ---
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
                if "SOURCE" in status:
                    print(f"✅ {status}")
                elif "WHEEL" in status:
                    print(f"🆗 {status}")
                else:
                    print(f"👍 {status}")
            else:
                # Error Handling
                if status == "TIMEOUT":
                    print(f"⏳ {pkg_name} (Timeout)")
                elif status == "NOT_FOUND":
                    print(f"🚫 {pkg_name} (Not on PyPI)")
                else:
                    print(f"⚠️  {pkg_name} ({status})")
                    
                with open(FAILURE_FILE, "a") as fail_log:
                    fail_log.write(f"{pkg_name},{status}\n")
                
        except Exception as exc:
            print(f"💥 Critical Error on {pkg}: {exc}")

print("-" * 40)
print("🏁 Batch finished.")
try:
    shutil.rmtree(TEMP_DIR)
except:
    pass