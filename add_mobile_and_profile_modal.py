import os

def update_search_card(file_path):
    if not os.path.exists(file_path):
        print(f"File not found: {file_path}")
        return False

    with open(file_path, 'r', encoding='utf-8') as f:
        code = f.read()

    old_target = """                                                                    <div className="text-lg font-black text-white leading-tight mb-1">{unifiedResults[0].name}</div>
                                                                    <div className="text-xs font-bold text-blue-200 mb-2">{unifiedResults[0].jobTitle}</div>
                                                                    <div className="text-[11px] font-bold text-indigo-100 bg-white bg-opacity-10 px-3 py-1 rounded-full inline-flex items-center gap-1 border border-white border-opacity-10">
                                                                        📍 {unifiedResults[0].unit || unifiedResults[0].location || 'غير محدد'}
                                                                    </div>"""

    new_replacement = """                                                                    <div className="text-lg font-black text-white leading-tight mb-1">{unifiedResults[0].name}</div>
                                                                    <div className="text-xs font-bold text-blue-200 mb-1.5">{unifiedResults[0].jobTitle || 'منتسب'}</div>
                                                                    <div className="flex flex-wrap items-center justify-center gap-1.5 mb-2">
                                                                        <div className="text-[11px] font-bold text-indigo-100 bg-white bg-opacity-10 px-3 py-0.5 rounded-full inline-flex items-center gap-1 border border-white border-opacity-10">
                                                                            📍 {unifiedResults[0].unit || unifiedResults[0].location || 'غير محدد'}
                                                                        </div>
                                                                        <div className="text-[11px] font-mono font-bold text-amber-200 bg-amber-950/40 px-3 py-0.5 rounded-full inline-flex items-center gap-1 border border-amber-400/30 shadow-inner">
                                                                            📱 {unifiedResults[0].mobile || unifiedResults[0].phone || 'غير مسجل'}
                                                                        </div>
                                                                    </div>
                                                                    <button
                                                                        onClick={() => setSelectedEmployeeCard(unifiedResults[0])}
                                                                        className="mt-1.5 w-full py-2 bg-gradient-to-r from-blue-500 to-indigo-600 hover:from-blue-600 hover:to-indigo-700 text-white rounded-xl text-xs font-black shadow-lg transition transform hover:scale-[1.02] active:scale-95 flex items-center justify-center gap-1.5 border border-white/20"
                                                                    >
                                                                        <span>📇</span>
                                                                        <span>عرض المعاينة وبطاقة المنتسب</span>
                                                                    </button>"""

    if old_target in code:
        code = code.replace(old_target, new_replacement)
        print(f"✓ Added mobile & profile button to search card in {file_path}")
    else:
        print(f"Target not found in {file_path}")

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(code)
    return True

if __name__ == '__main__':
    update_search_card('e:/Antigravity projects/HR Admin/index.html')
    update_search_card('e:/Antigravity projects/HR Admin/نظام_ادراة_الملاك_v6.9_online.html')
    update_search_card('e:/Antigravity projects/HR Admin/نظام_ادراة_الملاك_v6.9.html')
