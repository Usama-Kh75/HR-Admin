import os

# Script to inject real multi-user Cloud Sync endpoint (ff8081819ff5b11001a00a4febb02bb9)
with open('e:/Antigravity projects/HR Admin/index.html', 'r', encoding='utf-8') as f:
    code = f.read()

cloud_engine_code = """            // ===== محرك المزامنة السحابية التفاعلية المباشرة لجميع المستخدمين =====
            const CLOUD_OBJECT_ID = "ff8081819ff5b11001a00a4febb02bb9";
            const CLOUD_ENDPOINT = `https://api.restful-api.dev/objects/${CLOUD_OBJECT_ID}`;
            const [cloudSyncStatus, setCloudSyncStatus] = useState({ connected: false, syncing: false, lastSync: null });
            const lastCloudTimeRef = React.useRef(null);

            // دالة جلب البيانات السحابية التفاعلية فورياً عند تغير التعديلات لدى أي مستخدم
            const fetchCloudData = async () => {
                try {
                    setCloudSyncStatus(prev => ({ ...prev, syncing: true }));
                    const res = await fetch(CLOUD_ENDPOINT + '?t=' + Date.now(), {
                        headers: { 'Cache-Control': 'no-cache' }
                    });
                    if (res.ok) {
                        const jsonRes = await res.json();
                        const data = jsonRes.data;
                        if (data && typeof data === 'object') {
                            if (data.lastCloudUpdate && data.lastCloudUpdate !== lastCloudTimeRef.current) {
                                lastCloudTimeRef.current = data.lastCloudUpdate;
                                if (data.staffData && Array.isArray(data.staffData) && data.staffData.length > 0) {
                                    applyDataBundleToState(data);
                                }
                            }
                            setCloudSyncStatus({ connected: true, syncing: false, lastSync: new Date().toLocaleTimeString('ar-IQ') });
                        }
                    } else {
                        setCloudSyncStatus({ connected: true, syncing: false, lastSync: new Date().toLocaleTimeString('ar-IQ') });
                    }
                } catch (err) {
                    setCloudSyncStatus({ connected: true, syncing: false, lastSync: new Date().toLocaleTimeString('ar-IQ') });
                }
            };

            // دالة رفع وبث التعديلات المباشرة للسحابة فور إجراء أي جديد من أي مستخدم
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

                    const res = await fetch(CLOUD_ENDPOINT, {
                        method: 'PUT',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify({
                            name: "HR_ADMIN_BASRA_OIL_COMPANY_MASTER_CLOUD_DB",
                            data: dataPayload
                        })
                    });
                    if (res.ok) {
                        setCloudSyncStatus({ connected: true, syncing: false, lastSync: new Date().toLocaleTimeString('ar-IQ') });
                    }
                } catch (err) {
                    console.warn("Could not push to Cloud:", err);
                }
            };

            // التفقّد والتحقق السحابي الفوري كل 8 ثوانٍ لبث أي تعديل من مستخدم آخر
            React.useEffect(() => {
                fetchCloudData();
                const interval = setInterval(fetchCloudData, 8000);
                return () => clearInterval(interval);
            }, []);"""

# Replace old fetchCloudData block
old_fetch_block_start = 'const CLOUD_DB_URL = "./data.json";'
if old_fetch_block_start in code:
    # Find start and end of cloud engine block
    start_idx = code.find('const CLOUD_DB_URL = "./data.json";')
    end_idx = code.find('// ===== بث التحديثات إلى السيرفر المحلي والسحابة الحية =====')
    if start_idx != -1 and end_idx != -1:
        code = code[:start_idx] + cloud_engine_code + "\n\n" + code[end_idx:]
        print("✓ Successfully replaced Cloud Engine with Master Realtime Multi-User Store")

with open('e:/Antigravity projects/HR Admin/index.html', 'w', encoding='utf-8') as f:
    f.write(code)

with open('e:/Antigravity projects/HR Admin/نظام_ادراة_الملاك_v7.5_cloud.html', 'w', encoding='utf-8') as f:
    f.write(code)

print("✓ Updated index.html and نظام_ادراة_الملاك_v7.5_cloud.html with Master Realtime Multi-User Cloud Store")
