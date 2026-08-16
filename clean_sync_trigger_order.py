import os

with open('e:/Antigravity projects/HR Admin/index.html', 'r', encoding='utf-8') as f:
    code = f.read()

# Fix pushDataToServer to directly push to Firebase Cloud without attempting 405 /api/sync on github.io
old_push_fn = """            // بث التحديثات إلى السيرفر المحلي والسحابة الحية
            const pushDataToServer = async (customBundle = null) => {
                const bundle = customBundle || {
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
                    lastCloudUpdate: new Date().toISOString()
                };

                // بث إلى السيرفر المحلي في حال وجوده
                try {
                    const res = await fetch('/api/sync', {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify({ data: bundle })
                    });
                    if (res.ok) {
                        const resData = await res.json();
                        if (resData.success) {
                            serverVersionRef.current = resData.version;
                            setSyncStatus(prev => ({
                                ...prev,
                                connected: true,
                                version: resData.version,
                                lastUpdated: resData.last_updated
                            }));
                        }
                    }
                } catch (err) {
                    setSyncStatus(prev => ({ ...prev, connected: false }));
                }

                // بث إلى السحابة الحية دائماً (Firebase Cloud DB)
                try {
                    await pushDataToCloud(bundle);
                } catch (cErr) {
                    console.warn("Cloud push error:", cErr);
                }
            };"""

new_push_fn = """            // بث التحديثات إلى السيرفر المحلي والسحابة الحية
            const pushDataToServer = async (customBundle = null) => {
                const bundle = customBundle || {
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
                    lastCloudUpdate: new Date().toISOString()
                };

                // بث إلى السحابة الحية دائماً فوراً وبشكل أولي (Firebase Cloud DB)
                try {
                    await pushDataToCloud(bundle);
                } catch (cErr) {
                    console.warn("Cloud push error:", cErr);
                }

                // بث إلى السيرفر المحلي فقط في حال التشغيل على الشبكة المحلية
                if (!window.location.hostname.includes('github.io') && window.location.protocol !== 'file:') {
                    try {
                        const res = await fetch('/api/sync', {
                            method: 'POST',
                            headers: { 'Content-Type': 'application/json' },
                            body: JSON.stringify({ data: bundle })
                        });
                        if (res.ok) {
                            const resData = await res.json();
                            if (resData.success) {
                                serverVersionRef.current = resData.version;
                                setSyncStatus(prev => ({
                                    ...prev,
                                    connected: true,
                                    version: resData.version,
                                    lastUpdated: resData.last_updated
                                }));
                            }
                        }
                    } catch (err) {
                        setSyncStatus(prev => ({ ...prev, connected: false }));
                    }
                }
            };"""

if old_push_fn in code:
    code = code.replace(old_push_fn, new_push_fn)
    print("✓ Successfully prioritized pushDataToCloud before local server sync")

# Also auto-push to cloud on staff changes if staff length > 1
auto_push_code = """            // حفظ تلقائي عند تغيير البيانات وبثها للسحابة الحية
            React.useEffect(() => {
                if (staff.length > 1 && !isSyncingRef.current) {
                    safeStorage.setItem('staffData', JSON.stringify(staff));
                    pushDataToCloud();
                }
            }, [staff]);"""

old_auto_save = """            // حفظ تلقائي عند تغيير البيانات
            React.useEffect(() => {
                if (staff.length > 0) {
                    safeStorage.setItem('staffData', JSON.stringify(staff));
                }
            }, [staff]);"""

if old_auto_save in code:
    code = code.replace(old_auto_save, auto_push_code)
    print("✓ Injected auto-push to cloud on staff modification")

with open('e:/Antigravity projects/HR Admin/index.html', 'w', encoding='utf-8') as f:
    f.write(code)

with open('e:/Antigravity projects/HR Admin/نظام_ادراة_الملاك_v7.5_cloud.html', 'w', encoding='utf-8') as f:
    f.write(code)
