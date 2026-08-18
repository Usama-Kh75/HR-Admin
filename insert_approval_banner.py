import os

with open('e:/Antigravity projects/HR Admin/index.html', 'r', encoding='utf-8') as f:
    code = f.read()

banner_jsx = """            {/* إشعار طلب الحذف السحابي المعلق لمدير النظام */}
            {pendingDeletionRequest && pendingDeletionRequest.status === 'pending' && (
                <div className="bg-gradient-to-r from-red-600 via-rose-600 to-amber-600 text-white p-4 shadow-xl border-b-2 border-amber-300 animate-pulse sticky top-0 z-50">
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

header_line = '<header className="bg-gradient-to-r from-blue-600 via-indigo-600 to-indigo-800'
if header_line in code:
    code = code.replace(header_line, banner_jsx + "\n                    " + header_line, 1)
    print("✓ Successfully injected approval banner right above header!")

with open('e:/Antigravity projects/HR Admin/index.html', 'w', encoding='utf-8') as f:
    f.write(code)

with open('e:/Antigravity projects/HR Admin/نظام_ادراة_الملاك_v7.5_cloud.html', 'w', encoding='utf-8') as f:
    f.write(code)
