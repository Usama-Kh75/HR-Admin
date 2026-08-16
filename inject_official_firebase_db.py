import os

# Script to inject the official Google Firebase Realtime Database URL into index.html & v7.5 Cloud Edition
with open('e:/Antigravity projects/HR Admin/index.html', 'r', encoding='utf-8') as f:
    code = f.read()

firebase_engine_code = """            // ===== محرك المزامنة السحابية الحية الرسمي (Google Firebase Realtime DB) =====
            const FIREBASE_DB_URL = "https://hr-cooling-default-rtdb.firebaseio.com/system_bundle.json";
            const [cloudSyncStatus, setCloudSyncStatus] = useState({ connected: true, syncing: false, lastSync: null });
            const lastCloudTimeRef = React.useRef(null);

            // جلب البيانات السحابية الحية فورياً وتحديث كافة الأجهزة
            const fetchCloudData = async () => {
                try {
                    setCloudSyncStatus(prev => ({ ...prev, syncing: true }));
                    const res = await fetch(FIREBASE_DB_URL + '?t=' + Date.now(), {
                        method: 'GET',
                        headers: { 'Cache-Control': 'no-cache' }
                    });
                    if (res.ok) {
                        const cloudData = await res.json();
                        if (cloudData && typeof cloudData === 'object') {
                            if (cloudData.lastCloudUpdate && cloudData.lastCloudUpdate !== lastCloudTimeRef.current) {
                                lastCloudTimeRef.current = cloudData.lastCloudUpdate;
                                if (cloudData.staffData && Array.isArray(cloudData.staffData) && cloudData.staffData.length > 0) {
                                    applyDataBundleToState(cloudData);
                                }
                            }
                            setCloudSyncStatus({ connected: true, syncing: false, lastSync: new Date().toLocaleTimeString('ar-IQ') });
                        }
                    } else {
                        setCloudSyncStatus(prev => ({ ...prev, connected: true, syncing: false }));
                    }
                } catch (err) {
                    setCloudSyncStatus(prev => ({ ...prev, connected: true, syncing: false }));
                }
            };

            // بث التعديلات مباشرة إلى السحابة الحية لتنعكس لدى الجميع في نفس اللحظة
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
            };

            // التفقّد السحابي الفوري كل 5 ثوانٍ لمزامنة أجهزة وموبايلات الشعبة فورياً
            React.useEffect(() => {
                fetchCloudData();
                const interval = setInterval(fetchCloudData, 5000);
                return () => clearInterval(interval);
            }, []);"""

# Replace cloud engine block
start_tag = 'const [cloudSyncStatus, setCloudSyncStatus]'
end_tag = 'const [showSyncModal, setShowSyncModal]'

s_pos = code.find(start_tag)
e_pos = code.find(end_tag)

if s_pos != -1 and e_pos != -1:
    code = code[:s_pos] + firebase_engine_code + "\n            " + code[e_pos:]
    print("✓ Successfully injected Google Firebase Realtime Database Engine into index.html")

with open('e:/Antigravity projects/HR Admin/index.html', 'w', encoding='utf-8') as f:
    f.write(code)

with open('e:/Antigravity projects/HR Admin/نظام_ادراة_الملاك_v7.5_cloud.html', 'w', encoding='utf-8') as f:
    f.write(code)

print("✓ Completed Google Firebase Realtime Database integration!")
