import os

def update_file(file_path):
    if not os.path.exists(file_path):
        print(f"File not found: {file_path}")
        return False

    with open(file_path, 'r', encoding='utf-8') as f:
        code = f.read()

    old_dropdown_div = '<div className="absolute z-50 mt-1 w-64 bg-white border border-slate-200 rounded-xl shadow-2xl p-2.5 space-y-1.5 text-xs animate-fadeInUp">'
    new_dropdown_div = '<div className="absolute z-50 mt-1 w-64 bg-white border border-slate-200 rounded-xl shadow-2xl p-2.5 text-xs animate-fadeInUp max-h-56 overflow-y-auto space-y-1.5 scrollbar-thin">'

    if old_dropdown_div in code:
        code = code.replace(old_dropdown_div, new_dropdown_div)
        print(f"✓ Added scrollbar and max height to dropdown in {file_path}")
    else:
        print(f"Dropdown div target not found in {file_path}")

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(code)
    return True

if __name__ == '__main__':
    update_file('e:/Antigravity projects/HR Admin/index.html')
    update_file('e:/Antigravity projects/HR Admin/نظام_ادراة_الملاك_v6.8_online.html')
    update_file('e:/Antigravity projects/HR Admin/نظام_ادراة_الملاك_v6.8.html')
