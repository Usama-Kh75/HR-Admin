import os

def update_file(file_path):
    if not os.path.exists(file_path):
        print(f"File not found: {file_path}")
        return False

    with open(file_path, 'r', encoding='utf-8') as f:
        code = f.read()

    # 1. Update exportBackupJSON to include officialHolidaysList and all records
    old_export = """                    const backupData = {
                        version: 'v7.0 Beta',
                        exportDate: new Date().toISOString(),
                        staff: staff,
                        dailyStatusOverrides: dailyStatusOverrides,
                        shiftAnchorDate: anchorDate,
                        threeShiftAnchorSquad: threeShiftAnchorSquad,
                        twoShiftAnchorSquad: twoShiftAnchorSquad
                    };"""

    new_export = """                    const backupData = {
                        version: 'v7.0 Beta',
                        exportDate: new Date().toISOString(),
                        staff: staff,
                        staffData: staff,
                        officialHolidaysList: officialHolidays,
                        hourlyLeaveRecords: hourlyLeaveRecords,
                        overtimeHoursRecords: overtimeHoursRecords,
                        dailyStatusOverrides: dailyStatusOverrides,
                        shiftAnchorDate: anchorDate,
                        threeShiftAnchorSquad: threeShiftAnchorSquad,
                        twoShiftAnchorSquad: twoShiftAnchorSquad,
                        dataEntryOperator: dataEntryOperator,
                        overtimeSelectedIds: overtimeIds
                    };"""

    if old_export in code:
        code = code.replace(old_export, new_export)
        print(f"✓ Updated exportBackupJSON bundle in {file_path}")

    # 2. Check import handler to ensure it imports officialHolidaysList
    # Search for JSON import handler (e.g. FileReader onLoad)
    old_import_block = """                    if (data.staff && Array.isArray(data.staff)) {
                        setStaff(data.staff);
                        safeStorage.setItem('staffData', JSON.stringify(data.staff));
                    }"""

    new_import_block = """                    if (data.staff && Array.isArray(data.staff)) {
                        setStaff(data.staff);
                        safeStorage.setItem('staffData', JSON.stringify(data.staff));
                    } else if (data.staffData && Array.isArray(data.staffData)) {
                        setStaff(data.staffData);
                        safeStorage.setItem('staffData', JSON.stringify(data.staffData));
                    }
                    if (data.officialHolidaysList && Array.isArray(data.officialHolidaysList)) {
                        setOfficialHolidays(data.officialHolidaysList);
                        safeStorage.setItem('officialHolidaysList', JSON.stringify(data.officialHolidaysList));
                    }
                    if (data.hourlyLeaveRecords) {
                        setHourlyLeaveRecords(data.hourlyLeaveRecords);
                        safeStorage.setItem('hourlyLeaveRecords', JSON.stringify(data.hourlyLeaveRecords));
                    }
                    if (data.overtimeHoursRecords) {
                        setOvertimeHoursRecords(data.overtimeHoursRecords);
                        safeStorage.setItem('overtimeHoursRecords', JSON.stringify(data.overtimeHoursRecords));
                    }
                    if (data.dataEntryOperator) {
                        setDataEntryOperator(data.dataEntryOperator);
                        safeStorage.setItem('dataEntryOperator', data.dataEntryOperator);
                    }"""

    if old_import_block in code:
        code = code.replace(old_import_block, new_import_block)
        print(f"✓ Updated JSON import handler in {file_path}")

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(code)
    return True

if __name__ == '__main__':
    update_file('e:/Antigravity projects/HR Admin/index.html')
    update_file('e:/Antigravity projects/HR Admin/نظام_ادراة_الملاك_v7.0_online.html')
    update_file('e:/Antigravity projects/HR Admin/نظام_ادراة_الملاك_v7.0.html')
