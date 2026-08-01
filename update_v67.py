import re
import os

with open('نظام_ادراة_الملاك_v6.5.html', 'r', encoding='utf-8') as f:
    code = f.read()

# 1. Update Version strings to v6.7 Beta
code = code.replace('<title>نظام إدارة الملاك - الإصدار v6.5 Beta</title>', '<title>نظام إدارة الملاك - الإصدار v6.7 Beta</title>')
code = code.replace("version: 'v6.5 Beta',", "version: 'v6.7 Beta',")
code = code.replace('v6.5 Beta  Beta', 'v6.7 Beta')
code = code.replace('v6.5 Beta', 'v6.7 Beta')
code = code.replace('الإصدار v6.5 Beta', 'الإصدار v6.7 Beta')
code = code.replace('v6.6 Beta', 'v6.7 Beta')

# 2. Add dataEntryOperator state & period report state variables inside App component
state_insertion_point = "const [pendingShiftConfirm, setPendingShiftConfirm] = useState(null);"
v67_states_code = """const [pendingShiftConfirm, setPendingShiftConfirm] = useState(null);
            
            // ===== منظم الموقف ومدخل البيانات =====
            const [dataEntryOperator, setDataEntryOperator] = useState(() => {
                return localStorage.getItem('dataEntryOperator') || 'م. أسامة خليل هاشم';
            });
            React.useEffect(() => {
                localStorage.setItem('dataEntryOperator', dataEntryOperator);
            }, [dataEntryOperator]);

            // ===== موقف الفترة (من - إلى) =====
            const [periodStartDate, setPeriodStartDate] = useState(() => {
                const today = new Date();
                const year = today.getFullYear();
                const month = String(today.getMonth() + 1).padStart(2, '0');
                return `${year}-${month}-01`;
            });
            const [periodEndDate, setPeriodEndDate] = useState(() => {
                const today = new Date();
                const year = today.getFullYear();
                const month = today.getMonth() + 1;
                const lastDay = new Date(year, month, 0).getDate();
                return `${year}-${String(month).padStart(2, '0')}-${String(lastDay).padStart(2, '0')}`;
            });
            const [periodUnitFilter, setPeriodUnitFilter] = useState('all');
            const [periodSearchQuery, setPeriodSearchQuery] = useState('');
            const [expandedEmpPeriod, setExpandedEmpPeriod] = useState(null);

            const setPeriodPreset = (preset) => {
                const today = new Date();
                const year = today.getFullYear();
                const month = today.getMonth();
                
                if (preset === 'currentMonth') {
                    const start = `${year}-${String(month + 1).padStart(2, '0')}-01`;
                    const lastDay = new Date(year, month + 1, 0).getDate();
                    const end = `${year}-${String(month + 1).padStart(2, '0')}-${String(lastDay).padStart(2, '0')}`;
                    setPeriodStartDate(start);
                    setPeriodEndDate(end);
                } else if (preset === 'prevMonth') {
                    const pDate = new Date(year, month - 1, 1);
                    const pYear = pDate.getFullYear();
                    const pMonth = pDate.getMonth();
                    const start = `${pYear}-${String(pMonth + 1).padStart(2, '0')}-01`;
                    const lastDay = new Date(pYear, pMonth + 1, 0).getDate();
                    const end = `${pYear}-${String(pMonth + 1).padStart(2, '0')}-${String(lastDay).padStart(2, '0')}`;
                    setPeriodStartDate(start);
                    setPeriodEndDate(end);
                } else if (preset === 'last7') {
                    const endD = new Date();
                    const startD = new Date();
                    startD.setDate(endD.getDate() - 6);
                    setPeriodStartDate(`${startD.getFullYear()}-${String(startD.getMonth() + 1).padStart(2, '0')}-${String(startD.getDate()).padStart(2, '0')}`);
                    setPeriodEndDate(`${endD.getFullYear()}-${String(endD.getMonth() + 1).padStart(2, '0')}-${String(endD.getDate()).padStart(2, '0')}`);
                } else if (preset === 'last30') {
                    const endD = new Date();
                    const startD = new Date();
                    startD.setDate(endD.getDate() - 29);
                    setPeriodStartDate(`${startD.getFullYear()}-${String(startD.getMonth() + 1).padStart(2, '0')}-${String(startD.getDate()).padStart(2, '0')}`);
                    setPeriodEndDate(`${endD.getFullYear()}-${String(endD.getMonth() + 1).padStart(2, '0')}-${String(endD.getDate()).padStart(2, '0')}`);
                }
            };"""

if state_insertion_point in code:
    code = code.replace(state_insertion_point, v67_states_code, 1)

# 3. Update dailyStats calculation to include ONLY overtimeDuty
old_daily_stats = """            const dailyStats = useMemo(() => {
                let onDuty = 0;
                let morningOnDuty = 0;
                let dayShift12h = 0;
                let nightShift12h = 0;
                let shift24h = 0;
                let rest = 0;
                let off = 0;
                
                staff.forEach(s => {
                    const status = getEmployeeDailyStatus(s, dailyReportDate);
                    if (status === 'دوام صباحي' || status === 'حضور فعلي') {
                        onDuty++;
                        morningOnDuty++;
                    } else if (status === 'دوام صباحي (12 ساعة)') {
                        onDuty++;
                        dayShift12h++;
                    } else if (status === 'دوام مسائي (12 ساعة)') {
                        onDuty++;
                        nightShift12h++;
                    } else if (status === 'دوام 24 ساعة') {
                        onDuty++;
                        shift24h++;
                    } else if (status.includes('استراحة')) {
                        rest++;
                    } else if (status.includes('إجازة') || status.includes('غياب') || status.includes('دورة') || status.includes('إيفاد') || status.includes('مرضية') || status.includes('زمنية')) {
                        off++;
                    }
                });
                
                return { onDuty, morningOnDuty, dayShift12h, nightShift12h, shift24h, rest, off };
            }, [staff, dailyReportDate, dailyStatusOverrides, anchorDate, threeShiftAnchorSquad, twoShiftAnchorSquad]);"""

new_daily_stats = """            const dailyStats = useMemo(() => {
                let onDuty = 0;
                let morningOnDuty = 0;
                let dayShift12h = 0;
                let nightShift12h = 0;
                let shift24h = 0;
                let overtimeDuty = 0;
                let rest = 0;
                let off = 0;
                
                staff.forEach(s => {
                    const status = getEmployeeDailyStatus(s, dailyReportDate);
                    if (status === 'دوام صباحي' || status === 'حضور فعلي') {
                        onDuty++;
                        morningOnDuty++;
                    } else if (status === 'دوام صباحي (12 ساعة)') {
                        onDuty++;
                        dayShift12h++;
                    } else if (status === 'دوام مسائي (12 ساعة)') {
                        onDuty++;
                        nightShift12h++;
                    } else if (status === 'دوام 24 ساعة') {
                        onDuty++;
                        shift24h++;
                    } else if (status === 'دوام إضافي' || status.includes('إضافي')) {
                        onDuty++;
                        overtimeDuty++;
                    } else if (status.includes('استراحة')) {
                        rest++;
                    } else if (status.includes('إجازة') || status.includes('غياب') || status.includes('دورة') || status.includes('إيفاد') || status.includes('مرضية') || status.includes('زمنية')) {
                        off++;
                    }
                });
                
                return { onDuty, morningOnDuty, dayShift12h, nightShift12h, shift24h, overtimeDuty, rest, off };
            }, [staff, dailyReportDate, dailyStatusOverrides, anchorDate, threeShiftAnchorSquad, twoShiftAnchorSquad]);"""

code = code.replace(old_daily_stats, new_daily_stats)

# 4. Add periodReportData calculation
period_calc_code = """
            const periodReportData = useMemo(() => {
                if (!periodStartDate || !periodEndDate) return { datesList: [], employees: [], summary: { totalStaff: 0, totalDutyDays: 0, totalOvertimeDays: 0, totalLeaveDays: 0, totalAbsenceDays: 0, totalDaysCount: 0 } };
                
                const datesList = [];
                try {
                    const pStart = periodStartDate.split('-');
                    const pEnd = periodEndDate.split('-');
                    let cur = new Date(parseInt(pStart[0]), parseInt(pStart[1]) - 1, parseInt(pStart[2]));
                    const end = new Date(parseInt(pEnd[0]), parseInt(pEnd[1]) - 1, parseInt(pEnd[2]));
                    
                    while (cur <= end) {
                        const y = cur.getFullYear();
                        const m = String(cur.getMonth() + 1).padStart(2, '0');
                        const d = String(cur.getDate()).padStart(2, '0');
                        datesList.push(`${y}-${m}-${d}`);
                        cur.setDate(cur.getDate() + 1);
                    }
                } catch (e) {
                    return { datesList: [], employees: [], summary: { totalStaff: 0, totalDutyDays: 0, totalOvertimeDays: 0, totalLeaveDays: 0, totalAbsenceDays: 0, totalDaysCount: 0 } };
                }

                let filteredStaff = staff.filter(s => {
                    if (isLongOrMaternityLeave(s.status)) return false;
                    if (periodUnitFilter !== 'all' && s.unit !== periodUnitFilter) return false;
                    if (periodSearchQuery.trim()) {
                        const normQ = normalizeArabicForSearch(periodSearchQuery);
                        const normName = normalizeArabicForSearch(s.name || '');
                        const normJobNum = (s.jobNumber || '').toString();
                        return normName.includes(normQ) || normJobNum.includes(normQ);
                    }
                    return true;
                });

                let totalDutyDaysSum = 0;
                let totalOvertimeDaysSum = 0;
                let totalLeaveDaysSum = 0;
                let totalAbsenceDaysSum = 0;

                const employeesResult = filteredStaff.map(emp => {
                    let regularDuty = 0;
                    let overtimeDuty = 0;
                    let leaves = 0;
                    let coursesOrDeputation = 0;
                    let absence = 0;
                    let rest = 0;
                    const dailyLog = [];

                    datesList.forEach(dateStr => {
                        const status = getEmployeeDailyStatus(emp, dateStr);
                        const dayName = getArabicDayName(dateStr);
                        const isOverride = dailyStatusOverrides[dateStr] && dailyStatusOverrides[dateStr][emp.id];
                        
                        dailyLog.push({ dateStr, dayName, status, isOverride: !!isOverride });

                        if (status === 'دوام صباحي' || status === 'حضور فعلي' || status === 'دوام صباحي (12 ساعة)' || status === 'دوام مسائي (12 ساعة)' || status === 'دوام 24 ساعة') {
                            regularDuty++;
                        } else if (status === 'دوام إضافي' || status.includes('إضافي')) {
                            overtimeDuty++;
                        } else if (status.includes('إجازة') || status.includes('مرضية') || status.includes('زمنية')) {
                            leaves++;
                        } else if (status.includes('دورة') || status.includes('إيفاد')) {
                            coursesOrDeputation++;
                        } else if (status === 'غياب') {
                            absence++;
                        } else if (status.includes('استراحة')) {
                            rest++;
                        }
                    });

                    totalDutyDaysSum += regularDuty;
                    totalOvertimeDaysSum += overtimeDuty;
                    totalLeaveDaysSum += leaves;
                    totalAbsenceDaysSum += absence;

                    return {
                        employee: emp,
                        totalDays: datesList.length,
                        regularDuty,
                        overtimeDuty,
                        leaves,
                        coursesOrDeputation,
                        absence,
                        rest,
                        dailyLog
                    };
                });

                return {
                    datesList,
                    employees: employeesResult,
                    summary: {
                        totalStaff: filteredStaff.length,
                        totalDutyDays: totalDutyDaysSum,
                        totalOvertimeDays: totalOvertimeDaysSum,
                        totalLeaveDays: totalLeaveDaysSum,
                        totalAbsenceDays: totalAbsenceDaysSum,
                        totalDaysCount: datesList.length
                    }
                };
            }, [staff, periodStartDate, periodEndDate, periodUnitFilter, periodSearchQuery, dailyStatusOverrides, anchorDate, threeShiftAnchorSquad, twoShiftAnchorSquad]);

            const exportPeriodReportExcel = () => {
                try {
                    const exportData = [];
                    let counter = 1;

                    periodReportData.employees.forEach(item => {
                        const emp = item.employee;
                        exportData.push({
                            type: 'data',
                            'ت': counter++,
                            'الاسم الكامل': getTripleName(emp.name),
                            'الرقم الوظيفي': emp.jobNumber || '',
                            'الوحدة': emp.unit || '',
                            'طبيعة العمل': emp.workType || '',
                            'الدوام الاعتيادي (يوم)': item.regularDuty,
                            'الدوام الإضافي (يوم)': item.overtimeDuty,
                            'الإجازات (يوم)': item.leaves,
                            'الدورات والإيفاد (يوم)': item.coursesOrDeputation,
                            'الغياب (يوم)': item.absence,
                            'أيام الاستراحة (يوم)': item.rest
                        });
                    });

                    setPreviewData(exportData);
                    setVisiblePreviewColumns(['الرقم الوظيفي', 'الوحدة', 'طبيعة العمل', 'الدوام الاعتيادي (يوم)', 'الدوام الإضافي (يوم)', 'الإجازات (يوم)', 'الغياب (يوم)']);
                    setPreviewTitle(`موقف الحضور الموحد للشعبة للفترة من ${periodStartDate} إلى ${periodEndDate}`);
                    setShowPreview(true);
                } catch (e) {
                    alert('❌ خطأ في تصدير موقف الفترة: ' + e.message);
                }
            };
"""

code = code.replace(new_daily_stats, new_daily_stats + period_calc_code)

# 5. Add new dropdown options: "إجازة خارج العراق", "إيفاد داخل العراق", "إيفاد خارج العراق"
new_select_options = """                                                                                        <option value="default" className="bg-white text-slate-800 font-bold">
                                                                                            ⚙️ الافتراضي ({status})
                                                                                        </option>
                                                                                        <option value="دوام إضافي" className="bg-white text-emerald-800 font-bold">⚡ دوام إضافي</option>
                                                                                        <option value="إجازة اعتيادية" className="bg-white text-rose-700 font-bold">🏖️ إجازة اعتيادية</option>
                                                                                        <option value="إجازة خارج العراق" className="bg-white text-cyan-800 font-bold">🌍 إجازة خارج العراق</option>
                                                                                        <option value="إجازة مرضية" className="bg-white text-rose-700 font-bold">🏥 إجازة مرضية</option>
                                                                                        <option value="إجازة زمنية" className="bg-white text-amber-700 font-bold">⏰ إجازة زمنية</option>
                                                                                        <option value="في دورة" className="bg-white text-indigo-700 font-bold">🎓 في دورة</option>
                                                                                        <option value="إيفاد داخل العراق" className="bg-white text-purple-700 font-bold">🇮🇶 إيفاد داخل العراق</option>
                                                                                        <option value="إيفاد خارج العراق" className="bg-white text-indigo-900 font-bold">🌐 إيفاد خارج العراق</option>"""

old_select_block = """                                                                                        <option value="default" className="bg-white text-slate-800 font-bold">
                                                                                            ⚙️ الافتراضي ({status})
                                                                                        </option>
                                                                                        <option value="إجازة اعتيادية" className="bg-white text-rose-700 font-bold">🏖️ إجازة اعتيادية</option>
                                                                                        <option value="إجازة مرضية" className="bg-white text-rose-700 font-bold">🏥 إجازة مرضية</option>
                                                                                        <option value="إجازة زمنية" className="bg-white text-amber-700 font-bold">⏰ إجازة زمنية</option>
                                                                                        <option value="في دورة" className="bg-white text-indigo-700 font-bold">🎓 في دورة</option>
                                                                                        <option value="إيفاد" className="bg-white text-purple-700 font-bold">✈️ إيفاد</option>"""

code = code.replace(old_select_block, new_select_options)

# 6. Add status badge color handling for new status values
old_badge_colors = """                                                                         if (status === 'دوام صباحي') statusBadgeColor = 'bg-blue-50 text-blue-700 border-blue-200 hover:bg-blue-100';
                                                                        else if (status === 'دوام صباحي (12 ساعة)') statusBadgeColor = 'bg-amber-50 text-amber-700 border-amber-200 hover:bg-amber-100';
                                                                        else if (status === 'دوام مسائي (12 ساعة)') statusBadgeColor = 'bg-indigo-900 text-indigo-100 border-indigo-900 hover:bg-indigo-800';
                                                                        else if (status === 'دوام 24 ساعة') statusBadgeColor = 'bg-purple-100 text-purple-800 border-purple-200 hover:bg-purple-200';
                                                                        else if (status.includes('استراحة')) statusBadgeColor = 'bg-slate-100 text-slate-600 border-slate-200 hover:bg-slate-200';"""

new_badge_colors = """                                                                         if (status === 'دوام صباحي') statusBadgeColor = 'bg-blue-50 text-blue-700 border-blue-200 hover:bg-blue-100';
                                                                        else if (status === 'دوام صباحي (12 ساعة)') statusBadgeColor = 'bg-amber-50 text-amber-700 border-amber-200 hover:bg-amber-100';
                                                                        else if (status === 'دوام مسائي (12 ساعة)') statusBadgeColor = 'bg-indigo-900 text-indigo-100 border-indigo-900 hover:bg-indigo-800';
                                                                        else if (status === 'دوام 24 ساعة') statusBadgeColor = 'bg-purple-100 text-purple-800 border-purple-200 hover:bg-purple-200';
                                                                        else if (status === 'دوام إضافي' || status.includes('إضافي')) statusBadgeColor = 'bg-emerald-100 text-emerald-800 border-emerald-300 hover:bg-emerald-200';
                                                                        else if (status === 'إجازة خارج العراق') statusBadgeColor = 'bg-cyan-100 text-cyan-900 border-cyan-300 hover:bg-cyan-200';
                                                                        else if (status === 'إيفاد داخل العراق' || status === 'إيفاد') statusBadgeColor = 'bg-purple-100 text-purple-800 border-purple-300 hover:bg-purple-200';
                                                                        else if (status === 'إيفاد خارج العراق') statusBadgeColor = 'bg-indigo-100 text-indigo-900 border-indigo-300 hover:bg-indigo-200';
                                                                        else if (status.includes('استراحة')) statusBadgeColor = 'bg-slate-100 text-slate-600 border-slate-200 hover:bg-slate-200';"""

code = code.replace(old_badge_colors, new_badge_colors)

# 7. Add overtime card & dataEntryOperator input in header
old_stats_grid = """                                             <div className="bg-white rounded-xl shadow-sm border border-slate-100 p-4 text-center">
                                                 <div className="text-2xl mb-1">🕒</div>
                                                 <div className="text-[10px] font-bold text-slate-400">مناوب 24 ساعة</div>
                                                 <div className="text-xl font-black text-purple-600 mt-1">{dailyStats.shift24h} موظف</div>
                                             </div>"""

new_stats_grid = """                                             <div className="bg-white rounded-xl shadow-sm border border-slate-100 p-4 text-center">
                                                 <div className="text-2xl mb-1">🕒</div>
                                                 <div className="text-[10px] font-bold text-slate-400">مناوب 24 ساعة</div>
                                                 <div className="text-xl font-black text-purple-600 mt-1">{dailyStats.shift24h} موظف</div>
                                             </div>
                                             <div className="bg-white rounded-xl shadow-sm border border-slate-100 p-4 text-center">
                                                 <div className="text-2xl mb-1">⚡</div>
                                                 <div className="text-[10px] font-bold text-slate-400">دوام إضافي</div>
                                                 <div className="text-xl font-black text-emerald-600 mt-1">{dailyStats.overtimeDuty || 0} موظف</div>
                                             </div>"""

code = code.replace(old_stats_grid, new_stats_grid)

# Add Data Entry Operator Name Input in the Date Picker Controls Row
old_date_picker_grid = """                                            <div className="p-6 bg-slate-50/50 border-b border-slate-100 grid grid-cols-1 md:grid-cols-12 gap-5 items-end">
                                                {/* منتقي التاريخ */}
                                                <div className="md:col-span-6 space-y-2">
                                                    <label className="block text-xs font-black text-slate-700">📅 تاريخ الموقف اليومي (انقر للأسهم للتنقل السريع بين الأيام):</label>
                                                    <div className="flex items-center gap-2">
                                                        <button
                                                            onClick={() => changeReportDateByDays(-1)}
                                                            className="px-3.5 py-2.5 bg-slate-800 hover:bg-slate-900 text-amber-400 font-black rounded-xl text-xs transition cursor-pointer border border-slate-700 shadow-sm active:scale-95 whitespace-nowrap flex items-center gap-1.5"
                                                            title="اليوم السابق"
                                                        >
                                                            <span>◀️</span>
                                                            <span>اليوم السابق</span>
                                                        </button>

                                                        <div className="relative flex-1 bg-white border-2 border-slate-300 rounded-xl px-3 py-2 shadow-sm focus-within:border-teal-500 flex items-center gap-2">
                                                            <span className="text-slate-400 text-base">📅</span>
                                                            <input 
                                                                type="date"
                                                                value={dailyReportDate}
                                                                onChange={(e) => setDailyReportDate(e.target.value)}
                                                                className="w-full outline-none font-black text-slate-800 text-sm bg-transparent cursor-pointer font-mono"
                                                            />
                                                        </div>

                                                        <button
                                                            onClick={() => changeReportDateByDays(1)}
                                                            className="px-3.5 py-2.5 bg-slate-800 hover:bg-slate-900 text-amber-400 font-black rounded-xl text-xs transition cursor-pointer border border-slate-700 shadow-sm active:scale-95 whitespace-nowrap flex items-center gap-1.5"
                                                            title="اليوم التالي"
                                                        >
                                                            <span>اليوم التالي</span>
                                                            <span>▶️</span>
                                                        </button>
                                                    </div>
                                                </div>"""

new_date_picker_grid = """                                            <div className="p-6 bg-slate-50/50 border-b border-slate-100 grid grid-cols-1 md:grid-cols-12 gap-4 items-end">
                                                {/* منتقي التاريخ - يمين في RTL */}
                                                <div className="md:col-span-5 space-y-1.5">
                                                    <label className="block text-xs font-black text-slate-700">📅 تاريخ الموقف اليومي (التنقل بين الأيام):</label>
                                                    <div className="flex items-center gap-1.5">
                                                        <button
                                                            onClick={() => changeReportDateByDays(-1)}
                                                            className="px-3 py-2 bg-slate-800 hover:bg-slate-900 text-amber-400 font-black rounded-xl text-xs transition cursor-pointer border border-slate-700 shadow-sm active:scale-95 whitespace-nowrap flex items-center gap-1"
                                                            title="اليوم السابق"
                                                        >
                                                            <span>◀️</span>
                                                            <span>السابق</span>
                                                        </button>

                                                        <div className="relative flex-1 bg-white border-2 border-slate-300 rounded-xl px-2.5 py-1.5 shadow-sm focus-within:border-teal-500 flex items-center gap-1.5">
                                                            <span className="text-slate-400 text-sm">📅</span>
                                                            <input 
                                                                type="date"
                                                                value={dailyReportDate}
                                                                onChange={(e) => setDailyReportDate(e.target.value)}
                                                                className="w-full outline-none font-black text-slate-800 text-xs md:text-sm bg-transparent cursor-pointer font-mono"
                                                            />
                                                        </div>

                                                        <button
                                                            onClick={() => changeReportDateByDays(1)}
                                                            className="px-3 py-2 bg-slate-800 hover:bg-slate-900 text-amber-400 font-black rounded-xl text-xs transition cursor-pointer border border-slate-700 shadow-sm active:scale-95 whitespace-nowrap flex items-center gap-1"
                                                            title="اليوم التالي"
                                                        >
                                                            <span>التالي</span>
                                                            <span>▶️</span>
                                                        </button>
                                                    </div>
                                                </div>

                                                {/* اسم منظم الموقف / مدخل البيانات */}
                                                <div className="md:col-span-3 space-y-1.5">
                                                    <label className="block text-xs font-black text-slate-700">👤 اسم منظم الموقف / مدخل البيانات:</label>
                                                    <div className="bg-white border-2 border-slate-300 rounded-xl px-3 py-1.5 shadow-sm flex items-center gap-1.5 focus-within:border-teal-500">
                                                        <span className="text-slate-400 text-sm">✍️</span>
                                                        <input 
                                                            type="text" 
                                                            value={dataEntryOperator} 
                                                            onChange={(e) => setDataEntryOperator(e.target.value)} 
                                                            placeholder="منظم الموقف..." 
                                                            className="w-full outline-none font-bold text-slate-800 text-xs md:text-sm bg-transparent"
                                                        />
                                                    </div>
                                                </div>

                                                {/* زر محرك تقارير موقف الفترة - يسار في RTL */}
                                                <div className="md:col-span-4 space-y-1.5">
                                                    <label className="block text-xs font-black text-blue-800">📊 موقف فترة زمنية (من - إلى):</label>
                                                    <button 
                                                        onClick={() => setUnitsSubView('periodReport')}
                                                        className="w-full px-4 py-2 bg-gradient-to-r from-blue-600 via-indigo-600 to-purple-600 hover:from-blue-700 hover:to-indigo-700 text-white font-black rounded-xl text-xs md:text-sm shadow-md transition active:scale-95 flex items-center justify-center gap-1.5 cursor-pointer border-2 border-blue-300"
                                                    >
                                                        <span>📊</span>
                                                        <span>محرك تقارير موقف الفترة (من - إلى)</span>
                                                    </button>
                                                </div>"""

code = code.replace(old_date_picker_grid, new_date_picker_grid)

# 8. SIGNATURES MOVED DOWN BY 2 MORE CELLS (~210px margin-top) AND FOOTER MOVED DOWN PROPORTIONALLY (~240px margin-top)
old_preview_table_end = """                                    </table>
                                </div>
                                
                                <div className="preview-footer">"""

new_preview_table_end = """                                    </table>

                                    {/* قسم عناوين التوقيعات النظيفة نُزلت لأسفل بمقدار خليتين إضافيتين (إجمالي 6 خلايا تحت الجدول) */}
                                    <div className="preview-signatures-row mt-52 mb-14 px-12 flex justify-between items-center text-slate-950 font-black text-sm md:text-base">
                                        <div className="text-right">
                                            <p className="font-black text-base md:text-lg text-slate-950">مسؤول الإدارة</p>
                                        </div>
                                        <div className="text-left">
                                            <p className="font-black text-base md:text-lg text-slate-950">مسؤول الشعبة</p>
                                        </div>
                                    </div>

                                    {/* تذييل الورقة نزلت بنفس المقدار التناسبي أسفل التوقيعات بخط أصغر في نهاية الورقة */}
                                    <div className="preview-page-footer pt-3 mt-48 border-t border-slate-300 flex justify-between items-center text-[10px] text-slate-700 font-bold px-2">
                                        <span>منظم الموقف: <strong className="text-slate-950 font-black">{dataEntryOperator || '....................'}</strong></span>
                                        <span>تاريخ الطباعة والتنظيم: <strong className="text-slate-950 font-black font-mono">{new Date().toLocaleDateString('ar-EG', { year: 'numeric', month: '2-digit', day: '2-digit' })}</strong> ({new Date().toISOString().split('T')[0]})</span>
                                    </div>
                                </div>
                                
                                <div className="preview-footer">"""

code = code.replace(old_preview_table_end, new_preview_table_end)

# Also update explicit CSS rules for print: margin-top for signatures = 210px, for footer = 240px
old_print_style = """        @media print {
            body { font-size: 12px; }
            .no-print { display: none !important; }
            .print-only { display: block !important; }
            .page-break { page-break-before: always; }
        }"""

new_print_style = """        @media print {
            @page {
                size: A4 portrait;
                margin: 8mm 6mm;
            }
            body { 
                font-size: 10.5px !important; 
                -webkit-print-color-adjust: exact !important;
                print-color-adjust: exact !important;
            }
            .no-print { display: none !important; }
            .print-only { display: block !important; }
            .page-break { page-break-before: always; }
            table {
                font-size: 10.5px !important;
                width: 100% !important;
                border-collapse: collapse !important;
                table-layout: auto !important;
            }
            th, td {
                padding: 4px 5px !important;
                font-size: 10.5px !important;
                line-height: 1.3 !important;
                word-break: break-word !important;
                overflow-wrap: break-word !important;
            }
            th {
                font-weight: 900 !important;
                background-color: #f1f5f9 !important;
            }
            .preview-signatures-row {
                display: flex !important;
                justify-content: space-between !important;
                align-items: center !important;
                margin-top: 210px !important;
                margin-bottom: 35px !important;
                padding-left: 50px !important;
                padding-right: 50px !important;
                page-break-inside: avoid !important;
            }
            .preview-page-footer {
                display: flex !important;
                justify-content: space-between !important;
                align-items: center !important;
                border-top: 1px solid #94a3b8 !important;
                padding-top: 8px !important;
                margin-top: 240px !important;
                font-size: 8.5pt !important;
                color: #1e293b !important;
                page-break-inside: avoid !important;
            }
        }"""

code = code.replace(old_print_style, new_print_style)

# 9. UPDATE NEW EMPLOYEE REGISTRATION FORM: REMOVE "طبيعة العمل" AND ADD "هاتف أحد الذوي"
old_new_emp_form_block = """                                        <div className="border-b border-gray-400 pb-1 flex items-center col-span-2">
                                            <span className="font-bold text-gray-800 min-w-[100px]">طبيعة العمل:</span>
                                            <div className="flex gap-8 mr-4">
                                                <span className="flex items-center gap-2">
                                                    <span className="inline-block w-4 h-4 border border-black rounded"></span>
                                                    <span>صباحي</span>
                                                </span>
                                                <span className="flex items-center gap-2">
                                                    <span className="inline-block w-4 h-4 border border-black rounded"></span>
                                                    <span>مناوب</span>
                                                </span>
                                            </div>
                                        </div>

                                        <div className="border-b border-gray-400 pb-1 flex items-center col-span-2">
                                            <span className="font-bold text-gray-800 min-w-[100px]">الجنس:</span>
                                            <div className="flex gap-8 mr-4">
                                                <span className="flex items-center gap-2">
                                                    <span className="inline-block w-4 h-4 border border-black rounded"></span>
                                                    <span>ذكر</span>
                                                </span>
                                                <span className="flex items-center gap-2">
                                                    <span className="inline-block w-4 h-4 border border-black rounded"></span>
                                                    <span>أنثى</span>
                                                </span>
                                            </div>
                                        </div>"""

new_new_emp_form_block = """                                        <div className="border-b border-gray-400 pb-1 flex items-center">
                                            <span className="font-bold text-gray-800 min-w-[100px]">الجنس:</span>
                                            <div className="flex gap-8 mr-4">
                                                <span className="flex items-center gap-2">
                                                    <span className="inline-block w-4 h-4 border border-black rounded"></span>
                                                    <span>ذكر</span>
                                                </span>
                                                <span className="flex items-center gap-2">
                                                    <span className="inline-block w-4 h-4 border border-black rounded"></span>
                                                    <span>أنثى</span>
                                                </span>
                                            </div>
                                        </div>
                                        
                                        <div className="border-b border-gray-400 pb-1 flex items-baseline">
                                            <span className="font-bold text-gray-800 min-w-[120px]">هاتف أحد الذوي:</span>
                                            <span className="flex-1 text-gray-300">...........................................................................</span>
                                        </div>"""

code = code.replace(old_new_emp_form_block, new_new_emp_form_block)

# 10. FIX STICKY TOP OFFSET: SET top-[68px] SO BANNER STICKS CLEANLY BELOW THE MAIN NAV BAR WITH HIGH Z-INDEX (z-25)
old_unit_banner_block = """                                        {/* شريط أزرار الفلترة الكحلي والذهبي حسب الوحدات */}
                                        <div className="bg-slate-900 text-white p-4 rounded-2xl shadow-lg border border-slate-700 space-y-2.5 no-print my-4">
                                            <div className="flex justify-between items-center px-1">
                                                <span className="text-xs md:text-sm font-black text-amber-400 flex items-center gap-1.5">
                                                    <span>📍</span>
                                                    <span>اختر الوحدة لتصفية وتسجيل الموقف المباشر:</span>
                                                </span>
                                                <span className="text-[11px] text-slate-300 font-bold">
                                                    {selectedDailyUnitTab === 'all' ? 'عرض جميع الوحدات' : `وحدة: ${selectedDailyUnitTab}`}
                                                </span>
                                            </div>

                                            <div className="flex items-center gap-2 overflow-x-auto pb-1 scrollbar-thin">
                                                {[
                                                    { id: 'all', name: '🏢 كافة الوحدات', count: staff.length },
                                                    { id: 'مقر الشعبة', name: '📍 مقر الشعبة', count: staff.filter(s => s.unit === 'مقر الشعبة').length },
                                                    { id: 'تبريد باب الزبير', name: '❄️ باب الزبير', count: staff.filter(s => s.unit === 'تبريد باب الزبير').length },
                                                    { id: 'ورشة التبريد', name: '🔧 ورشة التبريد', count: staff.filter(s => s.unit === 'ورشة التبريد').length },
                                                    { id: 'تبريد المكينة', name: '🏭 تبريد المكينة', count: staff.filter(s => s.unit === 'تبريد المكينة').length },
                                                    { id: 'تبريد نهر بن عمر', name: '🌊 نهر بن عمر', count: staff.filter(s => s.unit === 'تبريد نهر بن عمر').length },
                                                    { id: 'تبريد المركز الثقافي', name: '🏛️ المركز الثقافي', count: staff.filter(s => s.unit === 'تبريد المركز الثقافي').length }
                                                ].map(u => {
                                                    const isActive = selectedDailyUnitTab === u.id;
                                                    return (
                                                        <button
                                                            key={u.id}
                                                            onClick={() => setSelectedDailyUnitTab(u.id)}
                                                            className={`py-2.5 px-4 rounded-xl font-black text-xs md:text-sm whitespace-nowrap transition cursor-pointer flex items-center gap-2 active:scale-95 shadow-sm ${
                                                                isActive
                                                                    ? 'bg-amber-400 text-slate-950 font-black ring-2 ring-amber-300 shadow-lg scale-105'
                                                                    : 'bg-slate-800 hover:bg-slate-700 text-slate-200 border border-slate-700'
                                                            }`}
                                                        >
                                                            <span>{u.name}</span>
                                                            <span className={`px-2 py-0.5 rounded-full text-xs font-black ${isActive ? 'bg-slate-950 text-amber-300' : 'bg-slate-900 text-slate-300'}`}>
                                                                {u.count}
                                                            </span>
                                                        </button>
                                                    );
                                                })}
                                            </div>
                                        </div>"""

new_unit_banner_block = """                                        {/* شريط أزرار الفلترة الكحلي والذهبي المجمد أسفل شريط التنقل الرئيسي تماماً (Sticky Header top-[68px]) */}
                                        <div className="sticky top-[68px] z-20 bg-slate-900 text-white p-3.5 rounded-2xl shadow-2xl border-2 border-slate-700 space-y-2 no-print my-4 transition-all">
                                            <div className="flex justify-between items-center px-1">
                                                <span className="text-xs md:text-sm font-black text-amber-400 flex items-center gap-1.5">
                                                    <span>📍</span>
                                                    <span>اختر الوحدة لتصفية وتسجيل الموقف المباشر:</span>
                                                </span>
                                                <span className="text-[11px] text-slate-300 font-bold">
                                                    {selectedDailyUnitTab === 'all' ? 'عرض جميع الوحدات' : `وحدة: ${selectedDailyUnitTab}`}
                                                </span>
                                            </div>

                                            <div className="flex items-center gap-2 overflow-x-auto pb-1 scrollbar-thin">
                                                {[
                                                    { id: 'all', name: '🏢 كافة الوحدات', count: staff.length },
                                                    { id: 'مقر الشعبة', name: '📍 مقر الشعبة', count: staff.filter(s => s.unit === 'مقر الشعبة').length },
                                                    { id: 'تبريد باب الزبير', name: '❄️ باب الزبير', count: staff.filter(s => s.unit === 'تبريد باب الزبير').length },
                                                    { id: 'ورشة التبريد', name: '🔧 ورشة التبريد', count: staff.filter(s => s.unit === 'ورشة التبريد').length },
                                                    { id: 'تبريد المكينة', name: '🏭 تبريد المكينة', count: staff.filter(s => s.unit === 'تبريد المكينة').length },
                                                    { id: 'تبريد نهر بن عمر', name: '🌊 نهر بن عمر', count: staff.filter(s => s.unit === 'تبريد نهر بن عمر').length },
                                                    { id: 'تبريد المركز الثقافي', name: '🏛️ المركز الثقافي', count: staff.filter(s => s.unit === 'تبريد المركز الثقافي').length }
                                                ].map(u => {
                                                    const isActive = selectedDailyUnitTab === u.id;
                                                    return (
                                                        <button
                                                            key={u.id}
                                                            onClick={() => {
                                                                setSelectedDailyUnitTab(u.id);
                                                                // الانتقال والتمركز التلقائي السلس لبداية أسماء الوحدة
                                                                window.scrollTo({ top: 340, behavior: 'smooth' });
                                                            }}
                                                            className={`py-2 px-3.5 rounded-xl font-black text-xs md:text-sm whitespace-nowrap transition cursor-pointer flex items-center gap-2 active:scale-95 shadow-sm ${
                                                                isActive
                                                                    ? 'bg-amber-400 text-slate-950 font-black ring-2 ring-amber-300 shadow-lg scale-105'
                                                                    : 'bg-slate-800 hover:bg-slate-700 text-slate-200 border border-slate-700'
                                                            }`}
                                                        >
                                                            <span>{u.name}</span>
                                                            <span className={`px-2 py-0.5 rounded-full text-xs font-black ${isActive ? 'bg-slate-950 text-amber-300' : 'bg-slate-900 text-slate-300'}`}>
                                                                {u.count}
                                                            </span>
                                                        </button>
                                                    );
                                                })}
                                            </div>
                                        </div>"""

code = code.replace(old_unit_banner_block, new_unit_banner_block)

# 11. Period Report UI insertion logic
old_subview_switch_end = """                                        </div>
                                    </div>
                                ) : (
                                    <div className="space-y-4">"""

period_view_ui = """                                        </div>
                                    </div>
                                ) : unitsSubView === 'periodReport' ? (
                                    <div className="space-y-6 animate-fadeIn">
                                        {/* شريط العنوان والتقرير الشامل للفترة */}
                                        <div className="bg-white rounded-2xl shadow-lg border border-slate-100 overflow-hidden">
                                            <div className="p-6 bg-gradient-to-r from-blue-600 via-indigo-600 to-purple-700 text-white flex flex-col md:flex-row justify-between items-start md:items-center gap-4">
                                                <div>
                                                    <h2 className="text-2xl font-black flex items-center gap-2">
                                                        <span>📊</span>
                                                        <span>محرك تقارير موقف الحضور والدوام للفترة المحددة</span>
                                                    </h2>
                                                    <p className="text-xs md:text-sm mt-1 text-blue-100 opacity-95 font-medium">
                                                        حدد الفترة الزمنية واضغط على استخراج الموقف لمعاينة وسجل إجازات ودورات وغياب ودواير المنتسبين للفترة
                                                    </p>
                                                </div>
                                                <div className="flex gap-2 flex-wrap w-full md:w-auto">
                                                    <button 
                                                        onClick={() => setUnitsSubView('dailyStatus')} 
                                                        className="bg-slate-800 hover:bg-slate-900 text-amber-400 border border-slate-700 px-4 py-2.5 rounded-xl font-bold text-xs md:text-sm shadow-md transition active:scale-95 flex items-center gap-1.5 flex-1 md:flex-initial justify-center cursor-pointer"
                                                    >
                                                        <span>📋</span>
                                                        <span>العودة للموقف اليومي</span>
                                                    </button>
                                                    <button 
                                                        onClick={exportPeriodReportExcel} 
                                                        className="bg-white text-indigo-700 hover:bg-blue-50 px-5 py-2.5 rounded-xl font-bold text-xs md:text-sm shadow-md transition active:scale-95 flex items-center gap-1.5 flex-1 md:flex-initial justify-center cursor-pointer"
                                                    >
                                                        <span>📊</span>
                                                        <span>معاينة وتصدير تقرير الفترة</span>
                                                    </button>
                                                </div>
                                            </div>

                                            {/* شريط التحكم بالفترة والفلترة */}
                                            <div className="p-6 bg-slate-50/70 border-b border-slate-200 space-y-4">
                                                <div className="grid grid-cols-1 md:grid-cols-12 gap-4 items-end">
                                                    {/* من تاريخ */}
                                                    <div className="md:col-span-3 space-y-1.5">
                                                        <label className="block text-xs font-black text-slate-700">📅 من تاريخ:</label>
                                                        <div className="relative bg-white border-2 border-slate-300 rounded-xl px-3 py-2 shadow-sm focus-within:border-indigo-500 flex items-center gap-2">
                                                            <span className="text-slate-400 text-base">🗓️</span>
                                                            <input 
                                                                type="date"
                                                                value={periodStartDate}
                                                                onChange={(e) => setPeriodStartDate(e.target.value)}
                                                                className="w-full outline-none font-black text-slate-800 text-sm bg-transparent cursor-pointer font-mono"
                                                            />
                                                        </div>
                                                    </div>

                                                    {/* إلى تاريخ */}
                                                    <div className="md:col-span-3 space-y-1.5">
                                                        <label className="block text-xs font-black text-slate-700">📅 إلى تاريخ:</label>
                                                        <div className="relative bg-white border-2 border-slate-300 rounded-xl px-3 py-2 shadow-sm focus-within:border-indigo-500 flex items-center gap-2">
                                                            <span className="text-slate-400 text-base">🏁</span>
                                                            <input 
                                                                type="date"
                                                                value={periodEndDate}
                                                                onChange={(e) => setPeriodEndDate(e.target.value)}
                                                                className="w-full outline-none font-black text-slate-800 text-sm bg-transparent cursor-pointer font-mono"
                                                            />
                                                        </div>
                                                    </div>

                                                    {/* فلتر الوحدة */}
                                                    <div className="md:col-span-3 space-y-1.5">
                                                        <label className="block text-xs font-black text-slate-700">📍 فلترة حسب الوحدة:</label>
                                                        <select
                                                            value={periodUnitFilter}
                                                            onChange={(e) => setPeriodUnitFilter(e.target.value)}
                                                            className="w-full bg-white border-2 border-slate-300 rounded-xl px-3 py-2 shadow-sm font-bold text-slate-800 text-xs md:text-sm outline-none cursor-pointer focus:border-indigo-500"
                                                        >
                                                            <option value="all">🏢 جميع الوحدات ({staff.length} موظف)</option>
                                                            {['مقر الشعبة', 'تبريد باب الزبير', 'ورشة التبريد', 'تبريد المكينة', 'تبريد نهر بن عمر', 'تبريد المركز الثقافي'].map(u => (
                                                                <option key={u} value={u}>📍 {u}</option>
                                                            ))}
                                                        </select>
                                                    </div>

                                                    {/* حقل البحث */}
                                                    <div className="md:col-span-3 space-y-1.5">
                                                        <label className="block text-xs font-black text-slate-700">🔍 بحث بالاسم/الرقم الوظيفي:</label>
                                                        <div className="relative bg-white border-2 border-slate-300 rounded-xl px-3 py-2 shadow-sm focus-within:border-indigo-500 flex items-center gap-2">
                                                            <span className="text-slate-400 text-sm">🔍</span>
                                                            <input
                                                                type="text"
                                                                placeholder="ابحث..."
                                                                value={periodSearchQuery}
                                                                onChange={(e) => setPeriodSearchQuery(e.target.value)}
                                                                className="w-full outline-none font-bold text-slate-800 text-xs md:text-sm bg-transparent"
                                                            />
                                                        </div>
                                                    </div>
                                                </div>

                                                {/* أزرار الفترات السريعة */}
                                                <div className="flex flex-wrap items-center gap-2 pt-2 border-t border-slate-200/60">
                                                    <span className="text-xs font-bold text-slate-500 ml-2">⚡ اختصارات سريعة للفترة:</span>
                                                    <button onClick={() => setPeriodPreset('currentMonth')} className="px-3 py-1.5 bg-indigo-50 hover:bg-indigo-100 text-indigo-700 font-bold rounded-lg text-xs transition border border-indigo-200 cursor-pointer">
                                                        🗓️ الشهر الحالي
                                                    </button>
                                                    <button onClick={() => setPeriodPreset('prevMonth')} className="px-3 py-1.5 bg-slate-100 hover:bg-slate-200 text-slate-700 font-bold rounded-lg text-xs transition border border-slate-300 cursor-pointer">
                                                        📅 الشهر الماضي
                                                    </button>
                                                    <button onClick={() => setPeriodPreset('last7')} className="px-3 py-1.5 bg-slate-100 hover:bg-slate-200 text-slate-700 font-bold rounded-lg text-xs transition border border-slate-300 cursor-pointer">
                                                        ⏩ آخر 7 أيام
                                                    </button>
                                                    <button onClick={() => setPeriodPreset('last30')} className="px-3 py-1.5 bg-slate-100 hover:bg-slate-200 text-slate-700 font-bold rounded-lg text-xs transition border border-slate-300 cursor-pointer">
                                                        ⏪ آخر 30 يوماً
                                                    </button>
                                                </div>
                                            </div>

                                            {/* بطاقات الملخص التجميعي للفترة */}
                                            <div className="p-6 grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-4 bg-slate-50/40 border-b border-slate-100">
                                                <div className="bg-white p-4 rounded-xl border border-slate-200 text-center shadow-sm">
                                                    <div className="text-2xl mb-1">👥</div>
                                                    <div className="text-[10px] font-bold text-slate-400">الموظفون المشمولون</div>
                                                    <div className="text-xl font-black text-slate-800 mt-1">{periodReportData.summary.totalStaff} موظف</div>
                                                </div>
                                                <div className="bg-white p-4 rounded-xl border border-slate-200 text-center shadow-sm">
                                                    <div className="text-2xl mb-1">📆</div>
                                                    <div className="text-[10px] font-bold text-slate-400">إجمالي أيام الفترة</div>
                                                    <div className="text-xl font-black text-indigo-600 mt-1">{periodReportData.summary.totalDaysCount} يوم</div>
                                                </div>
                                                <div className="bg-white p-4 rounded-xl border border-slate-200 text-center shadow-sm">
                                                    <div className="text-2xl mb-1">🟢</div>
                                                    <div className="text-[10px] font-bold text-slate-400">أيام الدوام الاعتيادي</div>
                                                    <div className="text-xl font-black text-emerald-600 mt-1">{periodReportData.summary.totalDutyDays} يوم</div>
                                                </div>
                                                <div className="bg-white p-4 rounded-xl border border-slate-200 text-center shadow-sm">
                                                    <div className="text-2xl mb-1">⚡</div>
                                                    <div className="text-[10px] font-bold text-slate-400">أيام الدوام الإضافي</div>
                                                    <div className="text-xl font-black text-amber-600 mt-1">{periodReportData.summary.totalOvertimeDays} يوم</div>
                                                </div>
                                                <div className="bg-white p-4 rounded-xl border border-slate-200 text-center shadow-sm">
                                                    <div className="text-2xl mb-1">🏖️</div>
                                                    <div className="text-[10px] font-bold text-slate-400">إجمالي أيام الإجازات</div>
                                                    <div className="text-xl font-black text-rose-600 mt-1">{periodReportData.summary.totalLeaveDays} يوم</div>
                                                </div>
                                                <div className="bg-white p-4 rounded-xl border border-slate-200 text-center shadow-sm">
                                                    <div className="text-2xl mb-1">❌</div>
                                                    <div className="text-[10px] font-bold text-slate-400">إجمالي أيام الغياب</div>
                                                    <div className="text-xl font-black text-red-700 mt-1">{periodReportData.summary.totalAbsenceDays} يوم</div>
                                                </div>
                                            </div>
                                        </div>

                                        {/* جدول موقف المنتسبين التفصيلي للفترة */}
                                        <div className="bg-white rounded-2xl shadow-md border border-slate-200 overflow-hidden">
                                            <div className="px-6 py-4 bg-slate-100/80 border-b border-slate-200 flex justify-between items-center">
                                                <h3 className="font-black text-slate-800 text-sm md:text-base flex items-center gap-2">
                                                    <span>📋</span>
                                                    <span>سجل حضور وإجازات المنتسبين للفترة من ({periodStartDate}) إلى ({periodEndDate})</span>
                                                </h3>
                                                <span className="bg-indigo-100 text-indigo-800 font-extrabold px-3 py-1 rounded-full text-xs">
                                                    {periodReportData.employees.length} منتسب
                                                </span>
                                            </div>

                                            <div className="overflow-x-auto w-full">
                                                <table className="w-full text-right border-collapse text-xs md:text-sm">
                                                    <thead>
                                                        <tr className="bg-slate-200/70 text-slate-700 border-b border-slate-300 font-black">
                                                            <th className="px-3 py-3.5 text-center w-12">ت</th>
                                                            <th className="px-4 py-3.5 text-right">الاسم الكامل</th>
                                                            <th className="px-3 py-3.5 text-center">الرقم الوظيفي</th>
                                                            <th className="px-3 py-3.5 text-center">الوحدة</th>
                                                            <th className="px-3 py-3.5 text-center">طبيعة الدوام</th>
                                                            <th className="px-3 py-3.5 text-center text-emerald-700">دوام اعتيادي</th>
                                                            <th className="px-3 py-3.5 text-center text-amber-700">دوام إضافي</th>
                                                            <th className="px-3 py-3.5 text-center text-rose-700">إجازات</th>
                                                            <th className="px-3 py-3.5 text-center text-indigo-700">دورة/إيفاد</th>
                                                            <th className="px-3 py-3.5 text-center text-red-700">غياب</th>
                                                            <th className="px-3 py-3.5 text-center">سجل الأيام</th>
                                                        </tr>
                                                    </thead>
                                                    <tbody>
                                                        {periodReportData.employees.length === 0 ? (
                                                            <tr>
                                                                <td colSpan="11" className="px-4 py-8 text-center text-slate-500 font-bold">
                                                                    🚫 لا توجد نتائج مطابقة لخيارات الفلترة المحددة.
                                                                </td>
                                                            </tr>
                                                        ) : (
                                                            periodReportData.employees.map((item, idx) => {
                                                                const emp = item.employee;
                                                                const isExpanded = expandedEmpPeriod === emp.id;
                                                                return (
                                                                    <React.Fragment key={emp.id}>
                                                                        <tr className={`border-b border-slate-100 hover:bg-indigo-50/40 transition ${isExpanded ? 'bg-indigo-50/60' : ''}`}>
                                                                            <td className="px-3 py-3 text-center text-slate-500 font-extrabold">{idx + 1}</td>
                                                                            <td className="px-4 py-3 font-black text-slate-900">
                                                                                <button onClick={() => openEditModal(emp)} className="text-blue-700 hover:underline outline-none text-right">
                                                                                    {getTripleName(emp.name)}
                                                                                </button>
                                                                            </td>
                                                                            <td className="px-3 py-3 text-center font-mono font-bold text-slate-600">{emp.jobNumber || '-'}</td>
                                                                            <td className="px-3 py-3 text-center font-bold text-slate-700">{emp.unit || '-'}</td>
                                                                            <td className="px-3 py-3 text-center">
                                                                                <span className={`px-2 py-0.5 rounded text-[11px] font-black ${emp.workType === 'مناوب' ? 'bg-purple-100 text-purple-800' : 'bg-blue-100 text-blue-800'}`}>
                                                                                    {emp.workType}
                                                                                </span>
                                                                            </td>
                                                                            <td className="px-3 py-3 text-center font-black text-emerald-700 bg-emerald-50/30">{item.regularDuty} يوم</td>
                                                                            <td className="px-3 py-3 text-center font-black text-amber-700 bg-amber-50/30">{item.overtimeDuty} يوم</td>
                                                                            <td className="px-3 py-3 text-center font-black text-rose-700 bg-rose-50/30">{item.leaves} يوم</td>
                                                                            <td className="px-3 py-3 text-center font-black text-indigo-700 bg-indigo-50/30">{item.coursesOrDeputation} يوم</td>
                                                                            <td className="px-3 py-3 text-center font-black text-red-700 bg-red-50/30">{item.absence} يوم</td>
                                                                            <td className="px-3 py-3 text-center">
                                                                                <button
                                                                                    onClick={() => setExpandedEmpPeriod(isExpanded ? null : emp.id)}
                                                                                    className="px-2.5 py-1 bg-slate-800 hover:bg-slate-900 text-amber-400 font-bold rounded-lg text-xs transition cursor-pointer"
                                                                                >
                                                                                    {isExpanded ? 'إخفاء 🔼' : 'عرض السجل 🔽'}
                                                                                </button>
                                                                            </td>
                                                                        </tr>

                                                                        {/* السجل اليومي التفصيلي عند الضغط */}
                                                                        {isExpanded && (
                                                                            <tr className="bg-slate-900 text-white border-b-2 border-slate-700">
                                                                                <td colSpan="11" className="p-4 space-y-3">
                                                                                    <div className="flex justify-between items-center">
                                                                                        <h4 className="font-black text-amber-400 text-xs md:text-sm flex items-center gap-1.5">
                                                                                            <span>🗓️</span>
                                                                                            <span>السجل اليومي التفصيلي للمنتسب: ({emp.name}) للفترة من {periodStartDate} إلى {periodEndDate}</span>
                                                                                        </h4>
                                                                                        <span className="text-slate-400 text-xs">إجمالي الأيام: {item.dailyLog.length} يوم</span>
                                                                                    </div>

                                                                                    <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-6 gap-2 max-h-60 overflow-y-auto p-1 scrollbar-thin">
                                                                                        {item.dailyLog.map(dayItem => {
                                                                                            let bgClass = 'bg-slate-800 border-slate-700 text-slate-200';
                                                                                            if (dayItem.status === 'دوام صباحي' || dayItem.status.includes('12 ساعة') || dayItem.status.includes('24 ساعة')) bgClass = 'bg-slate-800 border-emerald-500/50 text-emerald-300';
                                                                                            else if (dayItem.status === 'دوام إضافي' || dayItem.status.includes('إضافي')) bgClass = 'bg-amber-950 border-amber-500 text-amber-300 font-black';
                                                                                            else if (dayItem.status.includes('إجازة') || dayItem.status.includes('مرضية')) bgClass = 'bg-rose-950 border-rose-500 text-rose-300';
                                                                                            else if (dayItem.status === 'غياب') bgClass = 'bg-red-900 border-red-500 text-white font-black';

                                                                                            return (
                                                                                                <div key={dayItem.dateStr} className={`p-2 rounded-lg border text-xs space-y-1 ${bgClass}`}>
                                                                                                    <div className="flex justify-between items-center text-[10px] opacity-80">
                                                                                                        <span>{dayItem.dayName}</span>
                                                                                                        <span className="font-mono">{dayItem.dateStr}</span>
                                                                                                    </div>
                                                                                                    <div className="font-bold text-[11px] truncate" title={dayItem.status}>
                                                                                                        {dayItem.isOverride ? '📌 ' : ''}{dayItem.status}
                                                                                                    </div>
                                                                                                </div>
                                                                                            );
                                                                                        })}
                                                                                    </div>
                                                                                </td>
                                                                            </tr>
                                                                        )}
                                                                    </React.Fragment>
                                                                );
                                                            })
                                                        )}
                                                    </tbody>
                                                </table>
                                            </div>
                                        </div>
                                    </div>
                                ) : (
                                    <div className="space-y-4">"""

code = code.replace(old_subview_switch_end, period_view_ui)

# Save local offline v6.7
with open('نظام_ادراة_الملاك_v6.7.html', 'w', encoding='utf-8') as f:
    f.write(code)

print('Successfully generated نظام_ادراة_الملاك_v6.7.html')

# Generate online v6.7
online_code = code
online_code = online_code.replace('<script src="libs/react.production.min.js"></script>', '<script src="https://unpkg.com/react@18/umd/react.production.min.js"></script>')
online_code = online_code.replace('<script src="libs/react-dom.production.min.js"></script>', '<script src="https://unpkg.com/react-dom@18/umd/react-dom.production.min.js"></script>')
online_code = online_code.replace('<script src="libs/babel.min.js"></script>', '<script src="https://unpkg.com/@babel/standalone@7.26.2/babel.min.js"></script>')
online_code = online_code.replace('<script src="libs/tailwindcss.js"></script>', '<script src="https://cdn.tailwindcss.com"></script>')
online_code = online_code.replace('<script src="libs/xlsx.full.min.js"></script>', '<script src="https://cdn.jsdelivr.net/npm/xlsx@0.18.5/dist/xlsx.full.min.js"></script>')
online_code = online_code.replace('<script src="libs/exceljs.min.js"></script>', '<script src="https://cdn.jsdelivr.net/npm/exceljs@4.4.0/dist/exceljs.min.js"></script>')
online_code = online_code.replace('<script src="libs/docx.js"></script>', '<script src="https://cdn.jsdelivr.net/npm/docx@8.5.0/build/index.umd.js"></script>')
online_code = online_code.replace('<script src="libs/FileSaver.min.js"></script>', '<script src="https://cdn.jsdelivr.net/npm/file-saver@2.0.5/dist/FileSaver.min.js"></script>')

with open('نظام_ادراة_الملاك_v6.7_online.html', 'w', encoding='utf-8') as f:
    f.write(online_code)

print('Successfully generated نظام_ادراة_الملاك_v6.7_online.html')

# Copy to Desktop
desktop_dir = r'C:\Users\asalz\OneDrive\Desktop'
if os.path.exists(desktop_dir):
    with open(os.path.join(desktop_dir, 'نظام_ادراة_الملاك_v6.7.html'), 'w', encoding='utf-8') as f:
        f.write(code)
    with open(os.path.join(desktop_dir, 'نظام_ادراة_الملاك_v6.7_online.html'), 'w', encoding='utf-8') as f:
        f.write(online_code)
    print('Successfully copied v6.7 files to OneDrive Desktop')
