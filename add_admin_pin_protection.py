import os

def update_file(file_path):
    if not os.path.exists(file_path):
        print(f"File not found: {file_path}")
        return False

    with open(file_path, 'r', encoding='utf-8') as f:
        code = f.read()

    # 1. PIN protection for deleteEmployee function
    old_delete_fn = """            const deleteEmployee = () => {
                if (!editingEmployee) return;"""

    new_delete_fn = """            const deleteEmployee = () => {
                if (!editingEmployee) return;
                const adminPin = prompt('🔐 يتطلب حذف الموظف إدخال الرمز السري للإداري:');
                if (adminPin !== '1975') {
                    alert('❌ الرمز السري غير صحيح! تم إلغاء عملية الحذف للحماية.');
                    return;
                }"""

    if old_delete_fn in code:
        code = code.replace(old_delete_fn, new_delete_fn)
        print(f"✓ Protected deleteEmployee with PIN 1975 in {file_path}")

    # 2. PIN protection for inline delete button in table
    old_inline_delete = """onClick={() => {
                                                                                const firstName = s.name.split(' ')[0];
                                                                                if (confirm(`⚠️ هل أنت متأكد من حذف الموظف؟\\n\\nالموظف: ${s.name}\\nالرقم الوظيفي: ${s.jobNumber}\\n\\n⚠️ هذه العملية لا يمكن التراجع عنها!`)) {"""

    new_inline_delete = """onClick={() => {
                                                                                const adminPin = prompt('🔐 يتطلب حذف الموظف إدخال الرمز السري للإداري:');
                                                                                if (adminPin !== '1975') {
                                                                                    alert('❌ الرمز السري غير صحيح! تم إلغاء عملية الحذف للحماية.');
                                                                                    return;
                                                                                }
                                                                                const firstName = s.name.split(' ')[0];
                                                                                if (confirm(`⚠️ هل أنت متأكد من حذف الموظف؟\\n\\nالموظف: ${s.name}\\nالرقم الوظيفي: ${s.jobNumber}\\n\\n⚠️ هذه العملية لا يمكن التراجع عنها!`)) {"""

    if old_inline_delete in code:
        code = code.replace(old_inline_delete, new_inline_delete)
        print(f"✓ Protected inline delete button with PIN 1975 in {file_path}")

    # 3. PIN protection for clearAllData function
    old_clear_fn = """            const clearAllData = () => {
                if (confirm('⚠️ هل أنت متأكد من مسح جميع البيانات؟\\n\\nسيتم حذف جميع الموظفين والعودة للنظام الفارغ.')) {"""

    new_clear_fn = """            const clearAllData = () => {
                const adminPin = prompt('🔐 يتطلب مسح جميع البيانات إدخال الرمز السري للإداري:');
                if (adminPin !== '1975') {
                    alert('❌ الرمز السري غير صحيح! تم إلغاء العملية للحماية.');
                    return;
                }
                if (confirm('⚠️ هل أنت متأكد من مسح جميع البيانات؟\\n\\nسيتم حذف جميع الموظفين والعودة للنظام الفارغ.')) {"""

    if old_clear_fn in code:
        code = code.replace(old_clear_fn, new_clear_fn)
        print(f"✓ Protected clearAllData with PIN 1975 in {file_path}")

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(code)
    return True

if __name__ == '__main__':
    update_file('e:/Antigravity projects/HR Admin/index.html')
    update_file('e:/Antigravity projects/HR Admin/نظام_ادراة_الملاك_v6.9_online.html')
    update_file('e:/Antigravity projects/HR Admin/نظام_ادراة_الملاك_v6.9.html')
