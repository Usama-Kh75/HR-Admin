import os

def update_file(file_path):
    if not os.path.exists(file_path):
        print(f"File not found: {file_path}")
        return False

    with open(file_path, 'r', encoding='utf-8') as f:
        code = f.read()

    # 1. Clean up search match card in sidebar (remove mobile phone pill from sidebar card)
    old_match_card = """                                                                    <div className="text-lg font-black text-white leading-tight mb-1">{unifiedResults[0].name}</div>
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

    new_match_card = """                                                                    <div className="text-lg font-black text-white leading-tight mb-1">{unifiedResults[0].name}</div>
                                                                    <div className="text-xs font-bold text-blue-200 mb-2">{unifiedResults[0].jobTitle || 'منتسب'}</div>
                                                                    <div className="text-[11px] font-bold text-indigo-100 bg-white bg-opacity-10 px-3 py-1 rounded-full inline-flex items-center gap-1 border border-white border-opacity-10 mb-3">
                                                                        📍 {unifiedResults[0].unit || unifiedResults[0].location || 'غير محدد'}
                                                                    </div>
                                                                    <button
                                                                        onClick={() => setSelectedEmployeeCard(unifiedResults[0])}
                                                                        className="w-full py-2 bg-gradient-to-r from-blue-500 to-indigo-600 hover:from-blue-600 hover:to-indigo-700 text-white rounded-xl text-xs font-black shadow-lg transition transform hover:scale-[1.02] active:scale-95 flex items-center justify-center gap-1.5 border border-white/20"
                                                                    >
                                                                        <span>📇</span>
                                                                        <span>عرض المعاينة وبطاقة المنتسب</span>
                                                                    </button>"""

    if old_match_card in code:
        code = code.replace(old_match_card, new_match_card)
        print(f"✓ Cleaned search match card in {file_path}")

    # 2. Update Employee Profile Card Modal HTML to remove external work number, use uniform size, and add edit button
    old_profile_modal = """            {/* نافذة معاينة وبطاقة ملف المنتسب الفاخرة قبل الطباعة (Employee Rich Profile & ID Card Modal) */}
            {selectedEmployeeCard && (
                <div className="fixed inset-0 bg-slate-950/80 backdrop-blur-md z-50 flex items-center justify-center p-4 print:p-0 print:bg-white print:static">
                    <div className="bg-white rounded-3xl shadow-2xl border border-slate-100 max-w-2xl w-full overflow-hidden animate-fadeInUp print:shadow-none print:border-none print:max-w-none print:w-full">
                        {/* Header */}
                        <div className="bg-gradient-to-r from-blue-900 via-indigo-900 to-slate-900 p-6 text-white relative flex justify-between items-start print:bg-none print:text-slate-900 print:border-b-2 print:border-slate-800 print:p-4">
                            <div className="flex items-center gap-4">
                                <div className="w-20 h-20 rounded-2xl border-2 border-white/30 bg-white/10 flex items-center justify-center overflow-hidden flex-shrink-0 shadow-inner">
                                    {selectedEmployeeCard.photo ? (
                                        <img src={selectedEmployeeCard.photo} className="w-full h-full object-cover" alt={selectedEmployeeCard.name} />
                                    ) : (
                                        <span className="text-4xl">👤</span>
                                    )}
                                </div>
                                <div>
                                    <div className="text-[11px] font-bold text-blue-200 print:text-slate-600 mb-0.5">شركة نفط البصرة · قسم التكييف والتبريد</div>
                                    <h2 className="text-2xl font-black leading-tight">{selectedEmployeeCard.name}</h2>
                                    <div className="flex flex-wrap items-center gap-2 mt-1">
                                        <span className="px-2.5 py-0.5 bg-blue-500/20 text-blue-100 print:bg-slate-100 print:text-slate-800 text-xs font-bold rounded-lg border border-blue-400/20">
                                            👔 {selectedEmployeeCard.jobTitle || 'منتسب'}
                                        </span>
                                        <span className="px-2.5 py-0.5 bg-emerald-500/20 text-emerald-200 print:bg-slate-100 print:text-slate-800 text-xs font-bold rounded-lg border border-emerald-400/20">
                                            📍 {selectedEmployeeCard.unit || selectedEmployeeCard.location || 'غير محدد'}
                                        </span>
                                    </div>
                                </div>
                            </div>
                            <button
                                onClick={() => setSelectedEmployeeCard(null)}
                                className="w-8 h-8 rounded-full bg-white/10 hover:bg-white/20 flex items-center justify-center text-white font-bold transition print:hidden"
                            >
                                ✕
                            </button>
                        </div>

                        {/* Card Details Grid */}
                        <div className="p-6 space-y-6 text-slate-800 text-xs">
                            {/* المعلومات الأساسية ورقم الهاتف */}
                            <div className="grid grid-cols-2 sm:grid-cols-3 gap-3">
                                <div className="p-3 bg-amber-50 rounded-2xl border border-amber-200">
                                    <div className="text-[11px] text-amber-700 font-bold mb-1">📱 رقم الهاتف النقال:</div>
                                    <div className="text-sm font-mono font-black text-amber-950 dir-ltr text-right">
                                        {selectedEmployeeCard.mobile || selectedEmployeeCard.phone || 'غير مسجل'}
                                    </div>
                                </div>
                                <div className="p-3 bg-blue-50 rounded-2xl border border-blue-200">
                                    <div className="text-[11px] text-blue-700 font-bold mb-1">🆔 الرقم الوظيفي / السجل:</div>
                                    <div className="text-sm font-mono font-black text-blue-950">
                                        {selectedEmployeeCard.jobNumber || 'غير مسجل'}
                                    </div>
                                </div>
                                <div className="p-3 bg-indigo-50 rounded-2xl border border-indigo-200">
                                    <div className="text-[11px] text-indigo-700 font-bold mb-1">⚙️ رقم العمل الخارجي:</div>
                                    <div className="text-sm font-mono font-black text-indigo-950">
                                        {selectedEmployeeCard.workNumber || 'غير مسجل'}
                                    </div>
                                </div>
                            </div>

                            {/* تفاصيل طبيعة العمل والتحصيل العلمي */}
                            <div className="grid grid-cols-2 sm:grid-cols-3 gap-3">
                                <div className="p-3 bg-slate-50 rounded-2xl border border-slate-200">
                                    <div className="text-[11px] text-slate-500 font-bold mb-0.5">⏰ طبيعة العمل:</div>
                                    <div className="font-bold text-slate-800">{selectedEmployeeCard.workType || 'صباحي'}</div>
                                </div>
                                <div className="p-3 bg-slate-50 rounded-2xl border border-slate-200">
                                    <div className="text-[11px] text-slate-500 font-bold mb-0.5">🎓 التحصيل الدراسي:</div>
                                    <div className="font-bold text-slate-800">{selectedEmployeeCard.education || 'غير محدد'}</div>
                                </div>
                                <div className="p-3 bg-slate-50 rounded-2xl border border-slate-200">
                                    <div className="text-[11px] text-slate-500 font-bold mb-0.5">🩸 فصيلة الدم:</div>
                                    <div className="font-bold text-red-600 font-mono">{selectedEmployeeCard.bloodType || 'غير محدد'}</div>
                                </div>
                            </div>

                            {/* قياسات السلامة والبدلة */}
                            <div className="bg-slate-50 p-4 rounded-2xl border border-slate-200 space-y-2">
                                <div className="text-xs font-black text-slate-700 flex items-center gap-1.5">
                                    <span>👕</span>
                                    <span>قياسات السلامة والبدلة الخاصة بالمنتسب:</span>
                                </div>
                                <div className="grid grid-cols-3 gap-2 text-center">
                                    <div className="bg-white p-2 rounded-xl border border-slate-200">
                                        <div className="text-[10px] text-slate-400 font-bold">القميص (Shirt):</div>
                                        <div className="font-bold text-slate-800">{selectedEmployeeCard.shirtSize || 'غير مسجل'}</div>
                                    </div>
                                    <div className="bg-white p-2 rounded-xl border border-slate-200">
                                        <div className="text-[10px] text-slate-400 font-bold">البنطال (Pants):</div>
                                        <div className="font-bold text-slate-800">{selectedEmployeeCard.pantsSize || 'غير مسجل'}</div>
                                    </div>
                                    <div className="bg-white p-2 rounded-xl border border-slate-200">
                                        <div className="text-[10px] text-slate-400 font-bold">الحذاء (Shoes):</div>
                                        <div className="font-bold text-slate-800">{selectedEmployeeCard.shoeSize || 'غير مسجل'}</div>
                                    </div>
                                </div>
                            </div>

                            {/* أزرار التحكم والطباعة */}
                            <div className="flex justify-end gap-3 pt-2 print:hidden">
                                <button
                                    onClick={() => setSelectedEmployeeCard(null)}
                                    className="px-5 py-2.5 bg-slate-100 hover:bg-slate-200 text-slate-700 font-bold rounded-xl text-xs transition"
                                >
                                    إغلاق
                                </button>
                                <button
                                    onClick={() => window.print()}
                                    className="px-6 py-2.5 bg-gradient-to-r from-blue-600 to-indigo-700 hover:from-blue-700 hover:to-indigo-800 text-white font-bold rounded-xl text-xs shadow-lg transition flex items-center gap-2"
                                >
                                    <span>🖨️</span>
                                    <span>طباعة بطاقة المنتسب A4</span>
                                </button>
                            </div>
                        </div>
                    </div>
                </div>
            )}"""

    new_profile_modal = """            {/* نافذة معاينة وبطاقة ملف المنتسب الفاخرة قبل الطباعة (Employee Rich Profile & ID Card Modal) */}
            {selectedEmployeeCard && (
                <div className="fixed inset-0 bg-slate-950/80 backdrop-blur-md z-50 flex items-center justify-center p-4 print:p-0 print:bg-white print:static">
                    <div className="bg-white rounded-3xl shadow-2xl border border-slate-100 max-w-2xl w-full overflow-hidden animate-fadeInUp print:shadow-none print:border-none print:max-w-none print:w-full">
                        {/* Header */}
                        <div className="bg-gradient-to-r from-blue-900 via-indigo-900 to-slate-900 p-6 text-white relative flex justify-between items-start print:bg-none print:text-slate-900 print:border-b-2 print:border-slate-800 print:p-4">
                            <div className="flex items-center gap-4">
                                <div className="w-20 h-20 rounded-2xl border-2 border-white/30 bg-white/10 flex items-center justify-center overflow-hidden flex-shrink-0 shadow-inner">
                                    {selectedEmployeeCard.photo ? (
                                        <img src={selectedEmployeeCard.photo} className="w-full h-full object-cover" alt={selectedEmployeeCard.name} />
                                    ) : (
                                        <span className="text-4xl">👤</span>
                                    )}
                                </div>
                                <div>
                                    <div className="text-[11px] font-bold text-blue-200 print:text-slate-600 mb-0.5">شركة نفط البصرة · قسم التكييف والتبريد</div>
                                    <h2 className="text-2xl font-black leading-tight">{selectedEmployeeCard.name}</h2>
                                    <div className="flex flex-wrap items-center gap-2 mt-1">
                                        <span className="px-2.5 py-0.5 bg-blue-500/20 text-blue-100 print:bg-slate-100 print:text-slate-800 text-xs font-bold rounded-lg border border-blue-400/20">
                                            👔 {selectedEmployeeCard.jobTitle || 'منتسب'}
                                        </span>
                                        <span className="px-2.5 py-0.5 bg-emerald-500/20 text-emerald-200 print:bg-slate-100 print:text-slate-800 text-xs font-bold rounded-lg border border-emerald-400/20">
                                            📍 {selectedEmployeeCard.unit || selectedEmployeeCard.location || 'غير محدد'}
                                        </span>
                                    </div>
                                </div>
                            </div>
                            <button
                                onClick={() => setSelectedEmployeeCard(null)}
                                className="w-8 h-8 rounded-full bg-white/10 hover:bg-white/20 flex items-center justify-center text-white font-bold transition print:hidden"
                            >
                                ✕
                            </button>
                        </div>

                        {/* Card Details Grid */}
                        <div className="p-6 space-y-5 text-slate-800 text-xs">
                            {/* المعلومات الأساسية ورقم الهاتف */}
                            <div className="grid grid-cols-2 gap-3">
                                <div className="p-3.5 bg-amber-50 rounded-2xl border border-amber-200">
                                    <div className="text-[11px] text-amber-700 font-bold mb-1">📱 رقم الهاتف النقال:</div>
                                    <div className="text-sm font-mono font-black text-amber-950 text-right">
                                        {selectedEmployeeCard.mobile || selectedEmployeeCard.phone || 'غير مسجل'}
                                    </div>
                                </div>
                                <div className="p-3.5 bg-blue-50 rounded-2xl border border-blue-200">
                                    <div className="text-[11px] text-blue-700 font-bold mb-1">🆔 الرقم الوظيفي / السجل:</div>
                                    <div className="text-sm font-mono font-black text-blue-950">
                                        {selectedEmployeeCard.jobNumber || 'غير مسجل'}
                                    </div>
                                </div>
                            </div>

                            {/* تفاصيل طبيعة العمل والتحصيل العلمي وفصيلة الدم */}
                            <div className="grid grid-cols-3 gap-3">
                                <div className="p-3 bg-slate-50 rounded-2xl border border-slate-200">
                                    <div className="text-[11px] text-slate-500 font-bold mb-0.5">⏰ طبيعة العمل:</div>
                                    <div className="font-bold text-slate-800">{selectedEmployeeCard.workType || 'صباحي'}</div>
                                </div>
                                <div className="p-3 bg-slate-50 rounded-2xl border border-slate-200">
                                    <div className="text-[11px] text-slate-500 font-bold mb-0.5">🎓 التحصيل الدراسي:</div>
                                    <div className="font-bold text-slate-800">{selectedEmployeeCard.education || 'غير محدد'}</div>
                                </div>
                                <div className="p-3 bg-slate-50 rounded-2xl border border-slate-200">
                                    <div className="text-[11px] text-slate-500 font-bold mb-0.5">🩸 فصيلة الدم:</div>
                                    <div className="font-bold text-red-600 font-mono">{selectedEmployeeCard.bloodType || 'غير محدد'}</div>
                                </div>
                            </div>

                            {/* قياسات السلامة والبدلة الموحدة */}
                            <div className="bg-slate-50 p-4 rounded-2xl border border-slate-200 space-y-2">
                                <div className="text-xs font-black text-slate-700 flex items-center gap-1.5">
                                    <span>👕</span>
                                    <span>قياسات السلامة والبدلة المعتمدة للمنتسب:</span>
                                </div>
                                <div className="grid grid-cols-2 gap-3 text-center">
                                    <div className="bg-white p-3 rounded-xl border border-slate-200">
                                        <div className="text-[11px] text-slate-500 font-bold mb-0.5">👕 قياس البدلة:</div>
                                        <div className="font-extrabold text-slate-800 text-sm">{selectedEmployeeCard.uniformSize || 'غير مسجل'}</div>
                                    </div>
                                    <div className="bg-white p-3 rounded-xl border border-slate-200">
                                        <div className="text-[11px] text-slate-500 font-bold mb-0.5">🥾 قياس حذاء السلامة:</div>
                                        <div className="font-extrabold text-slate-800 text-sm">{selectedEmployeeCard.shoeSafetySize || selectedEmployeeCard.shoeSize || 'غير مسجل'}</div>
                                    </div>
                                </div>
                            </div>

                            {/* أزرار التحكم والطباعة والتعديل */}
                            <div className="flex justify-between items-center pt-2 print:hidden">
                                <button
                                    onClick={() => {
                                        const emp = selectedEmployeeCard;
                                        setSelectedEmployeeCard(null);
                                        openEditModal(emp);
                                    }}
                                    className="px-4 py-2.5 bg-amber-500 hover:bg-amber-600 text-white font-bold rounded-xl text-xs shadow transition flex items-center gap-1.5"
                                    title="تعديل بيانات ورقم المنتسب"
                                >
                                    <span>✏️</span>
                                    <span>تعديل معلومات المنتسب</span>
                                </button>
                                <div className="flex gap-2">
                                    <button
                                        onClick={() => setSelectedEmployeeCard(null)}
                                        className="px-5 py-2.5 bg-slate-100 hover:bg-slate-200 text-slate-700 font-bold rounded-xl text-xs transition"
                                    >
                                        إغلاق
                                    </button>
                                    <button
                                        onClick={() => window.print()}
                                        className="px-6 py-2.5 bg-gradient-to-r from-blue-600 to-indigo-700 hover:from-blue-700 hover:to-indigo-800 text-white font-bold rounded-xl text-xs shadow-lg transition flex items-center gap-2"
                                    >
                                        <span>🖨️</span>
                                        <span>طباعة بطاقة المنتسب A4</span>
                                    </button>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            )}"""

    if old_profile_modal in code:
        code = code.replace(old_profile_modal, new_profile_modal)
        print(f"✓ Refined Profile Modal with uniform size & edit button in {file_path}")

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(code)
    return True

if __name__ == '__main__':
    update_file('e:/Antigravity projects/HR Admin/index.html')
    update_file('e:/Antigravity projects/HR Admin/نظام_ادراة_الملاك_v6.9_online.html')
    update_file('e:/Antigravity projects/HR Admin/نظام_ادراة_الملاك_v6.9.html')
