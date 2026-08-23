with open('e:/Antigravity projects/HR Admin/index.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i, line in enumerate(lines):
    if '<option value="استراحة ذوي الاحتياجات الخاصة"' in line:
        indent = line[:line.find('<')]
        extra_options = [
            f'{indent}<option value="ورقة عمل" className="bg-white text-emerald-700 font-bold">📝 ورقة عمل</option>\n',
            f'{indent}<option value="تعذر حضور (قطع طرق / ظرف طارئ)" className="bg-white text-amber-800 font-bold">🚧 تعذر حضور (قطع طرق / ظرف طارئ)</option>\n',
            f'{indent}<option value="توقف موقع (قوة قاهرة)" className="bg-white text-orange-900 font-bold">🛑 توقف موقع (قوة قاهرة)</option>\n'
        ]
        lines[i:i] = extra_options
        print(f"✓ Injected extra options before line {i+1}")
        break

# Update statusBadgeColor
for i, line in enumerate(lines):
    if "else if (status.includes('دورة'))" in line:
        indent = line[:line.find('else')]
        extra_badges = [
            f"{indent}else if (status === 'ورقة عمل') statusBadgeColor = 'bg-emerald-50 text-emerald-800 border-emerald-300 hover:bg-emerald-100 font-bold';\n",
            f"{indent}else if (status.includes('تعذر') || status.includes('توقف موقع')) statusBadgeColor = 'bg-amber-100 text-amber-900 border-amber-300 hover:bg-amber-200 font-bold';\n"
        ]
        lines[i:i] = extra_badges
        print(f"✓ Injected extra badges before line {i+1}")
        break

with open('e:/Antigravity projects/HR Admin/index.html', 'w', encoding='utf-8') as f:
    f.writelines(lines)

with open('e:/Antigravity projects/HR Admin/نظام_ادراة_الملاك_v7.5_cloud.html', 'w', encoding='utf-8') as f:
    f.writelines(lines)

print("✓ Successfully updated files with exact line insertion!")
