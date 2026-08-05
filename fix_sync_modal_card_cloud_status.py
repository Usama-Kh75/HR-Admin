import os

# Update showSyncModal card in index.html to display Cloud connectivity status
with open('e:/Antigravity projects/HR Admin/index.html', 'r', encoding='utf-8') as f:
    code = f.read()

old_modal_card_code = """                            {/* بطاقة حالة الاتصال */}
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
                            </div>"""

new_modal_card_code = """                            {/* بطاقة حالة الاتصال */}
                            {cloudSyncStatus && cloudSyncStatus.connected ? (
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
                            )}"""

if old_modal_card_code in code:
    code = code.replace(old_modal_card_code, new_modal_card_code)
    print("✓ Successfully updated showSyncModal card to display Cloud Sync status!")

with open('e:/Antigravity projects/HR Admin/index.html', 'w', encoding='utf-8') as f:
    f.write(code)

with open('e:/Antigravity projects/HR Admin/نظام_ادراة_الملاك_v7.5_cloud.html', 'w', encoding='utf-8') as f:
    f.write(code)
