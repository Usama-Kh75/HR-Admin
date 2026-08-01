import os
import re

def update_file(file_path):
    if not os.path.exists(file_path):
        print(f"File not found: {file_path}")
        return False

    with open(file_path, 'r', encoding='utf-8') as f:
        code = f.read()

    # 1. Inject Sync States and Engine after officialHolidays/hourlyLeaveRecords states
    target_state_anchor = "const [officialHolidays, setOfficialHolidays] = useState(() => {"
    
    sync_engine_code = """// ----------------------------------------------------
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
                        shiftAnchorDate: shiftAnchorDate,
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
            }, [staff, officialHolidays, hourlyLeaveRecords, overtimeHoursRecords, dailyStatusOverrides, shiftAnchorDate, dataEntryOperator]);

            """

    if target_state_anchor in code and "Local Live Sync Engine" not in code:
        code = code.replace(target_state_anchor, sync_engine_code + target_state_anchor)
        print(f"✓ Injected sync engine into {file_path}")

    # 2. Update Header Status Badge to be interactive and reflect Local Server Sync
    old_badge = """                            <div className="flex items-center gap-2 bg-green-950/45 px-3 py-1.5 rounded-full border border-green-400/20 shadow-inner flex-shrink-0 relative">
                                <span className="relative flex h-2 w-2">
                                    <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-green-400 opacity-75"></span>
                                    <span className="relative inline-flex rounded-full h-2 w-2 bg-green-500"></span>
                                </span>
                                <span className="text-[10px] uppercase tracking-wider font-extrabold text-green-300">النظام نشط</span>
                            </div>"""

    new_badge = """                            <div 
                                onClick={() => setShowSyncModal(true)}
                                className={`flex items-center gap-2 px-3.5 py-1.5 rounded-full border cursor-pointer transition shadow-md flex-shrink-0 ${
                                    syncStatus.connected 
                                        ? 'bg-emerald-950/70 border-emerald-400/40 text-emerald-200 hover:bg-emerald-900/80' 
                                        : 'bg-amber-950/70 border-amber-400/30 text-amber-200 hover:bg-amber-900/80'
                                }`}
                                title="اضغط لعرض تفاصيل المزامنة ورابط أجهزة الشعبة"
                            >
                                <span className="relative flex h-2.5 w-2.5">
                                    {syncStatus.connected ? (
                                        <>
                                            <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-emerald-400 opacity-75"></span>
                                            <span className="relative inline-flex rounded-full h-2.5 w-2.5 bg-emerald-500"></span>
                                        </>
                                    ) : (
                                        <span className="relative inline-flex rounded-full h-2.5 w-2.5 bg-amber-500"></span>
                                    )}
                                </span>
                                <span className="text-xs font-bold">
                                    {syncStatus.connected ? `🟢 السيرفر المحلي نشط (${syncStatus.ip || 'Local'})` : '🟡 أوفلاين محلي'}
                                </span>
                            </div>"""

    if old_badge in code:
        code = code.replace(old_badge, new_badge)
        print(f"✓ Injected header badge into {file_path}")

    # 3. Inject Sync Modal HTML
    sync_modal_code = """
            {/* نافذة تفاصيل المزامنة السحابية والمحلية لشعبة تبريد المركز */}
            {showSyncModal && (
                <div className="fixed inset-0 bg-slate-950/70 backdrop-blur-sm z-50 flex items-center justify-center p-4">
                    <div className="bg-white rounded-3xl shadow-2xl border border-slate-100 max-w-lg w-full overflow-hidden animate-fadeInUp">
                        {/* رأس النافذة */}
                        <div className="bg-gradient-to-r from-blue-700 via-indigo-700 to-slate-900 p-6 text-white relative">
                            <button 
                                onClick={() => setShowSyncModal(false)}
                                className="absolute top-4 left-4 bg-white/10 hover:bg-white/20 w-8 h-8 rounded-full flex items-center justify-center text-white font-bold transition"
                            >
                                ✕
                            </button>
                            <div className="flex items-center gap-3">
                                <span className="text-3xl">📡</span>
                                <div>
                                    <h3 className="text-xl font-black">سيرفر المزامنة الداخلي للشعبة</h3>
                                    <p className="text-xs text-blue-200 mt-0.5">ربط ومزامنة البيانات حياً بين حواسب وموبايلات الشعبة</p>
                                </div>
                            </div>
                        </div>

                        {/* محتوى النافذة */}
                        <div className="p-6 space-y-5">
                            {/* بطاقة حالة الاتصال */}
                            <div className={`p-4 rounded-2xl border flex items-center gap-4 ${
                                syncStatus.connected 
                                    ? 'bg-emerald-50 border-emerald-200 text-emerald-900' 
                                    : 'bg-amber-50 border-amber-200 text-amber-900'
                            }`}>
                                <div className={`w-4 h-4 rounded-full flex-shrink-0 animate-pulse ${
                                    syncStatus.connected ? 'bg-emerald-500' : 'bg-amber-500'
                                }`} />
                                <div>
                                    <div className="font-extrabold text-sm">
                                        {syncStatus.connected ? '✅ السيرفر المحلي متصل ويعمل حياً' : '⚠️ متصل بالذاكرة المحلية (أوفلاين)'}
                                    </div>
                                    <div className="text-xs opacity-80 mt-0.5">
                                        {syncStatus.connected 
                                            ? `آخر تحديث تم بثه: ${syncStatus.lastUpdated || 'الآن'} (إصدار البيانات v${syncStatus.version})`
                                            : 'قم بتشغيل ملف "تشغيل_السيرفر_المحلي.bat" على الحاسبة الرئيسية لتفعيل الربط الحقيقي.'}
                                    </div>
                                </div>
                            </div>

                            {/* رابط أجهزة الشعبة */}
                            {syncStatus.connected && (
                                <div className="space-y-2 bg-slate-50 p-4 rounded-2xl border border-slate-200">
                                    <label className="text-xs font-bold text-slate-700 block">
                                        🔗 رابط النظام لأجهزة وموبايلات الشعبة الأخرى:
                                    </label>
                                    <div className="flex items-center gap-2">
                                        <input 
                                            type="text" 
                                            readOnly 
                                            value={`http://${syncStatus.ip}:${syncStatus.port}`}
                                            className="w-full bg-white border border-slate-300 rounded-xl px-3 py-2 text-xs font-mono font-bold text-blue-800 text-center select-all"
                                        />
                                        <button 
                                            onClick={() => {
                                                navigator.clipboard.writeText(`http://${syncStatus.ip}:${syncStatus.port}`);
                                                alert('✅ تم نسخ رابط الشعبة بنجاح!');
                                            }}
                                            className="px-4 py-2 bg-blue-600 hover:bg-blue-700 text-white rounded-xl text-xs font-bold whitespace-nowrap shadow transition"
                                        >
                                            📋 نسخ الرابط
                                        </button>
                                    </div>
                                    <p className="text-[11px] text-slate-500 text-right">
                                        * افتح هذا الرابط في أي مبايل أو حاسبة متصلة بنفس راوتر الشعبة لقراءة وتحديث البيانات حياً.
                                    </p>
                                </div>
                            )}

                            {/* أزرار التحكم والإجراءات */}
                            <div className="flex items-center justify-between gap-3 pt-2">
                                <button
                                    onClick={() => {
                                        pushDataToServer();
                                        alert('🔄 تم بث وتعميم البيانات الحالية للسيرفر بنجاح!');
                                    }}
                                    className="flex-1 py-3 bg-gradient-to-r from-emerald-600 to-teal-600 hover:from-emerald-700 hover:to-teal-700 text-white font-bold rounded-2xl text-xs shadow-md transition flex items-center justify-center gap-2"
                                >
                                    <span>🔄</span>
                                    <span>مزامنة حية الآن (Force Sync)</span>
                                </button>
                                <button
                                    onClick={() => setShowSyncModal(false)}
                                    className="px-6 py-3 bg-slate-100 hover:bg-slate-200 text-slate-700 font-bold rounded-2xl text-xs transition"
                                >
                                    إغلاق
                                </button>
                            </div>
                        </div>
                    </div>
                </div>
            )}
    """

    # Inject before the closing tag of StaffSystem (or before </main> or end of return)
    modal_injection_anchor = "{/* تنبيه النسخ الاحتياطي التلقائي */}"
    if modal_injection_anchor in code and "سيرفر المزامنة الداخلي للشعبة" not in code:
        code = code.replace(modal_injection_anchor, sync_modal_code + "\n\n                                " + modal_injection_anchor)
        print(f"✓ Injected sync modal into {file_path}")

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(code)
    return True

if __name__ == '__main__':
    update_file('e:/Antigravity projects/HR Admin/index.html')
    update_file('e:/Antigravity projects/HR Admin/نظام_ادراة_الملاك_v6.8_online.html')
    update_file('e:/Antigravity projects/HR Admin/نظام_ادراة_الملاك_v6.8.html')
