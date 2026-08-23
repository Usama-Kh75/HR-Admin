import os

files = [
    'e:/Antigravity projects/HR Admin/index.html',
    'e:/Antigravity projects/HR Admin/نظام_ادارة_الملاك_v8.0_cloud.html',
    'e:/Antigravity projects/HR Admin/نظام_ادارة_الملاك_v8.0_online.html',
    'e:/Antigravity projects/HR Admin/نظام_ادارة_الملاك_v8.0_offline.html',
    r'C:\Users\asalz\OneDrive\Desktop\index.html',
    r'C:\Users\asalz\OneDrive\Desktop\نظام_ادارة_الملاك_v8.0_أوفلاين_محلي.html'
]

for file_path in files:
    if os.path.exists(file_path):
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Replace robots meta tag to block all search engine indexing
        old_robots = '<meta name="robots" content="index, follow">'
        new_robots = '<meta name="robots" content="noindex, nofollow, noarchive, nosnippet">'
        
        if old_robots in content:
            content = content.replace(old_robots, new_robots)
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"✓ Updated robots meta tag in: {os.path.basename(file_path)}")

print("✓ Completed search engine privacy hardening!")
