import os

def update_file(file_path):
    if not os.path.exists(file_path):
        print(f"File not found: {file_path}")
        return False

    with open(file_path, 'r', encoding='utf-8') as f:
        code = f.read()

    # 1. Add state for profile fields visibility
    old_states_anchor = "const [selectedEmployeeCard, setSelectedEmployeeCard] = useState(null);"
    new_states_anchor = """const [selectedEmployeeCard, setSelectedEmployeeCard] = useState(null);
            const [cardFieldsVisibility, setCardFieldsVisibility] = useState({
                mobile: true,
                jobNumber: true,
                workType: true,
                education: true,
                bloodType: true,
                safetySizes: true
            });
            const [showFieldCustomizer, setShowFieldCustomizer] = useState(false);"""

    if old_states_anchor in code and "cardFieldsVisibility" not in code:
        code = code.replace(old_states_anchor, new_states_anchor)
        print(f"✓ Added cardFieldsVisibility state to {file_path}")

    # 2. Update Profile Modal HTML to use dynamic field toggles and replace Edit button with Customize Fields button
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

    new_profile_modal = """            {/* نافذة معاينة وبطاقة ملف المنتسب الفاخرة قبل الطباعة مع خيارات التخصيص والإخفاء والإظهار */}
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
                            {/* شريط تخصيص الحقول وإظهارها/إخفائها */}
                            {showFieldCustomizer && (
                                <div className="p-4 bg-slate-100 rounded-2xl border border-slate-300 space-y-2 animate-fadeIn print:hidden">
                                    <div className="text-xs font-black text-slate-800 flex justify-between items-center">
                                        <span>⚙️ حدد الحقول التي تريد إظهارها في البطاقة والطباعة:</span>
                                        <button 
                                            onClick={() => setCardFieldsVisibility({ mobile: true, jobNumber: true, workType: true, education: true, bloodType: true, safetySizes: true })}
                                            className="text-[11px] text-blue-600 font-bold hover:underline"
                                        >
                                            إظهار جميع الحقول
                                        </button>
                                    </div>
                                    <div className="grid grid-cols-2 sm:grid-cols-3 gap-2 pt-1 text-slate-700 font-bold">
                                        <label className="flex items-center gap-1.5 cursor-pointer bg-white px-2.5 py-1.5 rounded-lg border border-slate-200 hover:bg-slate-50">
                                            <input type="checkbox" checked={cardFieldsVisibility.mobile} onChange={(e) => setCardFieldsVisibility({...cardFieldsVisibility, mobile: e.target.checked})} className="rounded text-blue-600" />
                                            <span>📱 رقم الهاتف النقال</span>
                                        </label>
                                        <label className="flex items-center gap-1.5 cursor-pointer bg-white px-2.5 py-1.5 rounded-lg border border-slate-200 hover:bg-slate-50">
                                            <input type="checkbox" checked={cardFieldsVisibility.jobNumber} onChange={(e) => setCardFieldsVisibility({...cardFieldsVisibility, jobNumber: e.target.checked})} className="rounded text-blue-600" />
                                            <span>🆔 الرقم الوظيفي</span>
                                        </label>
                                        <label className="flex items-center gap-1.5 cursor-pointer bg-white px-2.5 py-1.5 rounded-lg border border-slate-200 hover:bg-slate-50">
                                            <input type="checkbox" checked={cardFieldsVisibility.workType} onChange={(e) => setCardFieldsVisibility({...cardFieldsVisibility, workType: e.target.checked})} className="rounded text-blue-600" />
                                            <span>⏰ طبيعة العمل</span>
                                        </label>
                                        <label className="flex items-center gap-1.5 cursor-pointer bg-white px-2.5 py-1.5 rounded-lg border border-slate-200 hover:bg-slate-50">
                                            <input type="checkbox" checked={cardFieldsVisibility.education} onChange={(e) => setCardFieldsVisibility({...cardFieldsVisibility, education: e.target.checked})} className="rounded text-blue-600" />
                                            <span>🎓 التحصيل الدراسي</span>
                                        </label>
                                        <label className="flex items-center gap-1.5 cursor-pointer bg-white px-2.5 py-1.5 rounded-lg border border-slate-200 hover:bg-slate-50">
                                            <input type="checkbox" checked={cardFieldsVisibility.bloodType} onChange={(e) => setCardFieldsVisibility({...cardFieldsVisibility, bloodType: e.target.checked})} className="rounded text-blue-600" />
                                            <span>🩸 فصيلة الدم</span>
                                        </label>
                                        <label className="flex items-center gap-1.5 cursor-pointer bg-white px-2.5 py-1.5 rounded-lg border border-slate-200 hover:bg-slate-50">
                                            <input type="checkbox" checked={cardFieldsVisibility.safetySizes} onChange={(e) => setCardFieldsVisibility({...cardFieldsVisibility, safetySizes: e.target.checked})} className="rounded text-blue-600" />
                                            <span>👕 قياس البدلة والحذاء</span>
                                        </label>
                                    </div>
                                </div>
                            )}

                            {/* المعلومات الأساسية ورقم الهاتف */}
                            {(cardFieldsVisibility.mobile || cardFieldsVisibility.jobNumber) && (
                                <div className="grid grid-cols-2 gap-3">
                                    {cardFieldsVisibility.mobile && (
                                        <div className="p-3.5 bg-amber-50 rounded-2xl border border-amber-200">
                                            <div className="text-[11px] text-amber-700 font-bold mb-1">📱 رقم الهاتف النقال:</div>
                                            <div className="text-sm font-mono font-black text-amber-950 text-right">
                                                {selectedEmployeeCard.mobile || selectedEmployeeCard.phone || 'غير مسجل'}
                                            </div>
                                        </div>
                                    )}
                                    {cardFieldsVisibility.jobNumber && (
                                        <div className="p-3.5 bg-blue-50 rounded-2xl border border-blue-200">
                                            <div className="text-[11px] text-blue-700 font-bold mb-1">🆔 الرقم الوظيفي / السجل:</div>
                                            <div className="text-sm font-mono font-black text-blue-950">
                                                {selectedEmployeeCard.jobNumber || 'غير مسجل'}
                                            </div>
                                        </div>
                                    )}
                                </div>
                            )}

                            {/* تفاصيل طبيعة العمل والتحصيل العلمي وفصيلة الدم */}
                            {(cardFieldsVisibility.workType || cardFieldsVisibility.education || cardFieldsVisibility.bloodType) && (
                                <div className="grid grid-cols-3 gap-3">
                                    {cardFieldsVisibility.workType && (
                                        <div className="p-3 bg-slate-50 rounded-2xl border border-slate-200">
                                            <div className="text-[11px] text-slate-500 font-bold mb-0.5">⏰ طبيعة العمل:</div>
                                            <div className="font-bold text-slate-800">{selectedEmployeeCard.workType || 'صباحي'}</div>
                                        </div>
                                    )}
                                    {cardFieldsVisibility.education && (
                                        <div className="p-3 bg-slate-50 rounded-2xl border border-slate-200">
                                            <div className="text-[11px] text-slate-500 font-bold mb-0.5">🎓 التحصيل الدراسي:</div>
                                            <div className="font-bold text-slate-800">{selectedEmployeeCard.education || 'غير محدد'}</div>
                                        </div>
                                    )}
                                    {cardFieldsVisibility.bloodType && (
                                        <div className="p-3 bg-slate-50 rounded-2xl border border-slate-200">
                                            <div className="text-[11px] text-slate-500 font-bold mb-0.5">🩸 فصيلة الدم:</div>
                                            <div className="font-bold text-red-600 font-mono">{selectedEmployeeCard.bloodType || 'غير محدد'}</div>
                                        </div>
                                    )}
                                </div>
                            )}

                            {/* قياسات السلامة والبدلة الموحدة */}
                            {cardFieldsVisibility.safetySizes && (
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
                            )}

                            {/* أزرار التحكم والطباعة وتخصيص الحقول */}
                            <div className="flex justify-between items-center pt-2 print:hidden">
                                <button
                                    onClick={() => setShowFieldCustomizer(!showFieldCustomizer)}
                                    className="px-4 py-2.5 bg-indigo-50 hover:bg-indigo-100 text-indigo-700 font-bold rounded-xl text-xs border border-indigo-200 transition flex items-center gap-1.5"
                                    title="تحديد الحقول التي ترغب بإظهارها أو إخفائها"
                                >
                                    <span>⚙️</span>
                                    <span>{showFieldCustomizer ? 'إغلاق شريط التخصيص' : 'تخصيص الحقول المعروضة'}</span>
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
        print(f"✓ Added Field Visibility Customizer to Profile Modal in {file_path}")

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(code)
    return True

if __name__ == '__main__':
    update_file('e:/Antigravity projects/HR Admin/index.html')
    update_file('e:/Antigravity projects/HR Admin/نظام_ادراة_الملاك_v6.9_online.html')
    update_file('e:/Antigravity projects/HR Admin/نظام_ادراة_الملاك_v6.9.html')
