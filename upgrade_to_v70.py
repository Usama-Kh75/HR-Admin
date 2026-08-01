import os

# 1. Read latest index.html
with open('e:/Antigravity projects/HR Admin/index.html', 'r', encoding='utf-8') as f:
    code = f.read()

# Update version strings to v7.0 Beta
code = code.replace('<title>نظام إدارة الملاك - الإصدار v6.9 Beta</title>', '<title>نظام إدارة الملاك - الإصدار v7.0 Beta</title>')
code = code.replace("version: 'v6.9 Beta',", "version: 'v7.0 Beta',")
code = code.replace('الإصدار v6.9 Beta', 'الإصدار v7.0 Beta')
code = code.replace('v6.9 Beta', 'v7.0 Beta')

# Write updated code back to index.html, v7.0_online.html, and v7.0.html
with open('e:/Antigravity projects/HR Admin/index.html', 'w', encoding='utf-8') as f:
    f.write(code)

with open('e:/Antigravity projects/HR Admin/نظام_ادراة_الملاك_v7.0_online.html', 'w', encoding='utf-8') as f:
    f.write(code)

with open('e:/Antigravity projects/HR Admin/نظام_ادراة_الملاك_v7.0.html', 'w', encoding='utf-8') as f:
    f.write(code)

print("✓ Created index.html, v7.0_online.html, and v7.0.html with official v7.0 Beta release")

# 2. Update HR_Admin_Handoff.md
with open('e:/Antigravity projects/HR Admin/HR_Admin_Handoff.md', 'r', encoding='utf-8') as f:
    handoff = f.read()

handoff = handoff.replace('تاريخ التحديث: 02 أغسطس 2026 | الإصدار الحالي: v6.9 Beta', 'تاريخ التحديث: 02 أغسطس 2026 | الإصدار الحالي: v7.0 Beta')

v70_decisions = """11. 📇 **بطاقة المنتسب الفاخرة وتخصيص الحقول المطبوعة (Printable Profile Customizer):**
    * إضافة بطاقة هوية فاخرة تعريفيّة بالمنتسب للطباعة A4 تحتوي على إظهار رقم الهاتف النقال في جدول البحث، واعتمدت قياس البدلة الموحد وقياس الحذاء، مع تزويدها بزر `⚙️ تخصيص الحقول المعروضة` لتأشير وإخفاء أو إظهار أي حقل قبل الطباعة.

---"""

v70_history = """* **v7.0 Beta (الإصدار الذهبي الرسمي الحالي):**
  * إطلاق ميزة **بطاقة المنتسب الفاخرة للطباعة A4** مع شريط تخصيص وإخفاء/إظهار الحقول بـ Checkboxes قبل الطباعة.
  * إظهار رقم الهاتف النقال في جدول نتائج البحث الرئيسي بوضوح.
  * تفعيل **نظام الصلاحيات المحدث والتعرف الآلي الذكي على كلمة المرور** بحقل واحد عند ضغط زر `✓ ابدأ العمل الآن`.
  * إضافة **نافذة إدارة وتجديد كلمات المرور المشرّفة** لمدير النظام.
  * التمييز والربط السلس بين النسخ المستقلة المباشرة بدون كلمة سر ونسخة السيرفر الشبكية المحمية.

* **v6.9 Beta:**"""

if 'Printable Profile Customizer' not in handoff:
    handoff = handoff.replace('---', v70_decisions, 1)
    handoff = handoff.replace('* **v6.9 Beta (الإصدار الحالي):**', v70_history)
    handoff = handoff.replace('* **v6.9 Beta:**', '* **v6.9 Beta:**')

with open('e:/Antigravity projects/HR Admin/HR_Admin_Handoff.md', 'w', encoding='utf-8') as f:
    f.write(handoff)

print("✓ Updated HR_Admin_Handoff.md to v7.0 Beta")
