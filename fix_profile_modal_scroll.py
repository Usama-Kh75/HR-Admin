import os

def update_file(file_path):
    if not os.path.exists(file_path):
        print(f"File not found: {file_path}")
        return False

    with open(file_path, 'r', encoding='utf-8') as f:
        code = f.read()

    # 1. Update Profile Card Modal container to fix max-height, overflow, and flex layout
    old_modal_container = """            {/* نافذة معاينة وبطاقة ملف المنتسب الفاخرة قبل الطباعة مع خيارات التخصيص والإخفاء والإظهار */}
            {selectedEmployeeCard && (
                <div className="fixed inset-0 bg-slate-950/80 backdrop-blur-md z-50 flex items-center justify-center p-4 print:p-0 print:bg-white print:static">
                    <div className="bg-white rounded-3xl shadow-2xl border border-slate-100 max-w-2xl w-full overflow-hidden animate-fadeInUp print:shadow-none print:border-none print:max-w-none print:w-full">"""

    new_modal_container = """            {/* نافذة معاينة وبطاقة ملف المنتسب الفاخرة قبل الطباعة مع خيارات التخصيص والإخفاء والإظهار */}
            {selectedEmployeeCard && (
                <div className="fixed inset-0 bg-slate-950/80 backdrop-blur-md z-50 flex items-center justify-center p-3 sm:p-4 print:p-0 print:bg-white print:static">
                    <div className="bg-white rounded-3xl shadow-2xl border border-slate-100 max-w-2xl w-full max-h-[92vh] flex flex-col overflow-hidden animate-fadeInUp print:shadow-none print:border-none print:max-w-none print:w-full print:max-h-none">"""

    if old_modal_container in code:
        code = code.replace(old_modal_container, new_modal_container)
        print(f"✓ Updated Modal outer container flex layout in {file_path}")

    # 2. Make Header flex-shrink-0 so top close button never disappears
    old_header = """                        {/* Header */}
                        <div className="bg-gradient-to-r from-blue-900 via-indigo-900 to-slate-900 p-6 text-white relative flex justify-between items-start print:bg-none print:text-slate-900 print:border-b-2 print:border-slate-800 print:p-4">"""

    new_header = """                        {/* Header */}
                        <div className="bg-gradient-to-r from-blue-900 via-indigo-900 to-slate-900 p-5 sm:p-6 text-white relative flex justify-between items-start flex-shrink-0 print:bg-none print:text-slate-900 print:border-b-2 print:border-slate-800 print:p-4">"""

    if old_header in code:
        code = code.replace(old_header, new_header)
        print(f"✓ Fixed Modal header flex-shrink-0 in {file_path}")

    # 3. Make Details Body scrollable (flex-1 overflow-y-auto)
    old_body = """                        {/* Card Details Grid */}
                        <div className="p-6 space-y-5 text-slate-800 text-xs">"""

    new_body = """                        {/* Card Details Grid */}
                        <div className="p-5 sm:p-6 space-y-5 text-slate-800 text-xs flex-1 overflow-y-auto scrollbar-thin">"""

    if old_body in code:
        code = code.replace(old_body, new_body)
        print(f"✓ Made Modal body scrollable in {file_path}")

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(code)
    return True

if __name__ == '__main__':
    update_file('e:/Antigravity projects/HR Admin/index.html')
    update_file('e:/Antigravity projects/HR Admin/نظام_ادراة_الملاك_v7.0_online.html')
    update_file('e:/Antigravity projects/HR Admin/نظام_ادراة_الملاك_v7.0.html')
