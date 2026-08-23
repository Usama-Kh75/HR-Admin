import os

with open('e:/Antigravity projects/HR Admin/index.html', 'r', encoding='utf-8') as f:
    code = f.read()

# 1. Update dropdown options in lines 6146-6160
old_options_block = """                                                                                         <option value="استراحة ذوي الاحتياجات الخاصة" className="bg-white text-teal-800 font-bold">♿ استراحة ذوي الاحتياجات الخاصة</option>
                                                                                         <option value="غياب" className="bg-white text-red-700 font-bold">❌ غياب</option>"""

new_options_block = """                                                                                         <option value="ورقة عمل" className="bg-white text-emerald-700 font-bold">📝 ورقة عمل</option>
                                                                                         <option value="تعذر حضور (قطع طرق / ظرف طارئ)" className="bg-white text-amber-800 font-bold">🚧 تعذر حضور (قطع طرق / ظرف طارئ)</option>
                                                                                         <option value="توقف موقع (قوة قاهرة)" className="bg-white text-orange-900 font-bold">🛑 توقف موقع (قوة قاهرة)</option>
                                                                                         <option value="استراحة ذوي الاحتياجات الخاصة" className="bg-white text-teal-800 font-bold">♿ استراحة ذوي الاحتياجات الخاصة</option>
                                                                                         <option value="غياب" className="bg-white text-red-700 font-bold">❌ غياب</option>"""

if old_options_block in code:
    code = code.replace(old_options_block, new_options_block, 1)
    print("✓ Successfully injected 'ورقة عمل' and 'تعذر حضور' to status select dropdown")

# 2. Update statusBadgeColor in lines 6110-6117
old_badge_block = """                                                                         else if (status.includes('دورة')) statusBadgeColor = 'bg-indigo-50 text-indigo-700 border-indigo-200 hover:bg-indigo-100';
                                                                         else if (status === 'غياب') statusBadgeColor = 'bg-red-600 text-white border-red-600 hover:bg-red-700';"""

new_badge_block = """                                                                         else if (status === 'ورقة عمل') statusBadgeColor = 'bg-emerald-50 text-emerald-800 border-emerald-300 hover:bg-emerald-100 font-bold';
                                                                         else if (status.includes('تعذر') || status.includes('توقف موقع')) statusBadgeColor = 'bg-amber-100 text-amber-900 border-amber-300 hover:bg-amber-200 font-bold';
                                                                         else if (status.includes('دورة')) statusBadgeColor = 'bg-indigo-50 text-indigo-700 border-indigo-200 hover:bg-indigo-100';
                                                                         else if (status === 'غياب') statusBadgeColor = 'bg-red-600 text-white border-red-600 hover:bg-red-700';"""

if old_badge_block in code:
    code = code.replace(old_badge_block, new_badge_block, 1)
    print("✓ Successfully added badge colors for 'ورقة عمل' and 'تعذر حضور'")

with open('e:/Antigravity projects/HR Admin/index.html', 'w', encoding='utf-8') as f:
    f.write(code)

with open('e:/Antigravity projects/HR Admin/نظام_ادراة_الملاك_v7.5_cloud.html', 'w', encoding='utf-8') as f:
    f.write(code)

print("✓ Completed add_work_paper_and_inaccessible.py")
