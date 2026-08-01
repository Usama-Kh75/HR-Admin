import os

def update_file(file_path):
    if not os.path.exists(file_path):
        print(f"File not found: {file_path}")
        return False

    with open(file_path, 'r', encoding='utf-8') as f:
        code = f.read()

    # Remove F12 / DevTools block script if present
    target_block = """    <!-- درع الأمان والحماية من التلاعب بالنظام (Security & Anti-Tamper Shield) -->
    <script>
        (function() {
            // منع فتح أدوات المطور عبر اختصارات لوحة المفاتيح
            document.addEventListener('keydown', function(e) {
                // F12
                if (e.keyCode === 123) {
                    e.preventDefault();
                    return false;
                }
                // Ctrl+Shift+I, Ctrl+Shift+J, Ctrl+Shift+C, Ctrl+U
                if (e.ctrlKey && (e.shiftKey && (e.keyCode === 73 || e.keyCode === 74 || e.keyCode === 67) || e.keyCode === 85)) {
                    e.preventDefault();
                    return false;
                }
            });
            // تعطيل القائمة اليمينية للحماية من Inspect Element
            document.addEventListener('contextmenu', function(e) {
                // السماح بالقائمة اليمينية فقط في حقول الإدخال للنصوص
                if (e.target.tagName !== 'INPUT' && e.target.tagName !== 'TEXTAREA') {
                    e.preventDefault();
                }
            });
        })();
    </script>"""

    if target_block in code:
        code = code.replace(target_block, "")
        print(f"✓ Removed F12 restriction script from {file_path}")

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(code)
    return True

if __name__ == '__main__':
    update_file('e:/Antigravity projects/HR Admin/index.html')
    update_file('e:/Antigravity projects/HR Admin/نظام_ادراة_الملاك_v6.9_online.html')
    update_file('e:/Antigravity projects/HR Admin/نظام_ادراة_الملاك_v6.9.html')
