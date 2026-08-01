import os
import re

def update_file(file_path):
    if not os.path.exists(file_path):
        print(f"File not found: {file_path}")
        return False

    with open(file_path, 'r', encoding='utf-8') as f:
        code = f.read()

    # 1. Add formatMobileNumber helper function inside component
    formatter_code = """
            // دالة تنسيق رقم الهاتف النقال لتسهيل القراءة (مثل: 0420 329 0770)
            const formatMobileNumber = (phoneStr) => {
                if (!phoneStr || phoneStr === 'غير مسجل') return 'غير مسجل';
                const digits = String(phoneStr).replace(/\\D/g, '');
                if (digits.length === 11) {
                    return `${digits.slice(0, 4)} ${digits.slice(4, 7)} ${digits.slice(7)}`;
                }
                if (digits.length === 10) {
                    return `${digits.slice(0, 3)} ${digits.slice(3, 6)} ${digits.slice(6)}`;
                }
                return phoneStr;
            };
    """

    if "const formatMobileNumber =" not in code:
        code = code.replace("const [cardFieldsVisibility, setCardFieldsVisibility]", formatter_code + "\n            const [cardFieldsVisibility, setCardFieldsVisibility]")
        print(f"✓ Added formatMobileNumber helper function to {file_path}")

    # 2. Update mobile phone rendering in search table & profile modal
    code = code.replace(
        "{s.mobile || s.phone ? `📱 ${s.mobile || s.phone}` : '-'}",
        "{s.mobile || s.phone ? `📱 ${formatMobileNumber(s.mobile || s.phone)}` : '-'}"
    )

    code = code.replace(
        "{selectedEmployeeCard.mobile || selectedEmployeeCard.phone || 'غير مسجل'}",
        "{formatMobileNumber(selectedEmployeeCard.mobile || selectedEmployeeCard.phone)}"
    )

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(code)
    print(f"✓ Formatted mobile phone display in {file_path}")
    return True

if __name__ == '__main__':
    update_file('e:/Antigravity projects/HR Admin/index.html')
    update_file('e:/Antigravity projects/HR Admin/نظام_ادراة_الملاك_v7.0_online.html')
    update_file('e:/Antigravity projects/HR Admin/نظام_ادراة_الملاك_v7.0.html')
