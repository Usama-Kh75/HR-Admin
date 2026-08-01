import re
import os

with open('نظام_ادراة_الملاك_v6.7.html', 'r', encoding='utf-8') as f:
    code = f.read()

# 1. Version string v6.8 Beta
code = code.replace('<title>نظام إدارة الملاك - الإصدار v6.7 Beta</title>', '<title>نظام إدارة الملاك - الإصدار v6.8 Beta</title>')
code = code.replace("version: 'v6.7 Beta',", "version: 'v6.8 Beta',")
code = code.replace('v6.7 Beta', 'v6.8 Beta')
code = code.replace('الإصدار v6.7 Beta', 'الإصدار v6.8 Beta')

# 2. Add Official Holidays state, Multi-day holiday states & Hourly Leaves tracking state
state_insertion_point = "const [dataEntryOperator, setDataEntryOperator] = useState(() => {"
v68_states_code = """// ===== قائمة وتاريخ العطل الرسمية المعرفة =====
            const [officialHolidays, setOfficialHolidays] = useState(() => {
                const saved = localStorage.getItem('officialHolidaysList');
                return saved ? JSON.parse(saved) : [];
            });
            React.useEffect(() => {
                localStorage.setItem('officialHolidaysList', JSON.stringify(officialHolidays));
            }, [officialHolidays]);

            // حالات نافذة العطل الرسمية والأعياد المتعددة الأيام
            const [showHolidaysModal, setShowHolidaysModal] = useState(false);
            const [holidayRangeStart, setHolidayRangeStart] = useState('');
            const [holidayRangeEnd, setHolidayRangeEnd] = useState('');

            // ===== سجل الإجازات الزمنية بالساعات وساعات الإضافي =====
            const [hourlyLeaveRecords, setHourlyLeaveRecords] = useState(() => {
                const saved = localStorage.getItem('hourlyLeaveRecords');
                return saved ? JSON.parse(saved) : {};
            });
            const [overtimeHoursRecords, setOvertimeHoursRecords] = useState(() => {
                const saved = localStorage.getItem('overtimeHoursRecords');
                return saved ? JSON.parse(saved) : {};
            });

            React.useEffect(() => {
                localStorage.setItem('hourlyLeaveRecords', JSON.stringify(hourlyLeaveRecords));
            }, [hourlyLeaveRecords]);
            React.useEffect(() => {
                localStorage.setItem('overtimeHoursRecords', JSON.stringify(overtimeHoursRecords));
            }, [overtimeHoursRecords]);

            const toggleOfficialHolidayDate = (dateStr) => {
                setOfficialHolidays(prev => {
                    if (prev.includes(dateStr)) {
                        return prev.filter(d => d !== dateStr);
                    } else {
                        return [...prev, dateStr];
                    }
                });
            };

            // إضافة نطاق عطل رسمية متعددة الأيام (مثل عطلة العيد)
            const addOfficialHolidayRange = (startStr, endStr) => {
                if (!startStr || !endStr) {
                    alert('⚠️ يرجى تحديد تاريخ البداية وتاريخ النهاية أولاً.');
                    return;
                }
                const start = new Date(startStr);
                const end = new Date(endStr);
                if (start > end) {
                    alert('⚠️ تاريخ البداية يجب أن يكون قبل أو يساوي تاريخ النهاية.');
                    return;
                }

                const newDates = [];
                let cur = new Date(start);
                while (cur <= end) {
                    const y = cur.getFullYear();
                    const m = String(cur.getMonth() + 1).padStart(2, '0');
                    const d = String(cur.getDate()).padStart(2, '0');
                    newDates.push(`${y}-${m}-${d}`);
                    cur.setDate(cur.getDate() + 1);
                }

                setOfficialHolidays(prev => Array.from(new Set([...prev, ...newDates])));
                alert(`✅ تم إضافة ${newDates.length} أيام كـ عطل رسمية بنجاح!`);
                setHolidayRangeStart('');
                setHolidayRangeEnd('');
            };

            const setEmployeeHourlyLeave = (empId, dateStr, hours) => {
                setHourlyLeaveRecords(prev => {
                    const next = { ...prev };
                    if (!next[dateStr]) next[dateStr] = {};
                    if (!hours || hours <= 0) {
                        delete next[dateStr][empId];
                        if (Object.keys(next[dateStr]).length === 0) delete next[dateStr];
                    } else {
                        next[dateStr][empId] = hours;
                    }
                    return next;
                });
            };

            const setEmployeeOvertimeHours = (empId, dateStr, hours) => {
                setOvertimeHoursRecords(prev => {
                    const next = { ...prev };
                    if (!next[dateStr]) next[dateStr] = {};
                    if (!hours || hours <= 0) {
                        delete next[dateStr][empId];
                        if (Object.keys(next[dateStr]).length === 0) delete next[dateStr];
                    } else {
                        next[dateStr][empId] = hours;
                    }
                    return next;
                });
            };

            const [dataEntryOperator, setDataEntryOperator] = useState(() => {"""

code = code.replace(state_insertion_point, v68_states_code)

# 3. Update dailyStats calculation
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
                    if (status === 'دوام صباحي' || status === 'حضور فعلي' || status === 'إجازة زمنية') {
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
                    } else if (status.includes('استراحة') || status === 'عطلة رسمية') {
                        rest++;
                    } else if (status.includes('إجازة') || status.includes('غياب') || status.includes('دورة') || status.includes('إيفاد') || status.includes('مرضية')) {
                        off++;
                    }
                });
                
                return { onDuty, morningOnDuty, dayShift12h, nightShift12h, shift24h, overtimeDuty, rest, off };
            }, [staff, dailyReportDate, dailyStatusOverrides, anchorDate, threeShiftAnchorSquad, twoShiftAnchorSquad, officialHolidays]);"""

code = code.replace(old_daily_stats, new_daily_stats)

# 4. Add getEmployeeDefaultNaturalStatus helper & Update getEmployeeDailyStatus function
old_get_daily_status = """            const getEmployeeDailyStatus = (emp, dateStr) => {
                if (dailyStatusOverrides[dateStr] && dailyStatusOverrides[dateStr][emp.id]) {
                    return dailyStatusOverrides[dateStr][emp.id];
                }
                if (emp.status && emp.status !== 'نشط') {
                    return emp.status;
                }
                if (emp.workType === 'صباحي') {
                    if (!dateStr) return 'دوام صباحي';
                    try {
                        const date = new Date(dateStr + 'T00:00:00');
                        const day = date.getDay();
                        if (day === 5 || day === 6) {
                            return 'استراحة نهاية الأسبوع';
                        }
                    } catch (e) {}
                    return 'دوام صباحي';
                }"""

new_get_daily_status = """            // الحصول على الموقف الطبيعي الافتراضي للمنتسب بدون أي تعديلات (الحضور/الدوام الأصلي)
            const getEmployeeDefaultNaturalStatus = (emp, dateStr) => {
                if (emp.status && emp.status !== 'نشط') {
                    return emp.status;
                }
                const isOfficialHoliday = officialHolidays.includes(dateStr);
                if (emp.workType === 'صباحي') {
                    if (!dateStr) return 'دوام صباحي';
                    try {
                        const parts = dateStr.split('-');
                        const curDate = new Date(parseInt(parts[0]), parseInt(parts[1]) - 1, parseInt(parts[2]));
                        const day = curDate.getDay();

                        if (isOfficialHoliday) return 'عطلة رسمية';
                        if (day === 5 || day === 6) return 'استراحة نهاية الأسبوع';
                    } catch (e) {}
                    return 'دوام صباحي';
                }
                if (emp.workType === 'مناوب') {
                    if (!emp.squad) return 'مناوب (الوجبة غير محددة)';
                    const isThreeShift = emp.location && emp.location.includes('نهر بن عمر');
                    const diffDays = getDaysBetweenDates(dateStr, anchorDate);
                    
                    if (isThreeShift) {
                        const squads = ['A', 'B', 'C', 'D'];
                        const idxAnchor = squads.indexOf(threeShiftAnchorSquad);
                        if (idxAnchor === -1) return 'استراحة مناوبة';
                        const idxActive = (idxAnchor + (diffDays % 4) + 4) % 4;
                        if (emp.squad === squads[idxActive]) return 'دوام 24 ساعة';
                        return 'استراحة مناوبة';
                    } else {
                        const squadToDayMap = { 'A': 1, 'C': 2, 'D': 3, 'B': 4 };
                        const anchorDay = squadToDayMap[twoShiftAnchorSquad] || 1;
                        const cycleDay = ((anchorDay - 1 + diffDays) % 4 + 4) % 4 + 1;
                        const S = emp.squad;
                        if (cycleDay === 1) {
                            if (S === 'A') return 'دوام صباحي (12 ساعة)';
                            if (S === 'B') return 'دوام مسائي (12 ساعة)';
                            return 'استراحة مناوبة';
                        } else if (cycleDay === 2) {
                            if (S === 'C') return 'دوام صباحي (12 ساعة)';
                            if (S === 'A') return 'دوام مسائي (12 ساعة)';
                            return 'استراحة مناوبة';
                        } else if (cycleDay === 3) {
                            if (S === 'D') return 'دوام صباحي (12 ساعة)';
                            if (S === 'C') return 'دوام مسائي (12 ساعة)';
                            return 'استراحة مناوبة';
                        } else if (cycleDay === 4) {
                            if (S === 'B') return 'دوام صباحي (12 ساعة)';
                            if (S === 'D') return 'دوام مسائي (12 ساعة)';
                            return 'استراحة مناوبة';
                        }
                        return 'استراحة مناوبة';
                    }
                }
                return 'دوام صباحي';
            };

            const getEmployeeDailyStatus = (emp, dateStr) => {
                // 1. التعديلات الاستثنائية المباشرة للموظف
                if (dailyStatusOverrides[dateStr] && dailyStatusOverrides[dateStr][emp.id]) {
                    return dailyStatusOverrides[dateStr][emp.id];
                }
                if (emp.status && emp.status !== 'نشط') {
                    return emp.status;
                }
                
                // 2. فحص العطل الرسمية المحددة بالنظام
                const isOfficialHoliday = officialHolidays.includes(dateStr);

                if (emp.workType === 'صباحي') {
                    if (!dateStr) return 'دوام صباحي';
                    try {
                        const parts = dateStr.split('-');
                        const curDate = new Date(parseInt(parts[0]), parseInt(parts[1]) - 1, parseInt(parts[2]));
                        const day = curDate.getDay();

                        // عطلة رسمية عامة
                        if (isOfficialHoliday) {
                            return 'عطلة رسمية';
                        }

                        // فحص يومي الجمعة (5) والسبت (6) وقاعدة الربط بالخميس والأحد
                        if (day === 5 || day === 6) {
                            // حساب تاريخ الخميس والأحد
                            let thuDate = new Date(curDate);
                            let sunDate = new Date(curDate);
                            if (day === 5) {
                                thuDate.setDate(curDate.getDate() - 1);
                                sunDate.setDate(curDate.getDate() + 2);
                            } else {
                                thuDate.setDate(curDate.getDate() - 2);
                                sunDate.setDate(curDate.getDate() + 1);
                            }
                            
                            const thuStr = `${thuDate.getFullYear()}-${String(thuDate.getMonth() + 1).padStart(2, '0')}-${String(thuDate.getDate()).padStart(2, '0')}`;
                            const sunStr = `${sunDate.getFullYear()}-${String(sunDate.getMonth() + 1).padStart(2, '0')}-${String(sunDate.getDate()).padStart(2, '0')}`;

                            const thuStatus = dailyStatusOverrides[thuStr] && dailyStatusOverrides[thuStr][emp.id];
                            const sunStatus = dailyStatusOverrides[sunStr] && dailyStatusOverrides[sunStr][emp.id];

                            // إذا كان الخميس والأحد إجازة مدفوعة/اعتيادية/مرضية، تحسب الجمعة والسبت من ضمن الإجازة
                            const isLeaveType = (st) => st && (st.includes('إجازة اعتيادية') || st.includes('مرضية') || st.includes('خارج العراق'));
                            if (isLeaveType(thuStatus) && isLeaveType(sunStatus)) {
                                return thuStatus; // تكتسب نفس نوع إجازة الخميس
                            }

                            return 'استراحة نهاية الأسبوع';
                        }
                    } catch (e) {}
                    return 'دوام صباحي';
                }"""

code = code.replace(old_get_daily_status, new_get_daily_status)

# 5. Update status badge color for "إجازة زمنية" to BRIGHT AMBER/YELLOW in daily list
old_badge_colors = """                                                                         if (status === 'دوام صباحي') statusBadgeColor = 'bg-blue-50 text-blue-700 border-blue-200 hover:bg-blue-100';
                                                                        else if (status === 'دوام صباحي (12 ساعة)') statusBadgeColor = 'bg-amber-50 text-amber-700 border-amber-200 hover:bg-amber-100';
                                                                        else if (status === 'دوام مسائي (12 ساعة)') statusBadgeColor = 'bg-indigo-900 text-indigo-100 border-indigo-900 hover:bg-indigo-800';
                                                                        else if (status === 'دوام 24 ساعة') statusBadgeColor = 'bg-purple-100 text-purple-800 border-purple-200 hover:bg-purple-200';
                                                                        else if (status === 'دوام إضافي' || status.includes('إضافي')) statusBadgeColor = 'bg-emerald-100 text-emerald-800 border-emerald-300 hover:bg-emerald-200';
                                                                        else if (status === 'إجازة خارج العراق') statusBadgeColor = 'bg-cyan-100 text-cyan-900 border-cyan-300 hover:bg-cyan-200';
                                                                        else if (status === 'إيفاد داخل العراق' || status === 'إيفاد') statusBadgeColor = 'bg-purple-100 text-purple-800 border-purple-300 hover:bg-purple-200';
                                                                        else if (status === 'إيفاد خارج العراق') statusBadgeColor = 'bg-indigo-100 text-indigo-900 border-indigo-300 hover:bg-indigo-200';
                                                                        else if (status.includes('استراحة')) statusBadgeColor = 'bg-slate-100 text-slate-600 border-slate-200 hover:bg-slate-200';"""

new_badge_colors = """                                                                         if (status === 'دوام صباحي') statusBadgeColor = 'bg-blue-50 text-blue-700 border-blue-200 hover:bg-blue-100';
                                                                        else if (status === 'دوام صباحي (12 ساعة)') statusBadgeColor = 'bg-amber-50 text-amber-700 border-amber-200 hover:bg-amber-100';
                                                                        else if (status === 'دوام مسائي (12 ساعة)') statusBadgeColor = 'bg-indigo-900 text-indigo-100 border-indigo-900 hover:bg-indigo-800';
                                                                        else if (status === 'دوام 24 ساعة') statusBadgeColor = 'bg-purple-100 text-purple-800 border-purple-200 hover:bg-purple-200';
                                                                        else if (status === 'دوام إضافي' || status.includes('إضافي')) statusBadgeColor = 'bg-emerald-100 text-emerald-800 border-emerald-300 hover:bg-emerald-200';
                                                                        else if (status === 'إجازة زمنية') statusBadgeColor = 'bg-amber-100 text-amber-950 border-amber-400 hover:bg-amber-200 font-black ring-2 ring-amber-300';
                                                                        else if (status === 'إجازة خارج العراق') statusBadgeColor = 'bg-cyan-100 text-cyan-900 border-cyan-300 hover:bg-cyan-200';
                                                                        else if (status === 'إيفاد داخل العراق' || status === 'إيفاد') statusBadgeColor = 'bg-purple-100 text-purple-800 border-purple-300 hover:bg-purple-200';
                                                                        else if (status === 'إيفاد خارج العراق') statusBadgeColor = 'bg-indigo-100 text-indigo-900 border-indigo-300 hover:bg-indigo-200';
                                                                        else if (status.includes('استراحة')) statusBadgeColor = 'bg-slate-100 text-slate-600 border-slate-200 hover:bg-slate-200';"""

code = code.replace(old_badge_colors, new_badge_colors)

# 6. FIX PROMPT CANCEL LOGIC & ADD EXPLICIT "دوام صباحي" TO SELECT OPTIONS
old_set_override = """            const setEmployeeDailyStatusOverride = (empId, dateStr, status) => {
                setDailyStatusOverrides(prev => {
                    const next = { ...prev };
                    if (!next[dateStr]) next[dateStr] = {};
                    if (status === 'default') {
                        delete next[dateStr][empId];
                        if (Object.keys(next[dateStr]).length === 0) {
                            delete next[dateStr];
                        }
                    } else {
                        next[dateStr][empId] = status;
                    }
                    return next;
                });
            };"""

new_set_override = """            const setEmployeeDailyStatusOverride = (empId, dateStr, status) => {
                const emp = staff.find(s => s.id === empId);

                // إلغاء وسحب التعديل فوراً والعودة إلى الافتراضي الأصلي
                const revertToDefault = () => {
                    setEmployeeHourlyLeave(empId, dateStr, 0);
                    setEmployeeOvertimeHours(empId, dateStr, 0);
                    setDailyStatusOverrides(prev => {
                        const next = { ...prev };
                        if (next[dateStr]) {
                            delete next[dateStr][empId];
                            if (Object.keys(next[dateStr]).length === 0) delete next[dateStr];
                        }
                        return next;
                    });
                };

                if (emp && emp.workType === 'صباحي' && dateStr && (status.includes('إجازة اعتيادية') || status.includes('إجازة مرضية') || status.includes('إجازة خارج العراق'))) {
                    try {
                        const parts = dateStr.split('-');
                        const d = new Date(parseInt(parts[0]), parseInt(parts[1]) - 1, parseInt(parts[2]));
                        const day = d.getDay();
                        if (day === 5 || day === 6) {
                            let thuDate = new Date(d);
                            let sunDate = new Date(d);
                            if (day === 5) { thuDate.setDate(d.getDate() - 1); sunDate.setDate(d.getDate() + 2); }
                            else { thuDate.setDate(d.getDate() - 2); sunDate.setDate(d.getDate() + 1); }
                            
                            const thuStr = `${thuDate.getFullYear()}-${String(thuDate.getMonth() + 1).padStart(2, '0')}-${String(thuDate.getDate()).padStart(2, '0')}`;
                            const sunStr = `${sunDate.getFullYear()}-${String(sunDate.getMonth() + 1).padStart(2, '0')}-${String(sunDate.getDate()).padStart(2, '0')}`;

                            const thuStatus = dailyStatusOverrides[thuStr] && dailyStatusOverrides[thuStr][empId];
                            const sunStatus = dailyStatusOverrides[sunStr] && dailyStatusOverrides[sunStr][empId];
                            const isLeaveType = (st) => st && (st.includes('إجازة اعتيادية') || st.includes('مرضية') || st.includes('خارج العراق'));

                            if (!isLeaveType(thuStatus) || !isLeaveType(sunStatus)) {
                                const confirmLeave = confirm(`⚠️ تنبيه إداري:\\n\\nيوم (${day === 5 ? 'الجمعة' : 'السبت'}) هو يوم استراحة رسمية نهاية الأسبوع للدوام الصباحي.\\n\\nتذكير: لا تحسب الإجازة في نهاية الأسبوع إلا إذا كانت مؤشرة يوم الخميس ويوم الأحد معاً (قاعدة ربط الإجازة).\\n\\nهل تريد تأكيد تسليط الإجازة بالرغم من ذلك؟\\n\\n• اضغط [موافق / OK] للتأكيد وتسليط الإجازة.\\n• اضغط [إلغاء / Cancel] للتراجع والاحتفاظ بـ استراحة نهاية الأسبوع.`);
                                if (!confirmLeave) {
                                    revertToDefault();
                                    return;
                                }
                            }
                        }
                    } catch(e) {}
                }

                if (status === 'default') {
                    revertToDefault();
                    return;
                } else if (status === 'إجازة زمنية') {
                    const empName = emp ? emp.name : 'المنتسب';
                    const inputHours = prompt(`⏰ الإجازة الزمنية للمنتسب (${empName}):\\n\\nكم عدد ساعات الإجازة الزمنية الممنوحة اليوم؟ (أدخل عدداً من 1 إلى 7 ساعات):`, '2');
                    if (inputHours !== null) {
                        const h = parseInt(inputHours.trim());
                        if (!isNaN(h) && h >= 1 && h <= 7) {
                            setEmployeeHourlyLeave(empId, dateStr, h);
                        } else {
                            setEmployeeHourlyLeave(empId, dateStr, 2);
                        }
                    } else {
                        revertToDefault();
                        return;
                    }
                } else if (status === 'دوام إضافي' || status.includes('إضافي')) {
                    try {
                        const empName = emp ? emp.name : 'المنتسب';
                        const dParts = dateStr.split('-');
                        const curD = new Date(parseInt(dParts[0]), parseInt(dParts[1]) - 1, parseInt(dParts[2]));
                        const isSatOrHoliday = curD.getDay() === 6 || officialHolidays.includes(dateStr);
                        const maxHours = isSatOrHoliday ? 3 : 2;

                        const inputOt = prompt(`⚡ الدوام الإضافي للمنتسب (${empName}):\\n\\nكم عدد ساعات العمل الإضافي؟ (الحد الأقصى لهذا اليوم ${maxHours} ساعات):`, maxHours.toString());
                        if (inputOt !== null) {
                            const h = parseInt(inputOt.trim());
                            if (!isNaN(h) && h >= 1 && h <= maxHours) {
                                setEmployeeOvertimeHours(empId, dateStr, h);
                            } else {
                                setEmployeeOvertimeHours(empId, dateStr, maxHours);
                            }
                        } else {
                            revertToDefault();
                            return;
                        }
                    } catch(e) {}
                }

                setDailyStatusOverrides(prev => {
                    const next = { ...prev };
                    if (!next[dateStr]) next[dateStr] = {};
                    next[dateStr][empId] = status;
                    return next;
                });
            };"""

code = code.replace(old_set_override, new_set_override)

# 7. REDESIGN TOP HEADER BAR (ELEGANT 4-COLUMN BALANCED GRID: 4 + 2 + 3 + 3 = 12)
start_marker = '{/* منتقي التاريخ - يمين في RTL */}'
end_marker = '{/* مطابقة الوجبات */}'

p1 = code.find(start_marker)
p2 = code.find(end_marker)

if p1 != -1 and p2 != -1:
    new_four_cols_jsx = """{/* منتقي التاريخ - 4 أعمدة يمين في RTL */}
                                                <div className="md:col-span-4 space-y-1.5">
                                                    <label className="block text-xs font-black text-slate-800">📅 تاريخ الموقف اليومي:</label>
                                                    <div className="flex items-center gap-1.5 bg-white p-1 rounded-xl border-2 border-slate-300 shadow-sm focus-within:border-blue-500">
                                                        <button
                                                            onClick={() => changeReportDateByDays(-1)}
                                                            className="px-2.5 py-1.5 bg-slate-800 hover:bg-slate-900 text-amber-400 font-black rounded-lg text-xs transition cursor-pointer border border-slate-700 active:scale-95 flex items-center gap-1 whitespace-nowrap"
                                                            title="اليوم السابق"
                                                        >
                                                            <span>◀️</span>
                                                            <span>السابق</span>
                                                        </button>

                                                        <div className="relative flex-1 flex items-center gap-1.5 px-1">
                                                            <span className="text-slate-400 text-sm">📅</span>
                                                            <input 
                                                                type="date"
                                                                value={dailyReportDate}
                                                                onChange={(e) => setDailyReportDate(e.target.value)}
                                                                className="w-full outline-none font-black text-slate-800 text-xs bg-transparent cursor-pointer font-mono text-center"
                                                            />
                                                        </div>

                                                        <button
                                                            onClick={() => changeReportDateByDays(1)}
                                                            className="px-2.5 py-1.5 bg-slate-800 hover:bg-slate-900 text-amber-400 font-black rounded-lg text-xs transition cursor-pointer border border-slate-700 active:scale-95 flex items-center gap-1 whitespace-nowrap"
                                                            title="اليوم التالي"
                                                        >
                                                            <span>التالي</span>
                                                            <span>▶️</span>
                                                        </button>
                                                    </div>
                                                </div>

                                                {/* زر إدارة العطل الرسمية والأعياد المستقل - عمودان */}
                                                <div className="md:col-span-2 space-y-1.5">
                                                    <label className="block text-xs font-black text-amber-900">🎉 العطل والأعياد:</label>
                                                    <button
                                                        onClick={() => setShowHolidaysModal(true)}
                                                        className={`w-full py-2 px-3 rounded-xl text-xs font-black transition cursor-pointer border shadow-sm flex items-center justify-center gap-1.5 whitespace-nowrap active:scale-95 ${
                                                            officialHolidays.includes(dailyReportDate)
                                                                ? 'bg-rose-600 hover:bg-rose-700 text-white border-rose-500 ring-2 ring-rose-200'
                                                                : 'bg-amber-100 hover:bg-amber-200 text-amber-950 border-amber-300'
                                                        }`}
                                                        title="إدارة وإعلان العطل الرسمية والأعياد المتعددة الأيام"
                                                    >
                                                        <span>🎉</span>
                                                        <span>{officialHolidays.includes(dailyReportDate) ? 'محدد كـ عطلة' : 'إدارة العطل'}</span>
                                                    </button>
                                                </div>

                                                {/* اسم منظم الموقف / مدخل البيانات - 3 أعمدة */}
                                                <div className="md:col-span-3 space-y-1.5">
                                                    <label className="block text-xs font-black text-slate-800">👤 اسم منظم الموقف / مدخل البيانات:</label>
                                                    <div className="bg-white border-2 border-slate-300 rounded-xl px-3 py-1.5 shadow-sm flex items-center gap-2 focus-within:border-blue-500">
                                                        <span className="text-slate-400 text-sm">✍️</span>
                                                        <input 
                                                            type="text" 
                                                            value={dataEntryOperator} 
                                                            onChange={(e) => setDataEntryOperator(e.target.value)} 
                                                            placeholder="اسم منظم الموقف..." 
                                                            className="w-full outline-none font-bold text-slate-800 text-xs bg-transparent"
                                                        />
                                                    </div>
                                                </div>

                                                {/* زر محرك تقارير موقف الفترة - 3 أعمدة يسار في RTL */}
                                                <div className="md:col-span-3 space-y-1.5">
                                                    <label className="block text-xs font-black text-blue-900">📊 موقف فترة زمنية (من - إلى):</label>
                                                    <button 
                                                        onClick={() => setUnitsSubView('periodReport')}
                                                        className="w-full py-2 px-3 bg-gradient-to-r from-blue-600 to-indigo-600 hover:from-blue-700 hover:to-indigo-700 text-white font-black rounded-xl text-xs shadow-sm hover:shadow transition transform active:scale-95 flex items-center justify-center gap-1.5 cursor-pointer border border-blue-400 whitespace-nowrap"
                                                        title="فتح محرك تقارير موقف الفترة الزمانية"
                                                    >
                                                        <span>📊</span>
                                                        <span>محرك تقارير موقف الفترة</span>
                                                    </button>
                                                </div>
                                                
                                                """
    code = code[:p1] + new_four_cols_jsx + code[p2:]

# 8. UPDATE periodReportData ACCUMULATION LOGIC FOR OVERTIME HOURS
old_period_report_calc = """                let filteredStaff = staff.filter(s => {
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
                });"""

new_period_report_calc = """                let filteredStaff = staff.filter(s => {
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
                    let courses = 0;
                    let deputations = 0;
                    let absence = 0;
                    let rest = 0;
                    let monthlyHourlyLeaveSum = 0;
                    let monthlyOvertimeHoursSum = 0;
                    const dailyLog = [];

                    datesList.forEach(dateStr => {
                        const status = getEmployeeDailyStatus(emp, dateStr);
                        const dayName = getArabicDayName(dateStr);
                        const isOverride = dailyStatusOverrides[dateStr] && dailyStatusOverrides[dateStr][emp.id];
                        const hourlyHours = (status === 'إجازة زمنية' && hourlyLeaveRecords[dateStr] && hourlyLeaveRecords[dateStr][emp.id]) || (status === 'إجازة زمنية' ? 2 : 0);

                        // احتساب ساعات العمل الإضافي التراكمية (السبت/العطلة = 3 ساعات كحد أقصى، الأيام العادية = 2 ساعة)
                        let otHours = 0;
                        if (status === 'دوام إضافي' || status.includes('إضافي')) {
                            if (overtimeHoursRecords[dateStr] && overtimeHoursRecords[dateStr][emp.id]) {
                                otHours = overtimeHoursRecords[dateStr][emp.id];
                            } else {
                                try {
                                    const dParts = dateStr.split('-');
                                    const curD = new Date(parseInt(dParts[0]), parseInt(dParts[1]) - 1, parseInt(dParts[2]));
                                    const isSatOrHoliday = curD.getDay() === 6 || officialHolidays.includes(dateStr);
                                    otHours = isSatOrHoliday ? 3 : 2;
                                } catch(e) { otHours = 2; }
                            }
                            monthlyOvertimeHoursSum += otHours;
                        }

                        if (status === 'إجازة زمنية') {
                            monthlyHourlyLeaveSum += hourlyHours;
                        }

                        // حساب تاريخ اليوم الحالي بالصيغة القياسية YYYY-MM-DD
                        const nowD = new Date();
                        const tY = nowD.getFullYear();
                        const tM = String(nowD.getMonth() + 1).padStart(2, '0');
                        const tD = String(nowD.getDate()).padStart(2, '0');
                        const todayStr = `${tY}-${tM}-${tD}`;
                        const isPastOrToday = dateStr <= todayStr;

                        dailyLog.push({ dateStr, dayName, status, isOverride: !!isOverride, hourlyHours, otHours, isFuture: !isPastOrToday });

                        // احتساب أيام الحضور والإحصائيات فقط للأيام المنقضية واليوم الحالي
                        if (isPastOrToday) {
                            if (status === 'دوام صباحي' || status === 'حضور فعلي' || status === 'دوام صباحي (12 ساعة)' || status === 'دوام مسائي (12 ساعة)' || status === 'دوام 24 ساعة' || status === 'إجازة زمنية') {
                                regularDuty++;
                            } else if (status === 'دوام إضافي' || status.includes('إضافي')) {
                                overtimeDuty++;
                            } else if (status.includes('إجازة اعتيادية') || status.includes('مرضية') || status.includes('خارج العراق') || isLongOrMaternityLeave(status)) {
                                leaves++;
                            } else if (status.includes('دورة')) {
                                courses++;
                            } else if (status.includes('إيفاد')) {
                                deputations++;
                            } else if (status === 'غياب') {
                                absence++;
                            } else if (status.includes('استراحة') || status === 'عطلة رسمية') {
                                rest++;
                            }
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
                        monthlyOvertimeHoursSum,
                        monthlyHourlyLeaveSum,
                        leaves,
                        courses,
                        deputations,
                        absence,
                        rest,
                        dailyLog
                    };
                });"""

code = code.replace(old_period_report_calc, new_period_report_calc)

# 9. REPLACE TOP BANNER (KEEP ONLY 2 CLEAN CARDS)
banner_start = code.find('p-6 grid grid-cols-2')
banner_start = code.rfind('<div', 0, banner_start)
banner_end = code.find('جدول موقف المنتسبين التفصيلي للفترة')
banner_end = code.rfind('{/*', 0, banner_end)

if banner_start != -1 and banner_end != -1:
    new_cards_banner = """<div className="p-4 bg-slate-50/60 border-b border-slate-200 space-y-3">
                                                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                                                    <div className="bg-white rounded-2xl shadow-sm border border-slate-200 p-4 flex items-center justify-between gap-3">
                                                        <div>
                                                            <div className="text-[11px] font-black text-slate-500">👥 الموظفون المشمولون بالتقرير:</div>
                                                            <div className="text-2xl font-black text-slate-900 mt-1">{periodReportData.summary.totalStaff} منتسب</div>
                                                            <div className="text-[10px] font-bold text-slate-400 mt-0.5">يشمل جميع كادر الشعبة المعتمد بالكامل</div>
                                                        </div>
                                                        <div className="w-12 h-12 rounded-2xl bg-blue-50 text-blue-600 flex items-center justify-center text-2xl font-bold flex-shrink-0">
                                                            👥
                                                        </div>
                                                    </div>

                                                    <div className="bg-white rounded-2xl shadow-sm border border-slate-200 p-4 flex items-center justify-between gap-3">
                                                        <div>
                                                            <div className="text-[11px] font-black text-slate-500">📅 أيام الفترة المحددة بالتقرير:</div>
                                                            <div className="text-2xl font-black text-indigo-600 mt-1">{periodReportData.summary.totalDaysCount} يوم</div>
                                                            <div className="text-[10px] font-mono font-bold text-indigo-500 mt-0.5">من {periodStartDate} إلى {periodEndDate}</div>
                                                        </div>
                                                        <div className="w-12 h-12 rounded-2xl bg-indigo-50 text-indigo-600 flex items-center justify-center text-2xl font-bold flex-shrink-0">
                                                            🗓️
                                                        </div>
                                                    </div>
                                                </div>

                                                <div className="bg-amber-50/90 border border-amber-200/80 rounded-xl px-4 py-2 text-xs font-bold text-amber-950 flex items-center gap-2 shadow-xs">
                                                    <span className="text-base flex-shrink-0">💡</span>
                                                    <span>تنبيه ذكي: يتم حساب <strong>أيام الحضور</strong> والإحصائيات التراكمية تلقائياً من بداية الفترة وتزداد يوماً بعد يوم للأيام المنقضية حتى تاريخ اليوم الحالي.</span>
                                                </div>
                                            </div>
                                        </div>

                                        """
    code = code[:banner_start] + new_cards_banner + code[banner_end:]

# 10. REPLACE PERIOD REPORT TABLE HEAD (EXACT 12 COLUMNS)
old_table_head = """                                                    <thead>
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
                                                    </thead>"""

new_table_head = """                                                    <thead>
                                                        <tr className="bg-slate-100 text-slate-800 border-b border-slate-200 font-black text-[12px]">
                                                            <th className="px-3 py-3.5 text-center w-10">ت</th>
                                                            <th className="px-4 py-3.5 text-right">الاسم الكامل</th>
                                                            <th className="px-3 py-3.5 text-center">الرقم الوظيفي</th>
                                                            <th className="px-3 py-3.5 text-center">طبيعة الدوام</th>
                                                            <th className="px-3 py-3.5 text-center text-emerald-700 bg-emerald-50/50">أيام الحضور</th>
                                                            <th className="px-3 py-3.5 text-center text-emerald-800 bg-emerald-100/40">دوام إضافي</th>
                                                            <th className="px-3 py-3.5 text-center text-amber-900 bg-amber-100/70 font-black">ساعات الإضافي ⚡</th>
                                                            <th className="px-3 py-3.5 text-center text-rose-700">إجازات</th>
                                                            <th className="px-3 py-3.5 text-center text-purple-700">دورات</th>
                                                            <th className="px-3 py-3.5 text-center text-indigo-700">إيفادات</th>
                                                            <th className="px-3 py-3.5 text-center text-red-700">غياب</th>
                                                            <th className="px-3 py-3.5 text-center">سجل الأيام</th>
                                                        </tr>
                                                    </thead>"""

code = code.replace(old_table_head, new_table_head)

# 11. REPLACE PERIOD REPORT TABLE ROW & EXPANDED ROW COLSPAN=12 SO IT SPANS FULL WIDTH (FROM NAME TO REGISTER)
old_table_row = """                                                                        <tr className={`border-b border-slate-100 hover:bg-indigo-50/40 transition ${isExpanded ? 'bg-indigo-50/60' : ''}`}>
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
                                                                        </tr>"""

new_table_row = """                                                                        <tr className={`border-b border-slate-100 hover:bg-indigo-50/40 transition ${isExpanded ? 'bg-indigo-50/60' : ''}`}>
                                                                            <td className="px-3 py-3 text-center text-slate-500 font-extrabold">{idx + 1}</td>
                                                                            <td className="px-4 py-3 font-black text-slate-900">
                                                                                <button onClick={() => openEditModal(emp)} className="text-blue-700 hover:underline outline-none text-right">
                                                                                    {getTripleName(emp.name)}
                                                                                </button>
                                                                            </td>
                                                                            <td className="px-3 py-3 text-center font-mono font-bold text-slate-600">{emp.jobNumber || '-'}</td>
                                                                            <td className="px-3 py-3 text-center">
                                                                                <span className={`px-2 py-0.5 rounded text-[11px] font-black ${emp.workType === 'مناوب' ? 'bg-purple-100 text-purple-800' : 'bg-blue-100 text-blue-800'}`}>
                                                                                    {emp.workType}
                                                                                </span>
                                                                            </td>
                                                                            <td className="px-3 py-3 text-center font-black text-emerald-700 bg-emerald-50/30">{item.regularDuty} يوم</td>
                                                                            <td className="px-3 py-3 text-center font-black bg-emerald-50/40 text-emerald-800">
                                                                                {item.overtimeDuty > 0 ? `${item.overtimeDuty} يوم` : '0'}
                                                                            </td>
                                                                            <td className="px-3 py-3 text-center font-black bg-amber-50/60">
                                                                                {item.monthlyOvertimeHoursSum > 0 ? (
                                                                                    <span className="px-2.5 py-1 bg-amber-200 text-amber-950 rounded-lg font-black text-xs ring-1 ring-amber-300">
                                                                                        ⚡ {item.monthlyOvertimeHoursSum}س
                                                                                    </span>
                                                                                ) : (
                                                                                    <span className="text-slate-400 font-bold">0</span>
                                                                                )}
                                                                            </td>
                                                                            <td className="px-3 py-3 text-center font-black text-rose-700">{item.leaves > 0 ? `${item.leaves} يوم` : '0'}</td>
                                                                            <td className="px-3 py-3 text-center font-black text-purple-700">{item.courses > 0 ? `${item.courses} يوم` : '0'}</td>
                                                                            <td className="px-3 py-3 text-center font-black text-indigo-700">{item.deputations > 0 ? `${item.deputations} يوم` : '0'}</td>
                                                                            <td className="px-3 py-3 text-center font-black text-red-700">{item.absence > 0 ? `${item.absence} يوم` : '0'}</td>
                                                                            <td className="px-3 py-3 text-center">
                                                                                <button
                                                                                    onClick={() => setExpandedEmpPeriod(isExpanded ? null : emp.id)}
                                                                                    className="px-2.5 py-1 bg-slate-800 hover:bg-slate-900 text-amber-400 font-bold rounded-lg text-xs transition cursor-pointer"
                                                                                >
                                                                                    {isExpanded ? 'إخفاء 🔼' : 'عرض السجل 🔽'}
                                                                                </button>
                                                                            </td>
                                                                        </tr>"""

code = code.replace(old_table_row, new_table_row)

# 12. UPDATE DAILY LIST STATUS OPTIONS (ADD EXPLICIT "دوام صباحي" OPTION AND CLEAR DEFAULT LABEL)
old_options_block = """                                                                                        <option value="default" className="bg-white text-slate-800 font-bold">
                                                                                            ⚙️ الافتراضي ({status})
                                                                                        </option>
                                                                                        <option value="دوام إضافي" className="bg-white text-emerald-800 font-bold">⚡ دوام إضافي</option>"""

new_options_block = """                                                                                        <option value="default" className="bg-white text-slate-800 font-bold">
                                                                                            ⚙️ الافتراضي ({getEmployeeDefaultNaturalStatus(emp, dailyReportDate)})
                                                                                        </option>
                                                                                        <option value="دوام صباحي" className="bg-white text-blue-700 font-bold">🟢 دوام صباحي (حضور فعلي)</option>
                                                                                        <option value="دوام إضافي" className="bg-white text-emerald-800 font-bold">⚡ دوام إضافي</option>"""

code = code.replace(old_options_block, new_options_block)

# 13. UPDATE EXPANDED ROW COLSPAN TO 12 SO IT EXPANDS ACROSS ALL 12 COLUMNS FULLY
code = code.replace('<td colSpan="11" className="px-4 py-8 text-center text-slate-500 font-bold">', '<td colSpan="12" className="px-4 py-8 text-center text-slate-500 font-bold">')
code = code.replace('<td colSpan="11" className="p-4 space-y-3">', '<td colSpan="12" className="p-4 space-y-3">')
code = code.replace('<td colSpan="11" className="p-4 bg-slate-900/95', '<td colSpan="12" className="p-4 bg-slate-900/95')

# 14. ADD SHOW HOLIDAYS MODAL COMPONENT
old_modal_anchor = "{pendingShiftConfirm && ("
new_modal_code = """{/* نافذة إدارة العطل الرسمية والأعياد */}
            {showHolidaysModal && (
                <div className="fixed inset-0 bg-slate-950/75 backdrop-blur-md flex items-center justify-center z-[120] p-4 animate-fadeIn no-print">
                    <div className="bg-white rounded-3xl max-w-2xl w-full overflow-hidden shadow-2xl border border-slate-200 flex flex-col max-h-[90vh]">
                        {/* رأس النافذة */}
                        <div className="bg-gradient-to-r from-amber-500 via-orange-500 to-amber-600 px-6 py-4 text-white flex items-center justify-between shadow-md">
                            <div className="flex items-center gap-3">
                                <div className="w-10 h-10 rounded-2xl bg-white/20 backdrop-blur-md flex items-center justify-center text-2xl">
                                    🎉
                                </div>
                                <div>
                                    <h3 className="text-xl font-black">إدارة العطل الرسمية والأعياد</h3>
                                    <p className="text-xs text-amber-100 font-bold">تحديد أيام العطل ليتم اعتبارهن عطلة رسمية لكافة المنتسبين</p>
                                </div>
                            </div>
                            <button
                                onClick={() => setShowHolidaysModal(false)}
                                className="w-9 h-9 rounded-full bg-white/10 hover:bg-white/20 text-white flex items-center justify-center font-bold text-lg transition cursor-pointer"
                                title="إغلاق النافذة"
                            >
                                ✕
                            </button>
                        </div>

                        {/* محتوى النافذة القابل للتمرير */}
                        <div className="p-6 overflow-y-auto space-y-6 flex-1 bg-slate-50/50">
                            
                            {/* قسم 1: التحكم بتاريخ الموقف المحدد حالياً */}
                            <div className="bg-white p-4 rounded-2xl border-2 border-amber-200 shadow-sm space-y-3">
                                <div className="flex items-center justify-between flex-wrap gap-2">
                                    <div>
                                        <span className="text-xs font-black text-slate-500 block">📅 تاريخ الموقف اليومي المحدد حالياً:</span>
                                        <span className="text-lg font-black text-slate-800 dir-ltr inline-block">{dailyReportDate}</span>
                                    </div>
                                    <div>
                                        {officialHolidays.includes(dailyReportDate) ? (
                                            <span className="px-3 py-1 rounded-full bg-rose-100 text-rose-700 border border-rose-300 font-black text-xs flex items-center gap-1">
                                                🎉 محدد حالياً كـ عطلة رسمية
                                            </span>
                                        ) : (
                                            <span className="px-3 py-1 rounded-full bg-slate-100 text-slate-600 border border-slate-300 font-black text-xs flex items-center gap-1">
                                                💼 يوم عمل اعتيادي
                                            </span>
                                        )}
                                    </div>
                                </div>
                                <button
                                    type="button"
                                    onClick={() => toggleOfficialHolidayDate(dailyReportDate)}
                                    className={`w-full py-2.5 px-4 rounded-xl font-black text-sm transition cursor-pointer flex items-center justify-center gap-2 shadow-sm ${
                                        officialHolidays.includes(dailyReportDate)
                                            ? 'bg-rose-600 hover:bg-rose-700 text-white shadow-rose-200'
                                            : 'bg-emerald-600 hover:bg-emerald-700 text-white shadow-emerald-200'
                                    }`}
                                >
                                    {officialHolidays.includes(dailyReportDate) ? (
                                        <><span>❌</span><span>إلغاء اعتبار تاريخ الموقف الحالي ({dailyReportDate}) كـ عطلة</span></>
                                    ) : (
                                        <><span>🎉</span><span>تثبيت تاريخ الموقف الحالي ({dailyReportDate}) كـ عطلة رسمية</span></>
                                    )}
                                </button>
                            </div>

                            {/* قسم 2: إضافة عطلة أو عيد متعدد الأيام */}
                            <div className="bg-white p-4 rounded-2xl border border-slate-200 shadow-sm space-y-3">
                                <h4 className="text-sm font-black text-slate-800 flex items-center gap-2">
                                    <span>🗓️</span>
                                    <span>إضافة نطاق عطلة رسمية أو عيد (عدة أيام):</span>
                                </h4>
                                <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
                                    <div className="space-y-1">
                                        <label className="text-xs font-bold text-slate-600">من تاريخ (تاريخ البداية):</label>
                                        <input
                                            type="date"
                                            value={holidayRangeStart}
                                            onChange={e => setHolidayRangeStart(e.target.value)}
                                            className="w-full px-3 py-2 border-2 border-slate-200 rounded-xl font-bold text-sm text-slate-800 focus:border-amber-500 focus:outline-none"
                                        />
                                    </div>
                                    <div className="space-y-1">
                                        <label className="text-xs font-bold text-slate-600">إلى تاريخ (تاريخ النهاية):</label>
                                        <input
                                            type="date"
                                            value={holidayRangeEnd}
                                            onChange={e => setHolidayRangeEnd(e.target.value)}
                                            className="w-full px-3 py-2 border-2 border-slate-200 rounded-xl font-bold text-sm text-slate-800 focus:border-amber-500 focus:outline-none"
                                        />
                                    </div>
                                </div>
                                <button
                                    type="button"
                                    onClick={() => addOfficialHolidayRange(holidayRangeStart, holidayRangeEnd)}
                                    className="w-full py-2.5 px-4 bg-amber-500 hover:bg-amber-600 text-white font-black text-sm rounded-xl transition cursor-pointer shadow-sm flex items-center justify-center gap-2"
                                >
                                    <span>➕</span>
                                    <span>إضافة نطاق التواريخ المحددة كـ عطل رسمية</span>
                                </button>
                            </div>

                            {/* قسم 3: سجل وقائمة العطل الرسمية المعرفة */}
                            <div className="bg-white p-4 rounded-2xl border border-slate-200 shadow-sm space-y-3">
                                <div className="flex items-center justify-between border-b border-slate-100 pb-2">
                                    <h4 className="text-sm font-black text-slate-800 flex items-center gap-2">
                                        <span>📜</span>
                                        <span>سجل العطل الرسمية والأعياد المعرفة بالنظام</span>
                                    </h4>
                                    <span className="px-2.5 py-0.5 rounded-full bg-amber-100 text-amber-900 font-black text-xs">
                                        المجموع: {officialHolidays.length} يوم
                                    </span>
                                </div>

                                {officialHolidays.length === 0 ? (
                                    <div className="text-center py-6 text-slate-400 font-bold text-xs space-y-1">
                                        <p>لا توجد أي عطل رسمية معرفة بالنظام حالياً.</p>
                                        <p>يمكنك استخدام الخيارات أعلاه لتحديد العطل الرسمية والأعياد.</p>
                                    </div>
                                ) : (
                                    <div className="max-h-56 overflow-y-auto space-y-2 pr-1">
                                        {[...officialHolidays].sort().map((hDate) => (
                                            <div
                                                key={hDate}
                                                className={`flex items-center justify-between p-2.5 rounded-xl border text-xs font-bold transition ${
                                                    hDate === dailyReportDate
                                                        ? 'bg-amber-50 border-amber-300 text-amber-950 ring-1 ring-amber-300'
                                                        : 'bg-slate-50 border-slate-200 text-slate-700 hover:bg-slate-100'
                                                }`}
                                            >
                                                <div className="flex items-center gap-2">
                                                    <span className="text-base">🎉</span>
                                                    <span className="dir-ltr font-black">{hDate}</span>
                                                    {hDate === dailyReportDate && (
                                                        <span className="px-2 py-0.5 rounded-md bg-amber-200 text-amber-900 text-[10px] font-black">
                                                            التاريخ الحالي بالموقف
                                                        </span>
                                                    )}
                                                </div>
                                                <button
                                                    type="button"
                                                    onClick={() => toggleOfficialHolidayDate(hDate)}
                                                    className="px-2 py-1 rounded-lg bg-rose-100 hover:bg-rose-200 text-rose-700 font-black transition cursor-pointer text-[11px] flex items-center gap-1"
                                                    title="حذف هذه العطلة"
                                                >
                                                    <span>🗑️</span>
                                                    <span>حذف</span>
                                                </button>
                                            </div>
                                        ))}
                                    </div>
                                )}
                            </div>

                        </div>

                        {/* أسفل النافذة - أزرار الإجراءات */}
                        <div className="bg-slate-100 px-6 py-3 border-t border-slate-200 flex items-center justify-end">
                            <button
                                type="button"
                                onClick={() => setShowHolidaysModal(false)}
                                className="px-6 py-2 bg-slate-700 hover:bg-slate-800 text-white font-black rounded-xl text-xs transition cursor-pointer shadow-sm"
                            >
                                إغلاق النافذة
                            </button>
                        </div>
                    </div>
                </div>
            )}

            {pendingShiftConfirm && ("""

code = code.replace(old_modal_anchor, new_modal_code)


# Save local offline v6.8
with open('نظام_ادراة_الملاك_v6.8.html', 'w', encoding='utf-8') as f:
    f.write(code)

print('Successfully generated نظام_ادراة_الملاك_v6.8.html')

# Generate online v6.8
online_code = code
online_code = online_code.replace('<script src="libs/react.production.min.js"></script>', '<script src="https://unpkg.com/react@18/umd/react.production.min.js"></script>')
online_code = online_code.replace('<script src="libs/react-dom.production.min.js"></script>', '<script src="https://unpkg.com/react-dom@18/umd/react-dom.production.min.js"></script>')
online_code = online_code.replace('<script src="libs/babel.min.js"></script>', '<script src="https://unpkg.com/@babel/standalone@7.26.2/babel.min.js"></script>')
online_code = online_code.replace('<script src="libs/tailwindcss.js"></script>', '<script src="https://cdn.tailwindcss.com"></script>')
online_code = online_code.replace('<script src="libs/xlsx.full.min.js"></script>', '<script src="https://cdn.jsdelivr.net/npm/xlsx@0.18.5/dist/xlsx.full.min.js"></script>')
online_code = online_code.replace('<script src="libs/exceljs.min.js"></script>', '<script src="https://cdn.jsdelivr.net/npm/exceljs@4.4.0/dist/exceljs.min.js"></script>')
online_code = online_code.replace('<script src="libs/docx.js"></script>', '<script src="https://cdn.jsdelivr.net/npm/docx@8.5.0/build/index.umd.js"></script>')
online_code = online_code.replace('<script src="libs/FileSaver.min.js"></script>', '<script src="https://cdn.jsdelivr.net/npm/file-saver@2.0.5/dist/FileSaver.min.js"></script>')

with open('نظام_ادراة_الملاك_v6.8_online.html', 'w', encoding='utf-8') as f:
    f.write(online_code)

print('Successfully generated online v6.8 file')

# Copy to Desktop
desktop_dir = r'C:\Users\asalz\OneDrive\Desktop'
if os.path.exists(desktop_dir):
    with open(os.path.join(desktop_dir, 'نظام_ادراة_الملاك_v6.8.html'), 'w', encoding='utf-8') as f:
        f.write(code)
    with open(os.path.join(desktop_dir, 'نظام_ادراة_الملاك_v6.8_online.html'), 'w', encoding='utf-8') as f:
        f.write(online_code)
    print('Successfully copied v6.8 files to OneDrive Desktop')
