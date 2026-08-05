import os

# Script to inject cloudSyncStatus state and safe checks cleanly into index.html
with open('e:/Antigravity projects/HR Admin/index.html', 'r', encoding='utf-8') as f:
    code = f.read()

# 1. Inject cloudSyncStatus state right after syncStatus
state_injection = """            const [syncStatus, setSyncStatus] = useState({
                connected: false,
                ip: '',
                port: 8000,
                version: 0,
                lastUpdated: '',
                isSyncing: false
            });
            const [cloudSyncStatus, setCloudSyncStatus] = useState({ connected: false, syncing: false, lastSync: null });
            const CLOUD_DB_URL = "https://hr-admin-basra-default-rtdb.firebaseio.com/system_bundle.json";

            const fetchCloudData = async () => {
                try {
                    setCloudSyncStatus(prev => ({ ...prev, syncing: true }));
                    const res = await fetch(CLOUD_DB_URL);
                    if (res.ok) {
                        const data = await res.json();
                        if (data && typeof data === 'object') {
                            applyDataBundleToState(data);
                            setCloudSyncStatus({ connected: true, syncing: false, lastSync: new Date().toLocaleTimeString('ar-IQ') });
                        }
                    } else {
                        setCloudSyncStatus(prev => ({ ...prev, connected: false, syncing: false }));
                    }
                } catch (err) {
                    setCloudSyncStatus(prev => ({ ...prev, connected: false, syncing: false }));
                }
            };

            const pushDataToCloud = async (bundle = null) => {
                try {
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
                        lastCloudUpdate: new Date().toISOString()
                    };
                    const res = await fetch(CLOUD_DB_URL, {
                        method: 'PUT',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify(dataPayload)
                    });
                    if (res.ok) {
                        setCloudSyncStatus({ connected: true, syncing: false, lastSync: new Date().toLocaleTimeString('ar-IQ') });
                    }
                } catch (err) {
                    console.warn("Could not push to Cloud:", err);
                }
            };

            React.useEffect(() => {
                fetchCloudData();
                const interval = setInterval(fetchCloudData, 15000);
                return () => clearInterval(interval);
            }, []);"""

if "const [cloudSyncStatus, setCloudSyncStatus]" not in code:
    code = code.replace("""            const [syncStatus, setSyncStatus] = useState({
                connected: false,
                ip: '',
                port: 8000,
                version: 0,
                lastUpdated: '',
                isSyncing: false
            });""", state_injection)
    print("✓ Successfully injected cloudSyncStatus state and cloud sync hooks")

# 2. Add defensive checks on cloudSyncStatus in JSX rendering
code = code.replace(
    "{cloudSyncStatus.connected || syncStatus.connected ?",
    "{(typeof cloudSyncStatus !== 'undefined' && cloudSyncStatus && cloudSyncStatus.connected) || syncStatus.connected ?"
)

code = code.replace(
    "{cloudSyncStatus.connected ? '☁️ متصل بالسحابة الحية (أونلاين 24/7)' :",
    "{(typeof cloudSyncStatus !== 'undefined' && cloudSyncStatus && cloudSyncStatus.connected) ? '☁️ متصل بالسحابة الحية (أونلاين 24/7)' :"
)

with open('e:/Antigravity projects/HR Admin/index.html', 'w', encoding='utf-8') as f:
    f.write(code)

with open('e:/Antigravity projects/HR Admin/نظام_ادراة_الملاك_v7.5_cloud.html', 'w', encoding='utf-8') as f:
    f.write(code)

print("✓ Fixed cloudSyncStatus ReferenceError cleanly across all HTML files")
