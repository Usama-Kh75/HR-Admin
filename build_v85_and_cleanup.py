import os
import shutil
import glob
import re

workspace_dir = r"e:\Antigravity projects\HR Admin"
desktop_dir = r"C:\Users\asalz\OneDrive\Desktop"

# 1. Update index.html to v8.5 Enterprise Cloud Edition
index_path = os.path.join(workspace_dir, "index.html")
with open(index_path, "r", encoding="utf-8") as f:
    code = f.read()

# Replace version occurrences
code = code.replace("v8.0 Cloud Edition", "v8.5 Enterprise Cloud Edition")
code = code.replace("الإصدار v8.0 Cloud Edition", "الإصدار v8.5 Enterprise Cloud Edition")
code = code.replace("الإصدار v8.0", "الإصدار v8.5 Enterprise")
code = code.replace("v8.0 Cloud", "v8.5 Enterprise")
code = code.replace("v8.0", "v8.5")

with open(index_path, "w", encoding="utf-8") as f:
    f.write(code)

print("✓ Updated index.html to v8.5 Enterprise Cloud Edition")

# 2. Generate v8.5 builds
cloud_file = os.path.join(workspace_dir, "نظام_ادارة_الملاك_v8.5_cloud.html")
with open(cloud_file, "w", encoding="utf-8") as f:
    f.write(code)

# Strict offline standalone version
offline_code = code.replace("<title>نظام إدارة الملاك - الإصدار v8.5 Enterprise Cloud Edition ☁️</title>", "<title>نظام إدارة الملاك - الإصدار v8.5 Standalone (أوفلاين محلي مستقل) 💾</title>")
offline_code = offline_code.replace('const FIREBASE_DB_URL = "https://hr-cooling-default-rtdb.firebaseio.com/system_bundle.json";', 'const FIREBASE_DB_URL = "";')
offline_code = offline_code.replace('const FIREBASE_BACKUPS_URL = "https://hr-cooling-default-rtdb.firebaseio.com/backups_history";', 'const FIREBASE_BACKUPS_URL = "";')
offline_code = offline_code.replace('const FIREBASE_SESSIONS_URL = "https://hr-cooling-default-rtdb.firebaseio.com/active_sessions";', 'const FIREBASE_SESSIONS_URL = "";')

offline_badge_old = '{cloudSyncStatus && cloudSyncStatus.connected ? ('
offline_badge_new = '{false ? ('
offline_code = offline_code.replace(offline_badge_old, offline_badge_new, 1)

offline_file = os.path.join(workspace_dir, "نظام_ادارة_الملاك_v8.5_offline.html")
with open(offline_file, "w", encoding="utf-8") as f:
    f.write(offline_code)

print("✓ Generated v8.5 Master Suite files in workspace")

# 3. Archive old versions on Desktop
if os.path.exists(desktop_dir):
    desktop_archive_dir = os.path.join(desktop_dir, "الأرشيف_القديم_v8.0_وما_قبلها")
    os.makedirs(desktop_archive_dir, exist_ok=True)
    
    old_desktop_patterns = [
        "نظام_ادارة_الملاك_v8.0*.html",
        "نظام_ادراة_الملاك_v*.html",
        "index.html"
    ]
    for pattern in old_desktop_patterns:
        for fpath in glob.glob(os.path.join(desktop_dir, pattern)):
            fname = os.path.basename(fpath)
            dest = os.path.join(desktop_archive_dir, fname)
            try:
                if os.path.exists(dest):
                    os.remove(dest)
                shutil.move(fpath, dest)
                print(f"  📦 Archived desktop file: {fname}")
            except Exception as e:
                print(f"  ⚠️ Could not archive {fname}: {e}")

    # Copy new v8.5 official files to Desktop
    try:
        shutil.copy2(cloud_file, os.path.join(desktop_dir, "نظام_ادارة_الملاك_v8.5_سحابي_رسمي.html"))
        shutil.copy2(offline_file, os.path.join(desktop_dir, "نظام_ادارة_الملاك_v8.5_أوفلاين_محلي_مستقل.html"))
        print("✓ Placed official v8.5 files on Desktop cleanly!")
    except Exception as e:
        print("  ⚠️ Error copying to desktop:", e)

# 4. Clean up workspace root
workspace_archive = os.path.join(workspace_dir, "الارشيف_القديم_v7.0_v7.5")
os.makedirs(workspace_archive, exist_ok=True)

old_workspace_patterns = [
    "نظام_ادراة_الملاك_v6*.html",
    "نظام_ادراة_الملاك_v7*.html",
    "نظام_ادارة_الملاك_v8.0*.html",
    "build_v75*.py",
    "build_v8_suite.py"
]

for pattern in old_workspace_patterns:
    for fpath in glob.glob(os.path.join(workspace_dir, pattern)):
        fname = os.path.basename(fpath)
        dest = os.path.join(workspace_archive, fname)
        try:
            if os.path.exists(dest):
                os.remove(dest)
            shutil.move(fpath, dest)
            print(f"  📦 Archived workspace file: {fname}")
        except Exception as e:
            pass

print("All cleanup and upgrade tasks completed successfully!")
