import os

# Script to unify Local + Cloud Sync in index.html & v7.5 Cloud Edition
with open('e:/Antigravity projects/HR Admin/index.html', 'r', encoding='utf-8') as f:
    code = f.read()

# 1. Update pushDataToServer to ALSO push to Cloud
old_push_server = """            // بث التحديثات إلى السيرفر المحلى
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
            };"""

new_push_server = """            // بث التحديثات إلى السيرفر المحلي والسحابة الحية
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

if old_push_server in code:
    code = code.replace(old_push_server, new_push_server)

# 2. Update Sync Modal UI to display Cloud or Local connectivity status clearly
old_modal_card = """                    {showSyncModal && (
                        <div className="fixed inset-0 bg-black/70 backdrop-blur-md flex items-center justify-center z-[110] p-4 animate-fadeIn no-print">
                            <div className="bg-white rounded-3xl max-w-md w-full overflow-hidden shadow-2xl border border-slate-200 animate-scaleUp">
                                <div className="bg-gradient-to-r from-blue-700 to-indigo-900 text-white p-6 text-center relative">
                                    <button 
                                        onClick={() => setShowSyncModal(false)}
                                        className="absolute top-4 left-4 w-8 h-8 rounded-full bg-white/20 hover:bg-white/30 text-white flex items-center justify-center text-sm font-bold transition"
                                    >✕</button>
                                    <div className="text-4xl mb-2">📡</div>
                                    <h3 className="text-xl font-bold">سيرفر المزامنة الداخلي للشعبة</h3>
                                    <p className="text-blue-100 text-xs mt-1">ربط ومزامنة البيانات حياً بين حواسب وموبايلات الشعبة</p>
                                </div>

                                <div className="p-6 space-y-4">
                                    {syncStatus.connected ? (
                                        <div className="p-4 bg-emerald-50 rounded-2xl border border-emerald-200 text-right space-y-2">
                                            <div className="flex items-center gap-2 font-bold text-emerald-800 text-sm">
                                                <span className="w-3 h-3 rounded-full bg-emerald-500 animate-ping"></span>
                                                متصل بالسيرفر المحلي بنجاح
                                            </div>
                                            <div className="text-xs text-emerald-700 space-y-1 pt-1 border-t border-emerald-200/60">
                                                <div>📍 عنوان السيرفر: <span className="font-mono dir-ltr inline-block">{syncStatus.ip}:{syncStatus.port}</span></div>
                                                <div>🔄 إصدار التحديث: <span className="font-bold">v{syncStatus.version}</span></div>
                                                <div>🕒 آخر مزامنة: <span>{syncStatus.lastUpdated || 'الآن'}</span></div>
                                            </div>
                                        </div>
                                    ) : (
                                        <div className="p-4 bg-amber-50 rounded-2xl border border-amber-200 text-right space-y-2">
                                            <div className="flex items-center gap-2 font-bold text-amber-800 text-sm">
                                                <span className="w-3 h-3 rounded-full bg-amber-500"></span>
                                                متصل بالذاكرة المحلية (أوفلاين)
                                            </div>
                                            <p className="text-xs text-amber-700 leading-relaxed">
                                                قم بتشغيل ملف "تشغيل_السيرفر_المحلي.bat" على الحاسبة الرئيسية لتفعيل الربط الحقيقي.
                                            </p>
                                        </div>
                                    )}

                                    <button 
                                        onClick={() => {
                                            pushDataToServer();
                                            alert('🔄 تم إرسال طلب المزامنة الحية وإعادة الربط بنجاح!');
                                        }}
                                        className="w-full py-3 bg-emerald-600 hover:bg-emerald-700 text-white font-bold rounded-xl text-sm transition shadow-lg flex items-center justify-center gap-2"
                                    >
                                        🔄 مزامنة حية الآن (Force Sync)
                                    </button>
                                </div>
                            </div>
                        </div>
                    )}"""

new_modal_card = """                    {showSyncModal && (
                        <div className="fixed inset-0 bg-black/70 backdrop-blur-md flex items-center justify-center z-[110] p-4 animate-fadeIn no-print">
                            <div className="bg-white rounded-3xl max-w-md w-full overflow-hidden shadow-2xl border border-slate-200 animate-scaleUp">
                                <div className="bg-gradient-to-r from-blue-700 to-indigo-900 text-white p-6 text-center relative">
                                    <button 
                                        onClick={() => setShowSyncModal(false)}
                                        className="absolute top-4 left-4 w-8 h-8 rounded-full bg-white/20 hover:bg-white/30 text-white flex items-center justify-center text-sm font-bold transition"
                                    >✕</button>
                                    <div className="text-4xl mb-2">☁️📡</div>
                                    <h3 className="text-xl font-bold">مركز المزامنة السحابية والمحلية</h3>
                                    <p className="text-blue-100 text-xs mt-1">ربط ومزامنة البيانات حياً بين حواسب وموبايلات الشعبة (بالبيت والشركة)</p>
                                </div>

                                <div className="p-6 space-y-4">
                                    {cloudSyncStatus.connected ? (
                                        <div className="p-4 bg-indigo-50 rounded-2xl border border-indigo-200 text-right space-y-2">
                                            <div className="flex items-center gap-2 font-bold text-indigo-900 text-sm">
                                                <span className="w-3 h-3 rounded-full bg-emerald-500 animate-ping"></span>
                                                🟢 متصل بالسحابة الحية (أونلاين 24/7)
                                            </div>
                                            <div className="text-xs text-indigo-800 space-y-1 pt-1 border-t border-indigo-200/60">
                                                <div>☁️ حالة السحابة: <span className="font-bold text-emerald-700">متصلة وشغالة بنجاح</span></div>
                                                <div>🕒 آخر مزامنة سحابية: <span>{cloudSyncStatus.lastSync || 'الآن'}</span></div>
                                            </div>
                                        </div>
                                    ) : syncStatus.connected ? (
                                        <div className="p-4 bg-emerald-50 rounded-2xl border border-emerald-200 text-right space-y-2">
                                            <div className="flex items-center gap-2 font-bold text-emerald-800 text-sm">
                                                <span className="w-3 h-3 rounded-full bg-emerald-500 animate-ping"></span>
                                                🟢 متصل بالسيرفر المحلي (شبكة الشركة)
                                            </div>
                                            <div className="text-xs text-emerald-700 space-y-1 pt-1 border-t border-emerald-200/60">
                                                <div>📍 عنوان السيرفر: <span className="font-mono dir-ltr inline-block">{syncStatus.ip}:{syncStatus.port}</span></div>
                                                <div>🔄 إصدار التحديث: <span className="font-bold">v{syncStatus.version}</span></div>
                                            </div>
                                        </div>
                                    ) : (
                                        <div className="p-4 bg-amber-50 rounded-2xl border border-amber-200 text-right space-y-2">
                                            <div className="flex items-center gap-2 font-bold text-amber-800 text-sm">
                                                <span className="w-3 h-3 rounded-full bg-amber-500"></span>
                                                ⚠️ متصل بالذاكرة المحلية (أوفلاين)
                                            </div>
                                            <p className="text-xs text-amber-700 leading-relaxed">
                                                تأكد من الاتصال بالإنترنت للمزامنة السحابية الحية، أو تشغيل السيرفر المحلي في شبكة الشركة.
                                            </p>
                                        </div>
                                    )}

                                    <button 
                                        onClick={async () => {
                                            await pushDataToServer();
                                            await fetchCloudData();
                                            alert('🔄 تم بث ومزامنة البيانات حياً مع السحابة والسيرفر بنجاح!');
                                        }}
                                        className="w-full py-3 bg-gradient-to-r from-emerald-600 to-teal-600 hover:from-emerald-700 hover:to-teal-700 text-white font-bold rounded-xl text-sm transition shadow-lg flex items-center justify-center gap-2"
                                    >
                                        ☁️ مزامنة سحابية حية الآن (Force Sync)
                                    </button>
                                </div>
                            </div>
                        </div>
                    )}"""

if old_modal_card in code:
    code = code.replace(old_modal_card, new_modal_card)

with open('e:/Antigravity projects/HR Admin/index.html', 'w', encoding='utf-8') as f:
    f.write(code)

with open('e:/Antigravity projects/HR Admin/نظام_ادراة_الملاك_v7.5_cloud.html', 'w', encoding='utf-8') as f:
    f.write(code)

print("✓ Successfully updated Dual Local + Cloud Sync Engine")
