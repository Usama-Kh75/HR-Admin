import os

# Update version title and state to include Beta: v7.5 Cloud Edition Beta
files_to_update = [
    'e:/Antigravity projects/HR Admin/index.html',
    'e:/Antigravity projects/HR Admin/نظام_ادراة_الملاك_v7.5_cloud.html'
]

for fpath in files_to_update:
    if os.path.exists(fpath):
        with open(fpath, 'r', encoding='utf-8') as f:
            code = f.read()

        code = code.replace('<title>نظام إدارة الملاك - الإصدار v7.5 Cloud Edition ☁️</title>', '<title>نظام إدارة الملاك - الإصدار v7.5 Cloud Edition Beta ☁️</title>')
        code = code.replace("version: 'v7.5 Cloud Edition',", "version: 'v7.5 Cloud Edition Beta',")
        code = code.replace('الإصدار v7.5 Cloud Edition', 'الإصدار v7.5 Cloud Edition Beta')
        code = code.replace('v7.5 Cloud Edition', 'v7.5 Cloud Edition Beta')

        with open(fpath, 'w', encoding='utf-8') as f:
            f.write(code)
        print(f"✓ Added Beta to version title in {fpath}")

# Update HR_Admin_Handoff.md
handoff_path = 'e:/Antigravity projects/HR Admin/HR_Admin_Handoff.md'
if os.path.exists(handoff_path):
    with open(handoff_path, 'r', encoding='utf-8') as f:
        handoff = f.read()

    handoff = handoff.replace('v7.0 Beta', 'v7.5 Cloud Edition Beta')
    with open(handoff_path, 'w', encoding='utf-8') as f:
        f.write(handoff)
    print("✓ Updated HR_Admin_Handoff.md to v7.5 Cloud Edition Beta")
