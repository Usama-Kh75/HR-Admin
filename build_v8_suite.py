import os
import re

# Read current master index.html
with open('e:/Antigravity projects/HR Admin/index.html', 'r', encoding='utf-8') as f:
    master_code = f.read()

# 1. Update version strings to v8.0 Master Suite across master_code
v8_master_code = master_code.replace("v7.5 Cloud Edition Beta", "v8.0 Cloud Edition")
v8_master_code = v8_master_code.replace("v7.5", "v8.0")
v8_master_code = v8_master_code.replace("الإصدار v7.5", "الإصدار v8.0")

with open('e:/Antigravity projects/HR Admin/index.html', 'w', encoding='utf-8') as f:
    f.write(v8_master_code)

# 2. Generate نظام_ادارة_الملاك_v8.0_cloud.html
with open('e:/Antigravity projects/HR Admin/نظام_ادارة_الملاك_v8.0_cloud.html', 'w', encoding='utf-8') as f:
    f.write(v8_master_code)

# 3. Generate نظام_ادارة_الملاك_v8.0_online.html (Intranet + Cloud Dual)
online_code = v8_master_code.replace("<title>نظام إدارة الملاك - الإصدار v8.0 Cloud Edition ☁️</title>", "<title>نظام إدارة الملاك - الإصدار v8.0 Online (سحابي ومحلي) 🌐</title>")
with open('e:/Antigravity projects/HR Admin/نظام_ادارة_الملاك_v8.0_online.html', 'w', encoding='utf-8') as f:
    f.write(online_code)

# 4. Generate نظام_ادارة_الملاك_v8.0_offline.html (Pure Offline Standalone)
offline_code = v8_master_code.replace("<title>نظام إدارة الملاك - الإصدار v8.0 Cloud Edition ☁️</title>", "<title>نظام إدارة الملاك - الإصدار v8.0 Standalone (أوفلاين محلي) 💾</title>")
# Update badge for offline edition to display offline storage
offline_badge_old = '{cloudSyncStatus && cloudSyncStatus.connected ? ('
offline_badge_new = '{false ? ('
offline_code = offline_code.replace(offline_badge_old, offline_badge_new, 1)

with open('e:/Antigravity projects/HR Admin/نظام_ادارة_الملاك_v8.0_offline.html', 'w', encoding='utf-8') as f:
    f.write(offline_code)

# 5. Copy to Desktop if available
desktop_dir = 'C:/Users/asalz/OneDrive/Desktop'
if os.path.exists(desktop_dir):
    try:
        with open(os.path.join(desktop_dir, 'نظام_ادارة_الملاك_v8.0_أوفلاين_محلي.html'), 'w', encoding='utf-8') as f:
            f.write(offline_code)
        with open(os.path.join(desktop_dir, 'نظام_ادارة_الملاك_v8.0_offline.html'), 'w', encoding='utf-8') as f:
            f.write(offline_code)
        with open(os.path.join(desktop_dir, 'نظام_ادارة_الملاك_v8.0_online.html'), 'w', encoding='utf-8') as f:
            f.write(online_code)
        with open(os.path.join(desktop_dir, 'نظام_ادارة_الملاك_v8.0_cloud.html'), 'w', encoding='utf-8') as f:
            f.write(v8_master_code)
        print("  ✓ Synced to Desktop:", desktop_dir)
    except Exception as err:
        print("  ⚠️ Could not copy to desktop:", err)

print("✓ Generated v8.0 Master Suite files:")
print("  - index.html (v8.0 Cloud Edition)")
print("  - نظام_ادارة_الملاك_v8.0_cloud.html")
print("  - نظام_ادارة_الملاك_v8.0_online.html")
print("  - نظام_ادارة_الملاك_v8.0_offline.html")
