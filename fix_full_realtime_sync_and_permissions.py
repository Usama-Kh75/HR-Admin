import os

with open('e:/Antigravity projects/HR Admin/index.html', 'r', encoding='utf-8') as f:
    code = f.read()

# 1. Update pushDataToCloud to take current state or payload and broadcast instantly
push_to_cloud_block = """            // بث التعديلات مباشرة إلى السحابة الحية لتنعكس لدى الجميع في نفس اللحظة
            const pushDataToCloud = async (bundle = null) => {
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
                        lastCloudUpdate: nowIso
                    };

                    const res = await fetch(FIREBASE_DB_URL, {
                        method: 'PUT',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify(dataPayload)
                    });
                    if (res.ok) {
                        setCloudSyncStatus({ connected: true, syncing: false, lastSync: new Date().toLocaleTimeString('ar-IQ') });
                    }
                } catch (err) {
                    console.warn("Could not push to Firebase Cloud:", err);
                }
            };"""

# 2. Add automatic cloud sync for dailyStatusOverrides, officialHolidays, hourlyLeaveRecords, overtimeHoursRecords
status_sync_effect = """            // حفظ وبث الموقف اليومي تلقائياً للسحابة الحية لتعميمه على كافة أجهزة وموبايلات الشعبة فورياً
            React.useEffect(() => {
                safeStorage.setItem('dailyStatusOverrides', JSON.stringify(dailyStatusOverrides));
                if (!isSyncingRef.current && (Object.keys(dailyStatusOverrides).length > 0 || staff.length > 0)) {
                    pushDataToCloud();
                }
            }, [dailyStatusOverrides]);

            // حفظ وبث الساعات الإضافية والإجازات الزمنية والعطل للسحابة فورياً
            React.useEffect(() => {
                safeStorage.setItem('officialHolidaysList', JSON.stringify(officialHolidays));
                safeStorage.setItem('hourlyLeaveRecords', JSON.stringify(hourlyLeaveRecords));
                safeStorage.setItem('overtimeHoursRecords', JSON.stringify(overtimeHoursRecords));
                if (!isSyncingRef.current && staff.length > 0) {
                    pushDataToCloud();
                }
            }, [officialHolidays, hourlyLeaveRecords, overtimeHoursRecords]);"""

old_daily_override_effect = """            React.useEffect(() => {
                safeStorage.setItem('dailyStatusOverrides', JSON.stringify(dailyStatusOverrides));
            }, [dailyStatusOverrides]);"""

if old_daily_override_effect in code:
    code = code.replace(old_daily_override_effect, status_sync_effect)
    print("✓ Added auto-broadcast for dailyStatusOverrides, holidays, and overtime to Firebase")

# 3. Enhance clearAllData permissions check
old_clear_data = """            const clearAllData = () => {
                const adminPin = prompt('🔐 يتطلب مسح جميع البيانات إدخال الرمز السري للإداري:');
                if (adminPin !== passwordsConfig.admin) {
                    alert('❌ الرمز السري غير صحيح! تم إلغاء العملية للحماية.');
                    return;
                }
                if (confirm('⚠️ هل أنت متأكد من مسح جميع البيانات؟\\n\\nسيتم حذف جميع الموظفين والعودة للنظام الفارغ.')) {
                    setStaff([]);
                    setView('dashboard');
                    alert('✅ تم مسح جميع البيانات بنجاح!');
                }
            };"""

new_clear_data = """            const clearAllData = () => {
                if (currentUserRole !== 'admin') {
                    alert('⛔ عذراً! صلاحية حذف وتفريغ قاعدة البيانات مقتصرة حصرياً على (👑 مدير النظام الرئيسي). لا يمكن للمُدخلين أو المستعرضين تنفيذ هذا الإجراء.');
                    return;
                }
                const adminPin = prompt('🔐 تأكيد الحذف: يرجى إدخال الرمز السري لمدير النظام الرئيسي:');
                if (adminPin !== passwordsConfig.admin) {
                    alert('❌ الرمز السري غير صحيح! تم إلغاء العملية للحماية والأمان.');
                    return;
                }
                if (confirm('⚠️ تحذير أمني شديد:\\n\\nهل أنت متأكد تماماً من رغبتك في مسح قاعدة البيانات بالكامل؟\\nسيتم تعميم الحذف سحابياً على جميع الأجهزة.')) {
                    setStaff([]);
                    setDailyStatusOverrides({});
                    setHourlyLeaveRecords({});
                    setOvertimeHoursRecords({});
                    setView('dashboard');
                    alert('✅ تم مسح قاعدة البيانات بنجاح من قبل مدير النظام.');
                }
            };"""

if old_clear_data in code:
    code = code.replace(old_clear_data, new_clear_data)
    print("✓ Restricted database clearing strictly to Master Admin (currentUserRole === 'admin')")

with open('e:/Antigravity projects/HR Admin/index.html', 'w', encoding='utf-8') as f:
    f.write(code)

with open('e:/Antigravity projects/HR Admin/نظام_ادراة_الملاك_v7.5_cloud.html', 'w', encoding='utf-8') as f:
    f.write(code)

print("✓ Updated index.html and standalone file with realtime status broadcast and RBAC enhancements")
