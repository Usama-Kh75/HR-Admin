import os

# Script to replace the old local offline header badge with the Cloud Sync Badge
with open('e:/Antigravity projects/HR Admin/index.html', 'r', encoding='utf-8') as f:
    code = f.read()

old_header_badge = """                                {/* مؤشر حالة الاتصال بالسيرفر */}
                                <button 
                                    onClick={() => setShowSyncModal(true)}
                                    className={`px-3 py-1.5 rounded-full text-[11px] font-bold transition flex items-center gap-1.5 shadow-sm border ${
                                        syncStatus.connected 
                                            ? 'bg-emerald-500/20 text-emerald-300 border-emerald-500/40 hover:bg-emerald-500/30' 
                                            : 'bg-amber-500/20 text-amber-300 border-amber-500/40 hover:bg-amber-500/30'
                                    }`}
                                >
                                    <span className={`w-2 h-2 rounded-full ${syncStatus.connected ? 'bg-emerald-400 animate-pulse' : 'bg-amber-400'}`}></span>
                                    {syncStatus.connected ? 'أونلاين سيرفر' : 'أوفلاين محلي'}
                                </button>"""

new_header_badge = """                                {/* مؤشر حالة الاتصال بالسحابة والسيرفر */}
                                <button 
                                    onClick={() => setShowSyncModal(true)}
                                    className={`px-3 py-1.5 rounded-full text-[11px] font-bold transition flex items-center gap-1.5 shadow-sm border ${
                                        cloudSyncStatus.connected || syncStatus.connected 
                                            ? 'bg-emerald-500/20 text-emerald-300 border-emerald-500/40 hover:bg-emerald-500/30' 
                                            : 'bg-amber-500/20 text-amber-300 border-amber-500/40 hover:bg-amber-500/30'
                                    }`}
                                >
                                    <span className={`w-2 h-2 rounded-full ${cloudSyncStatus.connected || syncStatus.connected ? 'bg-emerald-400 animate-pulse' : 'bg-amber-400'}`}></span>
                                    {cloudSyncStatus.connected ? '☁️ متصل بالسحابة الحية' : syncStatus.connected ? '🟢 متصل بالسيرفر' : '🟡 أوفلاين محلي'}
                                </button>"""

if old_header_badge in code:
    code = code.replace(old_header_badge, new_header_badge)
    print("✓ Updated top header badge to display Cloud Sync status")

with open('e:/Antigravity projects/HR Admin/index.html', 'w', encoding='utf-8') as f:
    f.write(code)

with open('e:/Antigravity projects/HR Admin/نظام_ادراة_الملاك_v7.5_cloud.html', 'w', encoding='utf-8') as f:
    f.write(code)
