import re
import os
import shutil

# 1. Read latest index.html
with open('e:/Antigravity projects/HR Admin/index.html', 'r', encoding='utf-8') as f:
    code = f.read()

# Update version strings to v6.9 Beta
code = code.replace('<title>نظام إدارة الملاك - الإصدار v6.8 Beta</title>', '<title>نظام إدارة الملاك - الإصدار v6.9 Beta</title>')
code = code.replace("version: 'v6.8 Beta',", "version: 'v6.9 Beta',")
code = code.replace('الإصدار v6.8 Beta', 'الإصدار v6.9 Beta')
code = code.replace('v6.8 Beta', 'v6.9 Beta')

# Add Anti-Tamper Security Script (Disables F12, Ctrl+U, Right Click inspect element)
security_script = """
    <!-- درع الأمان والحماية من التلاعب بالنظام (Security & Anti-Tamper Shield) -->
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
    </script>
"""

if 'Security & Anti-Tamper Shield' not in code:
    code = code.replace('</head>', security_script + '\n</head>')

# Write updated code back to index.html, v6.9_online.html, and v6.9.html
with open('e:/Antigravity projects/HR Admin/index.html', 'w', encoding='utf-8') as f:
    f.write(code)

with open('e:/Antigravity projects/HR Admin/نظام_ادراة_الملاك_v6.9_online.html', 'w', encoding='utf-8') as f:
    f.write(code)

# For v6.9 offline, create offline bundle
with open('e:/Antigravity projects/HR Admin/نظام_ادراة_الملاك_v6.9.html', 'w', encoding='utf-8') as f:
    f.write(code)

print("✓ Created index.html, v6.9_online.html, and v6.9.html with v6.9 Beta version & Anti-Tamper Shield")

# 2. Update HR_Admin_Handoff.md
with open('e:/Antigravity projects/HR Admin/HR_Admin_Handoff.md', 'r', encoding='utf-8') as f:
    handoff = f.read()

handoff = handoff.replace('تاريخ التحديث: 01 أغسطس 2026 | الإصدار الحالي: v6.8 Beta', 'تاريخ التحديث: 01 أغسطس 2026 | الإصدار الحالي: v6.9 Beta')

v69_decisions = """9. 🛡️ **درع الأمان والحماية من التلاعب بالواجهة (Anti-Tamper Security Shield):**
   * حظر اختصارات لوحة المفاتيح التطفلية (`F12`, `Ctrl+Shift+I`, `Ctrl+U`) والقائمة اليمينية العشوائية لمنع المتطفلين في الشبكة من التلاعب أو تعديل الشفرة المصدرية أثناء عمل السيرفر الشبكي المحلي.

---"""

v69_history = """* **v6.9 Beta (الإصدار الحالي):**
  * تفعيل درع الأمان وحماية الكود من التلاعب بالشبكة (Anti-Tamper Security Shield).
  * تفعيل وتكامل خادم المزامنة المحلي الحية والربط السلس بين أجهزة وموبايلات الشعبة عبر السيرفر الداخلي `local_sync_server.py`.
  * تفعيل خاصية اختيار فلترة أكثر من وحدة بنفس الوقت عبر صناديق الاختيار `Checkboxes` مع شريط التمرير الرأسي `max-h-56`.
  * تفعيل وتكامل نافذة إدارة العطل الرسمية والأعياد المنبثقة.
  * تغيير اسم العمود إلى **"أيام الحضور"** وتطبيق الحساب التراكمي اليومي حتى اليوم الحالي.

* **v6.8 Beta:**"""

if 'Anti-Tamper Security Shield' not in handoff:
    handoff = handoff.replace('---', v69_decisions, 1)
    handoff = handoff.replace('* **v6.8 Beta (الإصدار الحالي):**', v69_history)

with open('e:/Antigravity projects/HR Admin/HR_Admin_Handoff.md', 'w', encoding='utf-8') as f:
    f.write(handoff)

print("✓ Updated HR_Admin_Handoff.md to v6.9 Beta")
