import os

def update_file(file_path):
    if not os.path.exists(file_path):
        print(f"File not found: {file_path}")
        return False

    with open(file_path, 'r', encoding='utf-8') as f:
        code = f.read()

    old_import_target = """                            if (Array.isArray(data)) {
                                incomingList = data;
                            } else if (data && Array.isArray(data.staff)) {
                                incomingList = data.staff;
                                if (data.dailyStatusOverrides) {
                                    setDailyStatusOverrides(data.dailyStatusOverrides);
                                    safeStorage.setItem('dailyStatusOverrides', JSON.stringify(data.dailyStatusOverrides));
                                }
                                if (data.shiftAnchorDate) {
                                    setAnchorDate(data.shiftAnchorDate);
                                    safeStorage.setItem('shiftAnchorDate', data.shiftAnchorDate);
                                }
                                if (data.threeShiftAnchorSquad) {
                                    setThreeShiftAnchorSquad(data.threeShiftAnchorSquad);
                                    safeStorage.setItem('threeShiftAnchorSquad', data.threeShiftAnchorSquad);
                                }
                                if (data.twoShiftAnchorSquad) {
                                    setTwoShiftAnchorSquad(data.twoShiftAnchorSquad);
                                    safeStorage.setItem('twoShiftAnchorSquad', data.twoShiftAnchorSquad);
                                }
                            }"""

    new_import_target = """                            if (Array.isArray(data)) {
                                incomingList = data;
                            } else if (data && (Array.isArray(data.staff) || Array.isArray(data.staffData))) {
                                incomingList = data.staff || data.staffData;
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
                                if (data.dailyStatusOverrides) {
                                    setDailyStatusOverrides(data.dailyStatusOverrides);
                                    safeStorage.setItem('dailyStatusOverrides', JSON.stringify(data.dailyStatusOverrides));
                                }
                                if (data.shiftAnchorDate) {
                                    setAnchorDate(data.shiftAnchorDate);
                                    safeStorage.setItem('shiftAnchorDate', data.shiftAnchorDate);
                                }
                                if (data.threeShiftAnchorSquad) {
                                    setThreeShiftAnchorSquad(data.threeShiftAnchorSquad);
                                    safeStorage.setItem('threeShiftAnchorSquad', data.threeShiftAnchorSquad);
                                }
                                if (data.twoShiftAnchorSquad) {
                                    setTwoShiftAnchorSquad(data.twoShiftAnchorSquad);
                                    safeStorage.setItem('twoShiftAnchorSquad', data.twoShiftAnchorSquad);
                                }
                                if (data.dataEntryOperator) {
                                    setDataEntryOperator(data.dataEntryOperator);
                                    safeStorage.setItem('dataEntryOperator', data.dataEntryOperator);
                                }
                            }"""

    if old_import_target in code:
        code = code.replace(old_import_target, new_import_target)
        print(f"✓ Successfully updated JSON import handler in {file_path}")
    else:
        print(f"Target import block not found in {file_path}")

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(code)
    return True

if __name__ == '__main__':
    update_file('e:/Antigravity projects/HR Admin/index.html')
    update_file('e:/Antigravity projects/HR Admin/نظام_ادراة_الملاك_v7.0_online.html')
    update_file('e:/Antigravity projects/HR Admin/نظام_ادراة_الملاك_v7.0.html')
