import os
import shutil

desktop_dir = r"C:\Users\asalz\OneDrive\Desktop"
archive_dir = r"e:\Antigravity projects\HR Admin\الارشيف_القديم_v7.0_v7.5"
os.makedirs(archive_dir, exist_ok=True)

# Files to remove/archive from Desktop
obsolete_files = [
    "نظام_ادراة_الملاك_v7.0.html",
    "نظام_ادراة_الملاك_v7.0_online.html",
    "نظام_ادراة_الملاك_v7.5_cloud.html",
    "نظام_ادارة_الملاك_v8.0_cloud.html",
    "نظام_ادارة_الملاك_v8.0_online.html",
    "تشغيل_السيرفر_المحلي - Shortcut.lnk",
    "data",
    "data.json"
]

for filename in obsolete_files:
    src_path = os.path.join(desktop_dir, filename)
    if os.path.exists(src_path):
        dest_path = os.path.join(archive_dir, filename)
        try:
            shutil.move(src_path, dest_path)
            print(f"✓ Archived: {filename}")
        except Exception as e:
            try:
                os.remove(src_path)
                print(f"✓ Removed from Desktop: {filename}")
            except Exception as ex:
                print(f"Error handling {filename}: {ex}")

# Rename offline version on desktop to crystal clear Arabic name
old_offline_name = os.path.join(desktop_dir, "نظام_ادارة_الملاك_v8.0_offline.html")
new_offline_name = os.path.join(desktop_dir, "نظام_ادارة_الملاك_v8.0_أوفلاين_محلي.html")

if os.path.exists(old_offline_name):
    if os.path.exists(new_offline_name):
        os.remove(new_offline_name)
    os.rename(old_offline_name, new_offline_name)
    print("✓ Renamed offline file to: نظام_ادارة_الملاك_v8.0_أوفلاين_محلي.html")

# Create a direct shortcut to the live cloud URL on Desktop
url_shortcut_path = os.path.join(desktop_dir, "رابط_النظام_السحابي_أونلاين.url")
url_content = """[InternetShortcut]
URL=https://usama-kh75.github.io/HR-Admin/
IconIndex=0
"""
with open(url_shortcut_path, 'w', encoding='utf-8') as f:
    f.write(url_content)
print("✓ Created live web shortcut: رابط_النظام_السحابي_أونلاين.url")

print("\n🎉 Desktop cleanup completed successfully!")
