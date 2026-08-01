import os

def update_file(file_path):
    if not os.path.exists(file_path):
        print(f"File not found: {file_path}")
        return False

    with open(file_path, 'r', encoding='utf-8') as f:
        code = f.read()

    # 1. Update formatMobileNumber or inline spans with dir="ltr" inline-block
    old_target_modal = """<div className="text-sm font-mono font-black text-amber-950 text-right">
                                                {formatMobileNumber(selectedEmployeeCard.mobile || selectedEmployeeCard.phone)}
                                            </div>"""

    new_target_modal = """<div className="text-sm font-mono font-black text-amber-950 text-right">
                                                <span dir="ltr" className="inline-block dir-ltr">
                                                    {formatMobileNumber(selectedEmployeeCard.mobile || selectedEmployeeCard.phone)}
                                                </span>
                                            </div>"""

    if old_target_modal in code:
        code = code.replace(old_target_modal, new_target_modal)
        print(f"✓ Fixed RTL phone direction in profile modal in {file_path}")

    # 2. Update table cell phone direction
    old_target_table = """<span dir="ltr">{s.mobile || s.phone ? `📱 ${formatMobileNumber(s.mobile || s.phone)}` : '-'}</span>"""
    new_target_table = """<span dir="ltr" className="inline-block dir-ltr">{s.mobile || s.phone ? `📱 ${formatMobileNumber(s.mobile || s.phone)}` : '-'}</span>"""

    if old_target_table in code:
        code = code.replace(old_target_table, new_target_table)
        print(f"✓ Fixed RTL phone direction in search table in {file_path}")

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(code)
    return True

if __name__ == '__main__':
    update_file('e:/Antigravity projects/HR Admin/index.html')
    update_file('e:/Antigravity projects/HR Admin/نظام_ادراة_الملاك_v7.0_online.html')
    update_file('e:/Antigravity projects/HR Admin/نظام_ادراة_الملاك_v7.0.html')
