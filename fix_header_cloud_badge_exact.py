import os

# Update header badge to check cloudSyncStatus cleanly
with open('e:/Antigravity projects/HR Admin/index.html', 'r', encoding='utf-8') as f:
    code = f.read()

old_badge_block = """                                <span className="relative flex h-2.5 w-2.5">
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
                                </span>"""

new_badge_block = """                                <span className="relative flex h-2.5 w-2.5">
                                    {cloudSyncStatus.connected || syncStatus.connected ? (
                                        <>
                                            <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-emerald-400 opacity-75"></span>
                                            <span className="relative inline-flex rounded-full h-2.5 w-2.5 bg-emerald-500"></span>
                                        </>
                                    ) : (
                                        <span className="relative inline-flex rounded-full h-2.5 w-2.5 bg-amber-500"></span>
                                    )}
                                </span>
                                <span className="text-xs font-bold">
                                    {cloudSyncStatus.connected ? '☁️ متصل بالسحابة الحية (أونلاين 24/7)' : (syncStatus.connected ? `🟢 السيرفر المحلي نشط (${syncStatus.ip || 'Local'})` : '🟡 أوفلاين محلي')}
                                </span>"""

if old_badge_block in code:
    code = code.replace(old_badge_block, new_badge_block)
    print("✓ Updated top header cloud badge block cleanly!")

with open('e:/Antigravity projects/HR Admin/index.html', 'w', encoding='utf-8') as f:
    f.write(code)

with open('e:/Antigravity projects/HR Admin/نظام_ادراة_الملاك_v7.5_cloud.html', 'w', encoding='utf-8') as f:
    f.write(code)
