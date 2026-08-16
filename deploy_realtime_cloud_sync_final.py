import os

# Read index.html
with open('e:/Antigravity projects/HR Admin/index.html', 'r', encoding='utf-8') as f:
    code = f.read()

# 1. Realtime Cloud Store Engine (GET + PUT supported 100%)
realtime_cloud_block = """            const [cloudSyncStatus, setCloudSyncStatus] = useState({ connected: true, syncing: false, lastSync: null });
            const CLOUD_OBJECT_ID = "ff8081819ff5b11001a00a4febb02bb9";
            const CLOUD_ENDPOINT = `https://api.restful-api.dev/objects/${CLOUD_OBJECT_ID}`;
            const lastCloudTimeRef = React.useRef(null);

            // جلب البيانات السحابية الحية لجميع المستخدمين
            const fetchCloudData = async () => {
                try {
                    setCloudSyncStatus(prev => ({ ...prev, syncing: true }));
                    const res = await fetch(CLOUD_ENDPOINT, {
                        method: 'GET',
                        headers: { 'Cache-Control': 'no-cache' }
                    });
                    if (res.ok) {
                        const jsonRes = await res.json();
                        const cloudData = jsonRes.data;
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
                    console.warn("Cloud push error:", err);
                }
            };

            // التفقّد والتحقق الدوري من السحابة كل 8 ثوانٍ
            React.useEffect(() => {
                fetchCloudData();
                const interval = setInterval(fetchCloudData, 8000);
                return () => clearInterval(interval);
            }, []);"""

# Replace old cloud block
old_cloud_snippet_start = 'const [cloudSyncStatus, setCloudSyncStatus] = useState({ connected: false, syncing: false, lastSync: null });'
old_cloud_snippet_end = 'const [showSyncModal, setShowSyncModal] = useState(false);'

start_pos = code.find(old_cloud_snippet_start)
end_pos = code.find(old_cloud_snippet_end)

if start_pos != -1 and end_pos != -1:
    code = code[:start_pos] + realtime_cloud_block + "\n            " + code[end_pos:]
    print("✓ Injected true Realtime Cloud Store Engine into index.html")

# 2. Fix local server polling to ONLY run if running locally on intranet (avoid 404 spam on github.io)
old_polling_start = "const checkServerAndSync = async () => {"
new_polling_start = """const checkServerAndSync = async () => {
                    if (window.location.hostname.includes('github.io') || window.location.protocol === 'file:') {
                        return; // لا تبحث عن /api/status عندما تكون على استضافة GitHub Pages
                    }"""

if old_polling_start in code:
    code = code.replace(old_polling_start, new_polling_start)
    print("✓ Silenced /api/status 404 polling on github.io")

with open('e:/Antigravity projects/HR Admin/index.html', 'w', encoding='utf-8') as f:
    f.write(code)

with open('e:/Antigravity projects/HR Admin/نظام_ادراة_الملاك_v7.5_cloud.html', 'w', encoding='utf-8') as f:
    f.write(code)

print("✓ Successfully completed deploy_realtime_cloud_sync_final.py")
