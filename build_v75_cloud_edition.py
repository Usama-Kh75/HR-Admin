import os

# Build v7.5 Cloud Edition with Firebase Realtime Cloud Sync Engine
with open('e:/Antigravity projects/HR Admin/index.html', 'r', encoding='utf-8') as f:
    code = f.read()

# Update version title and state to v7.5 Cloud Edition
code = code.replace('<title>نظام إدارة الملاك - الإصدار v7.0 Beta</title>', '<title>نظام إدارة الملاك - الإصدار v7.5 Cloud Edition ☁️</title>')
code = code.replace("version: 'v7.0 Beta',", "version: 'v7.5 Cloud Edition',")
code = code.replace('الإصدار v7.0 Beta', 'الإصدار v7.5 Cloud Edition')
code = code.replace('v7.0 Beta', 'v7.5 Cloud Edition')

# Inject Cloud Sync Manager & Firebase Realtime Database Engine
cloud_engine = """
            // ===== محرك المزامنة السحابية الحية (Firebase Cloud Realtime DB Engine) =====
            const CLOUD_DB_URL = "https://hr-admin-basra-default-rtdb.firebaseio.com/system_bundle.json";
            const [cloudSyncStatus, setCloudSyncStatus] = useState({ connected: false, syncing: false, lastSync: null });

            // دالة جلب البيانات السحابية الحية عند الفتح
            const fetchCloudData = async () => {
                try {
                    setCloudSyncStatus(prev => ({ ...prev, syncing: true }));
                    const res = await fetch(CLOUD_DB_URL);
                    if (res.ok) {
                        const data = await res.json();
                        if (data && typeof data === 'object') {
                            applyDataBundleToState(data);
                            setCloudSyncStatus({ connected: true, syncing: false, lastSync: new Date().toLocaleTimeString('ar-IQ') });
                            console.log("☁️ Data successfully synced from Cloud!");
                        }
                    } else {
                        setCloudSyncStatus(prev => ({ ...prev, connected: false, syncing: false }));
                    }
                } catch (err) {
                    console.warn("Cloud sync offline fallback active:", err);
                    setCloudSyncStatus(prev => ({ ...prev, connected: false, syncing: false }));
                }
            };

            // دالة بث وتحديث البيانات إلى السحابة فوراً
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

            // تشغيل الاستماع المباشر للسحابة عند فتح التطبيق
            React.useEffect(() => {
                fetchCloudData();
                // فحص دوري كل 15 ثانية للمزامنة السحابية اللحظية
                const interval = setInterval(fetchCloudData, 15000);
                return () => clearInterval(interval);
            }, []);
"""

if "const CLOUD_DB_URL =" not in code:
    code = code.replace("// ===== بث التحديثات إلى السيرفر المحلى =====", cloud_engine + "\n            // ===== بث التحديثات إلى السيرفر المحلى =====")
    print("✓ Injected Firebase Cloud Realtime DB Engine into App code")

# Write v7.5 Cloud Edition file
with open('e:/Antigravity projects/HR Admin/نظام_ادراة_الملاك_v7.5_cloud.html', 'w', encoding='utf-8') as f:
    f.write(code)

# Write index.html as main version
with open('e:/Antigravity projects/HR Admin/index.html', 'w', encoding='utf-8') as f:
    f.write(code)

print("✓ Successfully generated نظام_ادراة_الملاك_v7.5_cloud.html and updated index.html")
