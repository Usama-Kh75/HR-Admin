import os
import re

def update_file(file_path):
    if not os.path.exists(file_path):
        print(f"File not found: {file_path}")
        return False

    with open(file_path, 'r', encoding='utf-8') as f:
        code = f.read()

    # 1. Add state for showUnitDropdown & update initial unifiedFilters state to include selectedUnits
    old_state_def = "const [unifiedFilters, setUnifiedFilters] = useState({ location:'', unit:'', workType:'', education:'', yearsOfService:'', graduationYear:'', hireYear:'', gender:'', hasMissingInfo:'' });"
    new_state_def = "const [unifiedFilters, setUnifiedFilters] = useState({ location:'', unit:'', selectedUnits:[], workType:'', education:'', yearsOfService:'', graduationYear:'', hireYear:'', gender:'', hasMissingInfo:'' });\n            const [showUnitDropdown, setShowUnitDropdown] = useState(false);"

    if old_state_def in code:
        code = code.replace(old_state_def, new_state_def)
        print(f"✓ Updated unifiedFilters state definition in {file_path}")

    # 2. Update performUnifiedSearch filtering logic for selectedUnits
    old_filter_logic = "if (f.unit)          results = results.filter(s => normalizeArabic(s.unit||'') === normalizeArabic(f.unit));"
    new_filter_logic = """if (f.selectedUnits && f.selectedUnits.length > 0) {
                    results = results.filter(s => f.selectedUnits.some(u => normalizeArabic(s.unit||'') === normalizeArabic(u)));
                } else if (f.unit) {
                    results = results.filter(s => normalizeArabic(s.unit||'') === normalizeArabic(f.unit));
                }"""

    if old_filter_logic in code:
        code = code.replace(old_filter_logic, new_filter_logic)
        print(f"✓ Updated performUnifiedSearch logic in {file_path}")

    # 3. Replace single-select dropdown UI with Multi-Select Checkboxes Dropdown
    old_select_ui = """                                                        <div>
                                                            <label className="block text-xs font-bold text-gray-500 mb-1">🏢 الوحدة</label>
                                                            <select value={unifiedFilters.unit}
                                                                onChange={(e) => setUnifiedFilters({...unifiedFilters, unit: e.target.value})}
                                                                className="w-full px-2 py-1.5 text-xs border rounded-lg focus:border-teal-500 outline-none bg-white">
                                                                <option value="">الكل</option>
                                                                {['مقر الشعبة','تبريد باب الزبير','ورشة التبريد','تبريد المكينة','تبريد نهر بن عمر','تبريد المركز الثقافي'].map(u => (
                                                                    <option key={u} value={u}>{u}</option>
                                                                ))}
                                                            </select>
                                                        </div>"""

    new_multiselect_ui = """                                                        <div className="relative">
                                                            <label className="block text-xs font-bold text-gray-500 mb-1">🏢 الوحدة (اختيار متعدد)</label>
                                                            <button
                                                                type="button"
                                                                onClick={() => setShowUnitDropdown(!showUnitDropdown)}
                                                                className="w-full px-2.5 py-1.5 text-xs border rounded-lg focus:border-teal-500 outline-none bg-white flex justify-between items-center font-bold text-slate-800 shadow-sm hover:bg-slate-50 transition"
                                                            >
                                                                <span className="truncate">
                                                                    {!unifiedFilters.selectedUnits || unifiedFilters.selectedUnits.length === 0 
                                                                        ? "الكل (جميع الوحدات)" 
                                                                        : unifiedFilters.selectedUnits.length === 1
                                                                        ? `📍 ${unifiedFilters.selectedUnits[0]}`
                                                                        : `📍 تم اختيار (${unifiedFilters.selectedUnits.length}) وحدات`}
                                                                </span>
                                                                <span className="text-gray-400 text-[10px] mr-1">{showUnitDropdown ? '▲' : '▼'}</span>
                                                            </button>

                                                            {showUnitDropdown && (
                                                                <div className="absolute z-50 mt-1 w-64 bg-white border border-slate-200 rounded-xl shadow-2xl p-2.5 space-y-1.5 text-xs animate-fadeInUp">
                                                                    <div className="flex justify-between items-center pb-2 border-b border-slate-100 mb-1">
                                                                        <span className="text-[11px] font-bold text-slate-600">اختر الوحدات المطلوبة:</span>
                                                                        {unifiedFilters.selectedUnits && unifiedFilters.selectedUnits.length > 0 && (
                                                                            <button
                                                                                type="button"
                                                                                onClick={() => setUnifiedFilters({ ...unifiedFilters, selectedUnits: [] })}
                                                                                className="text-[10px] font-bold text-red-600 hover:underline"
                                                                            >
                                                                                إلغاء التحديد
                                                                            </button>
                                                                        )}
                                                                    </div>
                                                                    {['مقر الشعبة', 'تبريد باب الزبير', 'ورشة التبريد', 'تبريد المكينة', 'تبريد نهر بن عمر', 'تبريد المركز الثقافي'].map(u => {
                                                                        const isChecked = (unifiedFilters.selectedUnits || []).includes(u);
                                                                        return (
                                                                            <label 
                                                                                key={u} 
                                                                                className={`flex items-center gap-2 px-2 py-1.5 rounded-lg cursor-pointer transition text-xs font-bold ${
                                                                                    isChecked ? 'bg-indigo-50 text-indigo-900' : 'hover:bg-slate-50 text-slate-700'
                                                                                }`}
                                                                            >
                                                                                <input
                                                                                    type="checkbox"
                                                                                    checked={isChecked}
                                                                                    onChange={(e) => {
                                                                                        const prev = unifiedFilters.selectedUnits || [];
                                                                                        let next;
                                                                                        if (e.target.checked) {
                                                                                            next = [...prev, u];
                                                                                        } else {
                                                                                            next = prev.filter(x => x !== u);
                                                                                        }
                                                                                        setUnifiedFilters({ ...unifiedFilters, selectedUnits: next, unit: '' });
                                                                                    }}
                                                                                    className="w-4 h-4 text-indigo-600 rounded border-slate-300 focus:ring-indigo-500 cursor-pointer"
                                                                                />
                                                                                <span>📍 {u}</span>
                                                                            </label>
                                                                        );
                                                                    })}
                                                                </div>
                                                            )}
                                                        </div>"""

    if old_select_ui in code:
        code = code.replace(old_select_ui, new_multiselect_ui)
        print(f"✓ Replaced single-select UI with Multi-Select Checkboxes in {file_path}")
    else:
        print(f"Old select UI not found in {file_path}")

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(code)
    return True

if __name__ == '__main__':
    update_file('e:/Antigravity projects/HR Admin/index.html')
    update_file('e:/Antigravity projects/HR Admin/نظام_ادراة_الملاك_v6.8_online.html')
    update_file('e:/Antigravity projects/HR Admin/نظام_ادراة_الملاك_v6.8.html')
