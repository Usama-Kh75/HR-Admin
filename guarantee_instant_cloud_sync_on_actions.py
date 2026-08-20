import os

with open('e:/Antigravity projects/HR Admin/index.html', 'r', encoding='utf-8') as f:
    code = f.read()

# 1. Update pushDataToCloud to support beacon / instant guarantee
push_fn_start = "const pushDataToCloud = async (bundle = null) => {"
push_fn_enhanced = """const pushDataToCloud = async (bundle = null) => {
                try {
                    setCloudSyncStatus(prev => ({ ...prev, syncing: true }));
                    const nowIso = new Date().toISOString();
                    lastCloudTimeRef.current = nowIso;
                    const dataPayload = bundle || {
                        staffData: staff,
                        officialHolidaysList: officialHolidays,
                        hourlyLeaveRecords: hourlyLeaveRecords,
                        overtimeHoursRecords: overtimeHoursRecords,
                        dailyStatusOverrides: dailyStatusOverrides,
                        shiftAnchorDate: anchorDate,
                        threeShiftAnchorSquad: threeShiftAnchorSquad,
                        twoShiftAnchorSquad: twoShiftAnchorSquad,
                        dataEntryOperator: dataEntryOperator,
                        overtimeSelectedIds: overtimeIds,
                        lastCloudUpdate: nowIso,
                        pendingDeletionRequest: pendingDeletionRequest
                    };

                    // بث سريع مباشر عبر fetch
                    const res = await fetch(FIREBASE_DB_URL, {
                        method: 'PUT',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify(dataPayload),
                        keepalive: true // يضمن استمرار إرسال البيانات حتى لو أغلق المستخدم المتصفح فوراً
                    });
                    if (res.ok) {
                        setCloudSyncStatus({ connected: true, syncing: false, lastSync: new Date().toLocaleTimeString('ar-IQ') });
                    }
                } catch (err) {
                    console.warn("Could not push to Firebase Cloud:", err);
                }
            };"""

old_push_fn_full_start = 'const pushDataToCloud = async (bundle = null) => {'
old_push_fn_full_end = 'React.useEffect(() => {\n                fetchCloudData();'

s_idx = code.find(old_push_fn_full_start)
e_idx = code.find(old_push_fn_full_end)

if s_idx != -1 and e_idx != -1:
    code = code[:s_idx] + push_fn_enhanced + "\n\n            " + code[e_idx:]
    print("✓ Enhanced pushDataToCloud with keepalive: true for instant delivery even on close")

# 2. Update saveEmployeeEdit to directly call pushDataToCloud with updatedStaff
old_save_emp = """                const sortedStaff = sortByUnit(updatedStaff);
                setStaff(sortedStaff);
                setShowEditModal(false);
                setEditingEmployee(null);
                stopCamera();
            };"""

new_save_emp = """                const sortedStaff = sortByUnit(updatedStaff);
                setStaff(sortedStaff);
                safeStorage.setItem('staffData', JSON.stringify(sortedStaff));
                // بث مباشر وفوري للسحابة فور الضغط على حفظ
                pushDataToCloud({
                    staffData: sortedStaff,
                    officialHolidaysList: officialHolidays,
                    hourlyLeaveRecords: hourlyLeaveRecords,
                    overtimeHoursRecords: overtimeHoursRecords,
                    dailyStatusOverrides: dailyStatusOverrides,
                    shiftAnchorDate: anchorDate,
                    threeShiftAnchorSquad: threeShiftAnchorSquad,
                    twoShiftAnchorSquad: twoShiftAnchorSquad,
                    dataEntryOperator: dataEntryOperator,
                    overtimeSelectedIds: overtimeIds,
                    lastCloudUpdate: new Date().toISOString(),
                    pendingDeletionRequest: pendingDeletionRequest
                });
                setShowEditModal(false);
                setEditingEmployee(null);
                stopCamera();
            };"""

if old_save_emp in code:
    code = code.replace(old_save_emp, new_save_emp)
    print("✓ Injected instant direct cloud push inside saveEmployeeEdit")

# 3. Update setEmployeeDailyStatusOverride to directly call pushDataToCloud with nextOverrides
old_status_override = """                setDailyStatusOverrides(prev => {
                    const next = { ...prev };
                    if (!next[dateStr]) next[dateStr] = {};
                    next[dateStr][empId] = status;
                    return next;
                });
            };"""

new_status_override = """                let nextOverrides;
                setDailyStatusOverrides(prev => {
                    const next = { ...prev };
                    if (!next[dateStr]) next[dateStr] = {};
                    next[dateStr][empId] = status;
                    nextOverrides = next;
                    return next;
                });
                // بث مباشر وفوري للموقف اليومي للسحابة في نفس اللحظة
                setTimeout(() => {
                    if (nextOverrides) {
                        pushDataToCloud({
                            staffData: staff,
                            officialHolidaysList: officialHolidays,
                            hourlyLeaveRecords: hourlyLeaveRecords,
                            overtimeHoursRecords: overtimeHoursRecords,
                            dailyStatusOverrides: nextOverrides,
                            shiftAnchorDate: anchorDate,
                            threeShiftAnchorSquad: threeShiftAnchorSquad,
                            twoShiftAnchorSquad: twoShiftAnchorSquad,
                            dataEntryOperator: dataEntryOperator,
                            overtimeSelectedIds: overtimeIds,
                            lastCloudUpdate: new Date().toISOString(),
                            pendingDeletionRequest: pendingDeletionRequest
                        });
                    }
                }, 50);
            };"""

if old_status_override in code:
    code = code.replace(old_status_override, new_status_override)
    print("✓ Injected instant direct cloud push inside setEmployeeDailyStatusOverride")

with open('e:/Antigravity projects/HR Admin/index.html', 'w', encoding='utf-8') as f:
    f.write(code)

with open('e:/Antigravity projects/HR Admin/نظام_ادراة_الملاك_v7.5_cloud.html', 'w', encoding='utf-8') as f:
    f.write(code)

print("✓ Completed instant cloud sync hardening!")
