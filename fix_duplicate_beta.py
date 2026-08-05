import os

files_to_fix = [
    'e:/Antigravity projects/HR Admin/index.html',
    'e:/Antigravity projects/HR Admin/نظام_ادراة_الملاك_v7.5_cloud.html'
]

for fpath in files_to_fix:
    if os.path.exists(fpath):
        with open(fpath, 'r', encoding='utf-8') as f:
            code = f.read()

        code = code.replace('v7.5 Cloud Edition Beta Beta', 'v7.5 Cloud Edition Beta')
        code = code.replace('Beta Beta', 'Beta')

        with open(fpath, 'w', encoding='utf-8') as f:
            f.write(code)
        print(f"✓ Fixed duplicated Beta in {fpath}")
