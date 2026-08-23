import os

# Create standalone mobile HTML file with CDN fallbacks for direct file opening on Android/iOS
with open('e:/Antigravity projects/HR Admin/index.html', 'r', encoding='utf-8') as f:
    code = f.read()

# Replace local libs with CDN links suitable for opening directly via content:// or file:// on Mobile
local_libs = """    <script src="libs/react.production.min.js"></script>
    <script src="libs/react-dom.production.min.js"></script>
    <script src="libs/babel.min.js"></script>
    <script src="libs/tailwindcss.js"></script>
    <script src="libs/xlsx.full.min.js"></script>
    <script src="libs/exceljs.min.js"></script>
    <script src="libs/docx.js"></script>
    <script src="libs/FileSaver.min.js"></script>"""

mobile_cdn_libs = """    <!-- مكتبات مهيأة خصيصاً للفتح المباشر على الموبايل -->
    <script src="https://unpkg.com/react@18/umd/react.production.min.js"></script>
    <script src="https://unpkg.com/react-dom@18/umd/react-dom.production.min.js"></script>
    <script src="https://unpkg.com/@babel/standalone@7.26.2/babel.min.js"></script>
    <script src="https://cdn.tailwindcss.com"></script>
    <script src="https://cdn.jsdelivr.net/npm/xlsx@0.18.5/dist/xlsx.full.min.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/exceljs@4.4.0/dist/exceljs.min.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/docx@8.5.0/build/index.umd.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/file-saver@2.0.5/dist/FileSaver.min.js"></script>"""

code_mobile = code.replace(local_libs, mobile_cdn_libs)

# Ensure default role is 'admin' (passwordless direct mode on mobile file)
code_mobile = code_mobile.replace("const [currentUserRole, setCurrentUserRole] = useState(null);", "const [currentUserRole, setCurrentUserRole] = useState('admin');")

# Save file as نظام_ادراة_الملاك_v7.0_mobile.html
with open('e:/Antigravity projects/HR Admin/نظام_ادراة_الملاك_v7.0_mobile.html', 'w', encoding='utf-8') as f:
    f.write(code_mobile)

print("✓ Created نظام_ادراة_الملاك_v7.0_mobile.html for direct mobile file opening")
