import os

def update_search_table_row(file_path):
    if not os.path.exists(file_path):
        print(f"File not found: {file_path}")
        return False

    with open(file_path, 'r', encoding='utf-8') as f:
        code = f.read()

    old_row_target = """                                                                        <td className="px-3 py-2 border border-gray-200 text-gray-600">{s.jobNumber}</td>
                                                                        <td className="px-3 py-2 border border-gray-200 text-gray-700">{s.jobTitle}</td>"""

    new_row_replacement = """                                                                        <td className="px-3 py-2 border border-gray-200 font-mono text-xs text-blue-900 font-bold">{s.jobNumber}</td>
                                                                        <td className="px-3 py-2 border border-gray-200 text-xs text-gray-700 font-bold">{s.jobTitle}</td>
                                                                        <td className="px-3 py-2 border border-gray-200 text-xs font-mono font-bold text-amber-800">
                                                                            <div className="flex items-center justify-between gap-1">
                                                                                <span dir="ltr">{s.mobile || s.phone ? `📱 ${s.mobile || s.phone}` : '-'}</span>
                                                                                <button 
                                                                                    onClick={() => setSelectedEmployeeCard(s)}
                                                                                    className="px-2 py-0.5 bg-blue-50 hover:bg-blue-100 text-blue-700 border border-blue-200 rounded text-[11px] font-sans font-bold transition shadow-xs"
                                                                                    title="معاينة بطاقة المنتسب الكاملة"
                                                                                >
                                                                                    📇 بطاقة
                                                                                </button>
                                                                            </div>
                                                                        </td>"""

    if old_row_target in code:
        code = code.replace(old_row_target, new_row_replacement)
        print(f"✓ Added Mobile Phone cell & ID card button to search table rows in {file_path}")
    else:
        print(f"Target row cells not found in {file_path}")

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(code)
    return True

if __name__ == '__main__':
    update_search_table_row('e:/Antigravity projects/HR Admin/index.html')
    update_search_table_row('e:/Antigravity projects/HR Admin/نظام_ادراة_الملاك_v6.9_online.html')
    update_search_table_row('e:/Antigravity projects/HR Admin/نظام_ادراة_الملاك_v6.9.html')
