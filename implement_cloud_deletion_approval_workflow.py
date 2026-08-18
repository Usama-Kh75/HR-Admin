import os

with open('e:/Antigravity projects/HR Admin/index.html', 'r', encoding='utf-8') as f:
    code = f.read()

# 1. Add pendingDeletionRequest state
state_search = "const [currentUserRole, setCurrentUserRole] = useState(null);"
state_replace = """const [currentUserRole, setCurrentUserRole] = useState(null);
            const [pendingDeletionRequest, setPendingDeletionRequest] = useState(() => {
                const saved = safeStorage.getItem('pendingDeletionRequest');
                return saved ? JSON.parse(saved) : null;
            });
            React.useEffect(() => {
                if (pendingDeletionRequest) {
                    safeStorage.setItem('pendingDeletionRequest', JSON.stringify(pendingDeletionRequest));
                } else {
                    safeStorage.removeItem('pendingDeletionRequest');
                }
            }, [pendingDeletionRequest]);"""

if state_search in code:
    code = code.replace(state_search, state_replace, 1)
    print("✓ Added pendingDeletionRequest state")

# 2. Update applyDataBundleToState to parse pendingDeletionRequest
apply_search = "if (bundle.overtimeSelectedIds) {"
apply_replace = """if (bundle.pendingDeletionRequest !== undefined) {
                    setPendingDeletionRequest(bundle.pendingDeletionRequest);
                    if (bundle.pendingDeletionRequest) {
                        safeStorage.setItem('pendingDeletionRequest', JSON.stringify(bundle.pendingDeletionRequest));
                    } else {
                        safeStorage.removeItem('pendingDeletionRequest');
                    }
                }
                if (bundle.overtimeSelectedIds) {"""

if apply_search in code:
    code = code.replace(apply_search, apply_replace, 1)
    print("✓ Added pendingDeletionRequest to applyDataBundleToState")

# 3. Update pushDataToCloud payload to include pendingDeletionRequest
push_payload_search = "lastCloudUpdate: nowIso"
push_payload_replace = """lastCloudUpdate: nowIso,
                        pendingDeletionRequest: pendingDeletionRequest"""

if push_payload_search in code:
    code = code.replace(push_payload_search, push_payload_replace)
    print("✓ Added pendingDeletionRequest to pushDataToCloud payloads")

# 4. Update clearAllData function with Interactive Request / Approval Workflow
old_clear_fn_start = "const clearAllData = () => {"
old_clear_fn_end = "alert('✅ تم مسح قاعدة البيانات بنجاح من قبل مدير النظام.');\n                }\n            };"

clear_workflow_fn = """const clearAllData = () => {
                if (currentUserRole !== 'admin') {
                    // مسار الإداري المُدخل: تقديم طلب حذف رسمي لمدير النظام
                    const reason = prompt('📝 تقديم طلب حذف رسمي لمدير النظام:\\n\\nيرجى كتابة سبب طلب حذف أو تفريغ قاعدة البيانات ليتم إرسال إشعار للموافقة:');
                    if (!reason || !reason.trim()) {
                        alert('⚠️ تم إلغاء الطلب: يجب كتابة سبب الحذف.');
                        return;
                    }
                    const newRequest = {
                        id: 'del_req_' + Date.now(),
                        requestedBy: dataEntryOperator || 'الإداري المُدخل',
                        reason: reason.trim(),
                        timestamp: new Date().toLocaleString('ar-IQ'),
                        status: 'pending'
                    };
                    setPendingDeletionRequest(newRequest);
                    safeStorage.setItem('pendingDeletionRequest', JSON.stringify(newRequest));
                    pushDataToCloud({
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
                        lastCloudUpdate: new Date().toISOString(),
                        pendingDeletionRequest: newRequest
                    });
                    alert('📨 تم إرسال طلب الحذف بنجاح إلى (👑 مدير النظام الرئيسي)!\\n\\nستصل رسالة لمدير النظام، وبمجرد موافقته سيتم تفريغ القاعدة سحابياً.');
                    return;
                }

                // مسار مدير النظام المباشر
                const adminPin = prompt('🔐 تأكيد الحذف المباشر: يرجى إدخال الرمز السري لمدير النظام:');
                if (adminPin !== passwordsConfig.admin) {
                    alert('❌ الرمز السري غير صحيح! تم إلغاء العملية للحماية والأمان.');
                    return;
                }
                if (confirm('⚠️ تحذير أمني:\\n\\nهل أنت متأكد تماماً من تفريغ ومسح قاعدة البيانات بالكامل؟\\nسيتم تعميم المسح سحابياً على جميع أجهزة الشعبة.')) {
                    executeCompleteDatabaseWipe();
                }
            };

            // دالة التنفيذ الفعلي لمسح وتفريغ قاعدة البيانات
            const executeCompleteDatabaseWipe = () => {
                setStaff([]);
                setDailyStatusOverrides({});
                setHourlyLeaveRecords({});
                setOvertimeHoursRecords({});
                setPendingDeletionRequest(null);
                safeStorage.setItem('staffData', JSON.stringify([]));
                safeStorage.setItem('dailyStatusOverrides', JSON.stringify({}));
                safeStorage.removeItem('pendingDeletionRequest');
                pushDataToCloud({
                    staffData: [],
                    officialHolidaysList: officialHolidays,
                    hourlyLeaveRecords: {},
                    overtimeHoursRecords: {},
                    dailyStatusOverrides: {},
                    shiftAnchorDate: anchorDate,
                    threeShiftAnchorSquad: threeShiftAnchorSquad,
                    twoShiftAnchorSquad: twoShiftAnchorSquad,
                    dataEntryOperator: dataEntryOperator,
                    overtimeSelectedIds: [],
                    lastCloudUpdate: new Date().toISOString(),
                    pendingDeletionRequest: null
                });
                setView('dashboard');
                alert('✅ تم مسح وتفريغ قاعدة البيانات بنجاح وتعميم ذلك سحابياً على كافة الأجهزة.');
            };

            // دالة رفض طلب الحذف من قبل مدير النظام
            const rejectDeletionRequest = () => {
                setPendingDeletionRequest(null);
                safeStorage.removeItem('pendingDeletionRequest');
                pushDataToCloud({
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
                    lastCloudUpdate: new Date().toISOString(),
                    pendingDeletionRequest: null
                });
                alert('❌ تم رفض وإلغاء طلب الحذف.');
            };"""

s_idx = code.find(old_clear_fn_start)
e_idx = code.find(old_clear_fn_end)
if s_idx != -1 and e_idx != -1:
    code = code[:s_idx] + clear_workflow_fn + code[e_idx + len(old_clear_fn_end):]
    print("✓ Replaced clearAllData with Interactive Request & Approval Workflow")

# 5. Add notification banner for pending deletion requests in UI
banner_jsx = """            {/* إشعار طلب الحذف السحابي المعلق لمدير النظام */}
            {pendingDeletionRequest && pendingDeletionRequest.status === 'pending' && (
                <div className="bg-gradient-to-r from-red-600 via-rose-600 to-amber-600 text-white p-4 shadow-xl border-b-2 border-amber-300 animate-pulse">
                    <div className="max-w-7xl mx-auto flex flex-col md:flex-row items-center justify-between gap-3">
                        <div className="flex items-center gap-3 text-right">
                            <span className="text-3xl">🔔</span>
                            <div>
                                <div className="font-extrabold text-sm md:text-base flex items-center gap-2">
                                    <span>طلب حذف قاعدة البيانات مقدم من:</span>
                                    <span className="bg-white/20 px-2 py-0.5 rounded-lg font-mono font-black">{pendingDeletionRequest.requestedBy}</span>
                                    <span className="text-xs opacity-80">({pendingDeletionRequest.timestamp})</span>
                                </div>
                                <div className="text-xs text-amber-100 mt-1 font-semibold">
                                    سبب الطلب: "{pendingDeletionRequest.reason}"
                                </div>
                            </div>
                        </div>
                        <div className="flex items-center gap-2">
                            {currentUserRole === 'admin' ? (
                                <>
                                    <button 
                                        onClick={() => {
                                            const pin = prompt('🔐 تأكيد الموافقة على الحذف: أدخل الرمز السري لمدير النظام:');
                                            if (pin === passwordsConfig.admin) {
                                                if (confirm('⚠️ هل توافق رسمياً على تنفيذ طلب الحذف ومسح كافة البيانات سحابياً؟')) {
                                                    executeCompleteDatabaseWipe();
                                                }
                                            } else {
                                                alert('❌ الرمز السري غير صحيح!');
                                            }
                                        }}
                                        className="bg-emerald-500 hover:bg-emerald-600 text-white text-xs font-black px-4 py-2 rounded-xl shadow-lg transition flex items-center gap-1"
                                    >
                                        <span>✅</span> موافقة وتنفيذ الحذف
                                    </button>
                                    <button 
                                        onClick={rejectDeletionRequest}
                                        className="bg-slate-900/80 hover:bg-slate-900 text-white text-xs font-bold px-3 py-2 rounded-xl shadow transition"
                                    >
                                        <span>❌</span> رفض الطلب
                                    </button>
                                </>
                            ) : (
                                <div className="bg-black/30 px-3 py-1.5 rounded-xl text-xs font-bold text-amber-200 flex items-center gap-1.5">
                                    <span className="animate-spin text-sm">⏳</span> الطلب بانتظار موافقة مدير النظام الرئيسي
                                </div>
                            )}
                        </div>
                    </div>
                </div>
            )}"""

# Insert banner_jsx right after main container or top header
header_container = '<header className="bg-gradient-to-r from-blue-700 via-indigo-700 to-slate-900'
if header_container in code:
    code = code.replace(header_container, banner_jsx + "\n            " + header_container, 1)
    print("✓ Added Deletion Request Banner to Header")

with open('e:/Antigravity projects/HR Admin/index.html', 'w', encoding='utf-8') as f:
    f.write(code)

with open('e:/Antigravity projects/HR Admin/نظام_ادراة_الملاك_v7.5_cloud.html', 'w', encoding='utf-8') as f:
    f.write(code)

print("✓ Completed Deletion Request and Approval System implementation!")
