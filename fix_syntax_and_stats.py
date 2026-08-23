with open('e:/Antigravity projects/HR Admin/index.html', 'r', encoding='utf-8') as f:
    code = f.read()

# 1. Fix lines 1580-1596 statistics calculation
broken_stats = """                            if (status === 'دوام صباحي' || status === 'حضور فعلي' || status === 'دوام صباحي (12 ساعة)' || status === 'دوام مسائي (12 ساعة)' || status === 'دوام 24 ساعة' || status === 'إجازة زمنية') {
                                regularDuty++;
                            } else if (status === 'دوام إضافي' || status.includes('إضافي')) {
                                overtimeDuty++;
                            } else if (status.includes('إجازة اعتيادية') || status.includes('مرضية') || status.includes('خارج العراق') || isLongOrMaternityLeave(status)) {
                                leaves++;
                            } else if (status === 'ورقة عمل') statusBadgeColor = 'bg-emerald-50 text-emerald-800 border-emerald-300 hover:bg-emerald-100 font-bold';
                            } else if (status.includes('تعذر') || status.includes('توقف موقع')) statusBadgeColor = 'bg-amber-100 text-amber-900 border-amber-300 hover:bg-amber-200 font-bold';
                            } else if (status.includes('دورة')) {"""

clean_stats = """                            if (status === 'دوام صباحي' || status === 'حضور فعلي' || status === 'دوام صباحي (12 ساعة)' || status === 'دوام مسائي (12 ساعة)' || status === 'دوام 24 ساعة' || status === 'إجازة زمنية' || status === 'ورقة عمل') {
                                regularDuty++;
                            } else if (status === 'دوام إضافي' || status.includes('إضافي')) {
                                overtimeDuty++;
                            } else if (status.includes('إجازة اعتيادية') || status.includes('مرضية') || status.includes('خارج العراق') || isLongOrMaternityLeave(status)) {
                                leaves++;
                            } else if (status.includes('تعذر') || status.includes('توقف موقع')) {
                                rest++;
                            } else if (status.includes('دورة')) {"""

if broken_stats in code:
    code = code.replace(broken_stats, clean_stats)
    print("✓ Fixed statistics calculation for 'ورقة عمل' and 'تعذر حضور'")

# 2. Add badge colors in UI around line 6115
old_badge_ui = """                                                                        else if (status.includes('دورة')) statusBadgeColor = 'bg-indigo-50 text-indigo-700 border-indigo-200 hover:bg-indigo-100';"""

new_badge_ui = """                                                                        else if (status === 'ورقة عمل') statusBadgeColor = 'bg-emerald-50 text-emerald-800 border-emerald-300 hover:bg-emerald-100 font-bold';
                                                                        else if (status.includes('تعذر') || status.includes('توقف موقع')) statusBadgeColor = 'bg-amber-100 text-amber-900 border-amber-300 hover:bg-amber-200 font-bold';
                                                                        else if (status.includes('دورة')) statusBadgeColor = 'bg-indigo-50 text-indigo-700 border-indigo-200 hover:bg-indigo-100';"""

if old_badge_ui in code:
    code = code.replace(old_badge_ui, new_badge_ui)
    print("✓ Fixed UI badge colors")

with open('e:/Antigravity projects/HR Admin/index.html', 'w', encoding='utf-8') as f:
    f.write(code)

with open('e:/Antigravity projects/HR Admin/نظام_ادراة_الملاك_v7.5_cloud.html', 'w', encoding='utf-8') as f:
    f.write(code)
