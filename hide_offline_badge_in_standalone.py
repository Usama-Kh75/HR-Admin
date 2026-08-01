import os

def update_file(file_path):
    if not os.path.exists(file_path):
        print(f"File not found: {file_path}")
        return False

    with open(file_path, 'r', encoding='utf-8') as f:
        code = f.read()

    old_target = """                            <div 
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

    new_replacement = """                            {syncStatus.connected && (
                                <div 
                                    onClick={() => setShowSyncModal(true)}
                                    className="flex items-center gap-2 px-3.5 py-1.5 rounded-full border cursor-pointer transition shadow-md flex-shrink-0 bg-emerald-950/70 border-emerald-400/40 text-emerald-200 hover:bg-emerald-900/80"
                                    title="اضغط لعرض تفاصيل المزامنة ورابط أجهزة الشعبة"
                                >
                                    <span className="relative flex h-2.5 w-2.5">
                                        <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-emerald-400 opacity-75"></span>
                                        <span className="relative inline-flex rounded-full h-2.5 w-2.5 bg-emerald-500"></span>
                                    </span>
                                    <span className="text-xs font-bold">
                                        🟢 السيرفر المحلي نشط ({syncStatus.ip || 'Local'})
                                    </span>
                                </div>
                            )}"""

    if old_target in code:
        code = code.replace(old_target, new_replacement)
        print(f"✓ Successfully hid offline badge in {file_path}")
    else:
        print(f"Target badge block not found in {file_path}")

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(code)
    return True

if __name__ == '__main__':
    update_file('e:/Antigravity projects/HR Admin/نظام_ادراة_الملاك_v7.0_online.html')
    update_file('e:/Antigravity projects/HR Admin/نظام_ادراة_الملاك_v7.0.html')
