import os
import shutil
import zipfile

src_dir = "dist/HarvestMoonBTN_PC_Release"
staging_dir = "dist/staging_clean"
zip_path = "dist/HarvestMoonBTN_PC_Port_v1.0.0_CleanRelease.zip"

if os.path.exists(staging_dir):
    shutil.rmtree(staging_dir)

os.makedirs(staging_dir, exist_ok=True)

# Copy directories and files with clean-room exclusions
exclude_files = {
    "card1.mcd", "card2.mcd", "overlay_captures.json.d",
    "stdout.txt", "stderr.txt", "psx_last_run_report.json",
    "psx_freeze_heartbeat.json"
}

for root, dirs, files in os.walk(src_dir):
    rel_root = os.path.relpath(root, src_dir)
    if rel_root == ".":
        target_root = staging_dir
    else:
        target_root = os.path.join(staging_dir, rel_root)
        os.makedirs(target_root, exist_ok=True)

    # Exclude certain directories from traversal
    dirs[:] = [d for d in dirs if d not in {"cache", "overlay_captures.json.d"}]

    for f in files:
        if f in exclude_files:
            continue
        if f.startswith("psx_freeze_") or f.endswith(".tmp"):
            continue
        # Exclude copyrighted disc files in game directory
        if rel_root == "game" and (f.endswith(".bin") or f.endswith(".cue") or f.endswith(".chd") or f.endswith(".iso")):
            continue

        src_file = os.path.join(root, f)
        dst_file = os.path.join(target_root, f)
        shutil.copy2(src_file, dst_file)

print(f"Staging prepared at: {staging_dir}")

# Create Zip Archive
if os.path.exists(zip_path):
    os.remove(zip_path)

with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zipf:
    for root, dirs, files in os.walk(staging_dir):
        for f in files:
            full_path = os.path.join(root, f)
            arcname = os.path.relpath(full_path, staging_dir)
            zipf.write(full_path, arcname)

size_mb = os.path.getsize(zip_path) / (1024 * 1024)
print(f"Zip created successfully: {zip_path} ({size_mb:.2f} MB)")

# Verify contents
with zipfile.ZipFile(zip_path, "r") as zipf:
    print(f"Total files in zip: {len(zipf.namelist())}")
    for item in sorted(zipf.namelist()):
        print(f"  {item}")

# Cleanup staging
shutil.rmtree(staging_dir)
print("Staging cleaned up.")

