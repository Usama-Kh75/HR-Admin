import os

# Update index.html to use CDN links for GitHub Pages online hosting
with open('e:/Antigravity projects/HR Admin/index.html', 'r', encoding='utf-8') as f:
    code = f.read()

local_libs = """    <script src="libs/react.production.min.js"></script>
    <script src="libs/react-dom.production.min.js"></script>
    <script src="libs/babel.min.js"></script>
    <script src="libs/tailwindcss.js"></script>
    <script src="libs/xlsx.full.min.js"></script>
    <script src="libs/exceljs.min.js"></script>
    <script src="libs/docx.js"></script>
    <script src="libs/FileSaver.min.js"></script>"""

cdn_libs = """    <script src="https://unpkg.com/react@18/umd/react.production.min.js"></script>
    <script src="https://unpkg.com/react-dom@18/umd/react-dom.production.min.js"></script>
    <script src="https://unpkg.com/@babel/standalone@7.26.2/babel.min.js"></script>
    <script src="https://cdn.tailwindcss.com"></script>
    <script src="https://cdn.jsdelivr.net/npm/xlsx@0.18.5/dist/xlsx.full.min.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/exceljs@4.4.0/dist/exceljs.min.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/docx@8.5.0/build/index.umd.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/file-saver@2.0.5/dist/FileSaver.min.js"></script>"""

if local_libs in code:
    code = code.replace(local_libs, cdn_libs)

with open('e:/Antigravity projects/HR Admin/index.html', 'w', encoding='utf-8') as f:
    f.write(code)

print("✓ Updated index.html CDN links for GitHub Pages")
