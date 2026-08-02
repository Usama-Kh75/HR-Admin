import os

def update_file(file_path):
    if not os.path.exists(file_path):
        print(f"File not found: {file_path}")
        return False

    with open(file_path, 'r', encoding='utf-8') as f:
        code = f.read()

    # Old online CDN script tags
    old_cdn_scripts = """    <script src="https://unpkg.com/react@18/umd/react.production.min.js"></script>
    <script src="https://unpkg.com/react-dom@18/umd/react-dom.production.min.js"></script>
    <script src="https://unpkg.com/@babel/standalone@7.26.2/babel.min.js"></script>
    <script src="https://cdn.tailwindcss.com"></script>
    <script src="https://cdn.jsdelivr.net/npm/xlsx@0.18.5/dist/xlsx.full.min.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/exceljs@4.4.0/dist/exceljs.min.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/docx@8.5.0/build/index.umd.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/file-saver@2.0.5/dist/FileSaver.min.js"></script>"""

    # New 100% local offline script tags
    new_local_scripts = """    <script src="libs/react.production.min.js"></script>
    <script src="libs/react-dom.production.min.js"></script>
    <script src="libs/babel.min.js"></script>
    <script src="libs/tailwindcss.js"></script>
    <script src="libs/xlsx.full.min.js"></script>
    <script src="libs/exceljs.min.js"></script>
    <script src="libs/docx.js"></script>
    <script src="libs/FileSaver.min.js"></script>"""

    if old_cdn_scripts in code:
        code = code.replace(old_cdn_scripts, new_local_scripts)
        print(f"✓ Converted online CDN script tags to 100% local offline libs in {file_path}")
    else:
        # Fallback check if individual CDN links are present
        code = re.sub(r'<script\s+src="https://unpkg.com/react@18/umd/react.production.min.js"></script>', '<script src="libs/react.production.min.js"></script>', code)
        code = re.sub(r'<script\s+src="https://unpkg.com/react-dom@18/umd/react-dom.production.min.js"></script>', '<script src="libs/react-dom.production.min.js"></script>', code)
        code = re.sub(r'<script\s+src="https://unpkg.com/@babel/standalone@[^"]+"></script>', '<script src="libs/babel.min.js"></script>', code)
        code = re.sub(r'<script\s+src="https://cdn.tailwindcss.com"></script>', '<script src="libs/tailwindcss.js"></script>', code)
        code = re.sub(r'<script\s+src="https://cdn.jsdelivr.net/npm/xlsx@[^"]+"></script>', '<script src="libs/xlsx.full.min.js"></script>', code)
        code = re.sub(r'<script\s+src="https://cdn.jsdelivr.net/npm/exceljs@[^"]+"></script>', '<script src="libs/exceljs.min.js"></script>', code)
        code = re.sub(r'<script\s+src="https://cdn.jsdelivr.net/npm/docx@[^"]+"></script>', '<script src="libs/docx.js"></script>', code)
        code = re.sub(r'<script\s+src="https://cdn.jsdelivr.net/npm/file-saver@[^"]+"></script>', '<script src="libs/FileSaver.min.js"></script>', code)
        print(f"✓ Converted individual CDN links to local libs in {file_path}")

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(code)
    return True

if __name__ == '__main__':
    update_file('e:/Antigravity projects/HR Admin/index.html')
    update_file('e:/Antigravity projects/HR Admin/نظام_ادراة_الملاك_v7.0_online.html')
    update_file('e:/Antigravity projects/HR Admin/نظام_ادراة_الملاك_v7.0.html')
