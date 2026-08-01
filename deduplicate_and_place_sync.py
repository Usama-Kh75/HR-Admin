import re
import os

def clean_file(file_path):
    if not os.path.exists(file_path):
        return
    with open(file_path, 'r', encoding='utf-8') as f:
        code = f.read()

    # Define the canonical single Sync Engine code block
    sync_engine_block = """
            // ----------------------------------------------------
            // محرك المزامنة حياً مع السيرفر المحلي للشعبة (Local Live Sync Engine)
            // ----------------------------------------------------
            const [syncStatus, setSyncStatus] = useState({
                connected: false,
                ip: '',
                port: 8000,
                version: 0,
                lastUpdated: '',
                isSyncing: false
            });
            const [showSyncModal, setShowSyncModal] = useState(false);
            const serverVersionRef = React.useRef(0);
            const isSyncingRef = React.useRef(false);

            // بث التحديثات إلى السيرفر المحلى
            const pushDataToServer = async (customBundle = null) => {
                try {
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
                        overtimeSelectedIds: overtimeIds
                    };
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
            };

            // تطبيق حزمة البيانات المجلوبة من السيرفر على React State
            const applyDataBundleToState = (bundle) => {
                if (!bundle || typeof bundle !== 'object') return;
                isSyncingRef.current = true;
                if (bundle.staffData && Array.isArray(bundle.staffData)) {
                    setStaff(bundle.staffData);
                    localStorage.setItem('staffData', JSON.stringify(bundle.staffData));
                }
                if (bundle.officialHolidaysList && Array.isArray(bundle.officialHolidaysList)) {
                    setOfficialHolidays(bundle.officialHolidaysList);
                    localStorage.setItem('officialHolidaysList', JSON.stringify(bundle.officialHolidaysList));
                }
                if (bundle.hourlyLeaveRecords) {
                    setHourlyLeaveRecords(bundle.hourlyLeaveRecords);
                    localStorage.setItem('hourlyLeaveRecords', JSON.stringify(bundle.hourlyLeaveRecords));
                }
                if (bundle.overtimeHoursRecords) {
                    setOvertimeHoursRecords(bundle.overtimeHoursRecords);
                    localStorage.setItem('overtimeHoursRecords', JSON.stringify(bundle.overtimeHoursRecords));
                }
                if (bundle.dailyStatusOverrides) {
                    setDailyStatusOverrides(bundle.dailyStatusOverrides);
                    localStorage.setItem('dailyStatusOverrides', JSON.stringify(bundle.dailyStatusOverrides));
                }
                if (bundle.shiftAnchorDate) {
                    setAnchorDate(bundle.shiftAnchorDate);
                    localStorage.setItem('shiftAnchorDate', bundle.shiftAnchorDate);
                }
                if (bundle.threeShiftAnchorSquad) {
                    setThreeShiftAnchorSquad(bundle.threeShiftAnchorSquad);
                    localStorage.setItem('threeShiftAnchorSquad', bundle.threeShiftAnchorSquad);
                }
                if (bundle.twoShiftAnchorSquad) {
                    setTwoShiftAnchorSquad(bundle.twoShiftAnchorSquad);
                    localStorage.setItem('twoShiftAnchorSquad', bundle.twoShiftAnchorSquad);
                }
                if (bundle.dataEntryOperator) {
                    setDataEntryOperator(bundle.dataEntryOperator);
                    localStorage.setItem('dataEntryOperator', bundle.dataEntryOperator);
                }
                if (bundle.overtimeSelectedIds) {
                    setOvertimeIds(bundle.overtimeSelectedIds);
                    localStorage.setItem('overtimeSelectedIds', JSON.stringify(bundle.overtimeSelectedIds));
                }
                setTimeout(() => { isSyncingRef.current = false; }, 500);
            };

            // المزامنة التلقائية والفحص الدوري (Polling) كل 3 ثوانٍ
            React.useEffect(() => {
                let isMounted = true;
                const checkServerAndSync = async () => {
                    try {
                        const statusRes = await fetch('/api/status?t=' + Date.now());
                        if (statusRes.ok) {
                            const statusJson = await statusRes.json();
                            if (!isMounted) return;
                            
                            setSyncStatus(prev => ({
                                ...prev,
                                connected: true,
                                ip: statusJson.ip,
                                port: statusJson.port,
                                version: statusJson.version,
                                lastUpdated: statusJson.last_updated
                            }));

                            if (statusJson.version > serverVersionRef.current) {
                                const syncRes = await fetch('/api/sync?t=' + Date.now());
                                if (syncRes.ok) {
                                    const syncJson = await syncRes.json();
                                    serverVersionRef.current = syncJson.version;
                                    if (syncJson.data && Object.keys(syncJson.data).length > 0) {
                                        applyDataBundleToState(syncJson.data);
                                    } else {
                                        pushDataToServer();
                                    }
                                }
                            }
                        } else {
                            if (isMounted) setSyncStatus(prev => ({ ...prev, connected: false }));
                        }
                    } catch (e) {
                        if (isMounted) setSyncStatus(prev => ({ ...prev, connected: false }));
                    }
                };

                checkServerAndSync();
                const interval = setInterval(checkServerAndSync, 3000);
                return () => {
                    isMounted = false;
                    clearInterval(interval);
                };
            }, []);

            // بث التغييرات عند تعديل أي بيانات في النظام
            React.useEffect(() => {
                if (!isSyncingRef.current && syncStatus.connected) {
                    pushDataToServer();
                }
            }, [staff, officialHolidays, hourlyLeaveRecords, overtimeHoursRecords, dailyStatusOverrides, anchorDate, dataEntryOperator]);
"""

    # 1. Remove all existing sync blocks using regex
    pattern = r"// ----------------------------------------------------\s+// محرك المزامنة حياً مع السيرفر المحلي للشعبة \(Local Live Sync Engine\).*?pushDataToServer\(\);\s+\}\s+\}, \[.*?\]\);"
    code = re.sub(pattern, "", code, flags=re.DOTALL)

    # 2. Find insertion anchor: AFTER anchorDate, threeShiftAnchorSquad, twoShiftAnchorSquad, dailyReportDate state declarations!
    insertion_anchor = "localStorage.setItem('twoShiftAnchorSquad', twoShiftAnchorSquad);\n            }, [anchorDate, threeShiftAnchorSquad, twoShiftAnchorSquad]);"

    if insertion_anchor in code:
        code = code.replace(insertion_anchor, insertion_anchor + "\n" + sync_engine_block)
        print(f"✓ Inserted single clean sync engine block in {file_path}")
    else:
        print(f"Insertion anchor not found in {file_path}")

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(code)

if __name__ == '__main__':
    clean_file('e:/Antigravity projects/HR Admin/index.html')
    clean_file('e:/Antigravity projects/HR Admin/نظام_ادراة_الملاك_v6.8_online.html')
    clean_file('e:/Antigravity projects/HR Admin/نظام_ادراة_الملاك_v6.8.html')
