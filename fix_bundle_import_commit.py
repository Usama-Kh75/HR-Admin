import os

def update_file(file_path):
    if not os.path.exists(file_path):
        print(f"File not found: {file_path}")
        return False

    with open(file_path, 'r', encoding='utf-8') as f:
        code = f.read()

    # 1. Add incomingBundle state initialization
    if "const [incomingBundle, setIncomingBundle] = useState(null);" not in code:
        code = code.replace(
            "const [incomingStaff, setIncomingStaff] = useState([]);",
            "const [incomingStaff, setIncomingStaff] = useState([]);\n            const [incomingBundle, setIncomingBundle] = useState(null);"
        )

    # 2. Update loadFile handler to set incomingBundle
    old_load_file_block = """                             const data = JSON.parse(text);
                             
                             // في استيراد JSON، نتحقق ما إذا كان الملف هو قالب النسخ الجديد أو مصفوفة قديمة
                             let incomingList = [];
                             if (Array.isArray(data)) {
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

    new_load_file_block = """                             const data = JSON.parse(text);
                             
                             let incomingList = [];
                             if (Array.isArray(data)) {
                                 incomingList = data;
                                 setIncomingBundle(null);
                             } else if (data && (Array.isArray(data.staff) || Array.isArray(data.staffData))) {
                                 incomingList = data.staff || data.staffData;
                                 setIncomingBundle(data);
                             }"""

    if old_load_file_block in code:
        code = code.replace(old_load_file_block, new_load_file_block)

    # 3. Add commitBundleMetadata helper
    commit_helper = """            const commitBundleMetadata = (bundle) => {
                if (!bundle || typeof bundle !== 'object') return;
                if (bundle.officialHolidaysList && Array.isArray(bundle.officialHolidaysList)) {
                    setOfficialHolidays(bundle.officialHolidaysList);
                    safeStorage.setItem('officialHolidaysList', JSON.stringify(bundle.officialHolidaysList));
                }
                if (bundle.hourlyLeaveRecords) {
                    setHourlyLeaveRecords(bundle.hourlyLeaveRecords);
                    safeStorage.setItem('hourlyLeaveRecords', JSON.stringify(bundle.hourlyLeaveRecords));
                }
                if (bundle.overtimeHoursRecords) {
                    setOvertimeHoursRecords(bundle.overtimeHoursRecords);
                    safeStorage.setItem('overtimeHoursRecords', JSON.stringify(bundle.overtimeHoursRecords));
                }
                if (bundle.dailyStatusOverrides) {
                    setDailyStatusOverrides(bundle.dailyStatusOverrides);
                    safeStorage.setItem('dailyStatusOverrides', JSON.stringify(bundle.dailyStatusOverrides));
                }
                if (bundle.shiftAnchorDate) {
                    setAnchorDate(bundle.shiftAnchorDate);
                    safeStorage.setItem('shiftAnchorDate', bundle.shiftAnchorDate);
                }
                if (bundle.threeShiftAnchorSquad) {
                    setThreeShiftAnchorSquad(bundle.threeShiftAnchorSquad);
                    safeStorage.setItem('threeShiftAnchorSquad', bundle.threeShiftAnchorSquad);
                }
                if (bundle.twoShiftAnchorSquad) {
                    setTwoShiftAnchorSquad(bundle.twoShiftAnchorSquad);
                    safeStorage.setItem('twoShiftAnchorSquad', bundle.twoShiftAnchorSquad);
                }
                if (bundle.dataEntryOperator) {
                    setDataEntryOperator(bundle.dataEntryOperator);
                    safeStorage.setItem('dataEntryOperator', bundle.dataEntryOperator);
                }
            };
"""

    if "const commitBundleMetadata =" not in code:
        code = code.replace("const handleSmartMerge = (incoming) => {", commit_helper + "\n            const handleSmartMerge = (incoming) => {")

    # 4. Update handleSmartMerge & handleFullOverwrite to call commitBundleMetadata
    code = code.replace(
        "const sorted = sortByUnit(mergedList);\n                setStaff(sorted);",
        "commitBundleMetadata(incomingBundle);\n                const sorted = sortByUnit(mergedList);\n                setStaff(sorted);"
    )

    code = code.replace(
        "const sorted = sortByUnit(incoming);\n                setStaff(sorted);",
        "commitBundleMetadata(incomingBundle);\n                const sorted = sortByUnit(incoming);\n                setStaff(sorted);"
    )

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(code)
    return True

if __name__ == '__main__':
    update_file('e:/Antigravity projects/HR Admin/index.html')
    update_file('e:/Antigravity projects/HR Admin/نظام_ادراة_الملاك_v7.0_online.html')
    update_file('e:/Antigravity projects/HR Admin/نظام_ادراة_الملاك_v7.0.html')
