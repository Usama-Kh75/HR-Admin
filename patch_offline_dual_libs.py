import os

offline_file = 'e:/Antigravity projects/HR Admin/نظام_ادارة_الملاك_v8.0_offline.html'
with open(offline_file, 'r', encoding='utf-8') as f:
    code = f.read()

old_scripts = """    <script src="https://unpkg.com/react@18/umd/react.production.min.js"></script>
    <script src="https://unpkg.com/react-dom@18/umd/react-dom.production.min.js"></script>
    <script src="https://unpkg.com/@babel/standalone@7.26.2/babel.min.js"></script>
    <script src="https://cdn.tailwindcss.com"></script>
    <script src="https://cdn.jsdelivr.net/npm/xlsx@0.18.5/dist/xlsx.full.min.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/exceljs@4.4.0/dist/exceljs.min.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/docx@8.5.0/build/index.umd.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/file-saver@2.0.5/dist/FileSaver.min.js"></script>"""

new_scripts = """    <!-- محمل المكتبات المزدوج الذكي: يقرأ من مجلد libs المحلي أوفلاين، مع دعم التبديل للإنترنت -->
    <script src="./libs/react.production.min.js" onerror="this.onerror=null;this.src='https://unpkg.com/react@18/umd/react.production.min.js'"></script>
    <script src="./libs/react-dom.production.min.js" onerror="this.onerror=null;this.src='https://unpkg.com/react-dom@18/umd/react-dom.production.min.js'"></script>
    <script src="./libs/babel.min.js" onerror="this.onerror=null;this.src='https://unpkg.com/@babel/standalone@7.26.2/babel.min.js'"></script>
    <script src="./libs/tailwindcss.js" onerror="this.onerror=null;this.src='https://cdn.tailwindcss.com'"></script>
    <script src="./libs/xlsx.full.min.js" onerror="this.onerror=null;this.src='https://cdn.jsdelivr.net/npm/xlsx@0.18.5/dist/xlsx.full.min.js'"></script>
    <script src="./libs/exceljs.min.js" onerror="this.onerror=null;this.src='https://cdn.jsdelivr.net/npm/exceljs@4.4.0/dist/exceljs.min.js'"></script>
    <script src="./libs/docx.js" onerror="this.onerror=null;this.src='https://cdn.jsdelivr.net/npm/docx@8.5.0/build/index.umd.js'"></script>
    <script src="./libs/FileSaver.min.js" onerror="this.onerror=null;this.src='https://cdn.jsdelivr.net/npm/file-saver@2.0.5/dist/FileSaver.min.js'"></script>"""

if old_scripts in code:
    code = code.replace(old_scripts, new_scripts)
    print("✓ Patched offline html with dual libs loader")

with open(offline_file, 'w', encoding='utf-8') as f:
    f.write(code)

# Copy to Desktop
desktop_offline = r'C:\Users\asalz\OneDrive\Desktop\نظام_ادارة_الملاك_v8.0_أوفلاين_محلي.html'
with open(desktop_offline, 'w', encoding='utf-8') as f:
    f.write(code)

print("✓ Copied updated offline file to Desktop!")
