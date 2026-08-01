import os
import re

def update_file(file_path):
    if not os.path.exists(file_path):
        print(f"File not found: {file_path}")
        return False

    with open(file_path, 'r', encoding='utf-8') as f:
        code = f.read()

    # Replace any incorrect references to shiftAnchorDate in the sync engine
    code = code.replace("shiftAnchorDate: shiftAnchorDate,", "shiftAnchorDate: anchorDate,")
    code = code.replace("], [staff, officialHolidays, hourlyLeaveRecords, overtimeHoursRecords, dailyStatusOverrides, shiftAnchorDate, dataEntryOperator]);", "], [staff, officialHolidays, hourlyLeaveRecords, overtimeHoursRecords, dailyStatusOverrides, anchorDate, dataEntryOperator]);")

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(code)
    print(f"✓ Fixed shiftAnchorDate -> anchorDate in {file_path}")
    return True

if __name__ == '__main__':
    update_file('e:/Antigravity projects/HR Admin/index.html')
    update_file('e:/Antigravity projects/HR Admin/نظام_ادراة_الملاك_v6.8_online.html')
    update_file('e:/Antigravity projects/HR Admin/نظام_ادراة_الملاك_v6.8.html')
