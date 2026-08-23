import os

with open('e:/Antigravity projects/HR Admin/index.html', 'r', encoding='utf-8') as f:
    code = f.read()

# 1. Update daily status options to include "ورقة عمل" and "تعذر حضور (قطع طرق / ظرف طارئ)"
old_dropdown_options = """                                                                                         <option value="استراحة ذوي الاحتياجات الخاصة" className="bg-white text-teal-800 font-bold">♿ استراحة ذوي الاحتياجات الخاصة</option>
                                                                                         <option value="غياب" className="bg-white text-red-700 font-bold">❌ غياب</option>"""

new_dropdown_options = """                                                                                         <option value="ورقة عمل" className="bg-white text-emerald-700 font-bold">📝 ورقة عمل</option>
                                                                                         <option value="تعذر حضور (قطع طرق / ظرف طارئ)" className="bg-white text-amber-800 font-bold">🚧 تعذر حضور (قطع طرق / ظرف طارئ)</option>
                                                                                         <option value="توقف موقع (قوة قاهرة)" className="bg-white text-orange-900 font-bold">🛑 توقف موقع (قوة قاهرة)</option>
                                                                                         <option value="استراحة ذوي الاحتياجات الخاصة" className="bg-white text-teal-800 font-bold">♿ استراحة ذوي الاحتياجات الخاصة</option>
                                                                                         <option value="غياب" className="bg-white text-red-700 font-bold">❌ غياب</option>"""

if old_dropdown_options in code:
    code = code.replace(old_dropdown_options, new_dropdown_options)
    print("✓ Added 'ورقة عمل' and 'تعذر حضور' to Daily Status select options")

# 2. Refine shareViaWhatsApp to send ONLY checked columns in Search / Dashboard view cleanly
old_whatsapp_fn_start = "// مشاركة تقرير الموقف أو نتائج الاستعلام عبر تطبيق الواتساب مباشرة"
old_whatsapp_fn_end = "const printPreview = () => {"

new_whatsapp_fn = """// مشاركة تقرير الموقف أو نتائج الاستعلام عبر تطبيق الواتساب مباشرة
            const shareViaWhatsApp = () => {
                if (!previewData || previewData.length === 0) {
                    alert('⚠️ لا توجد بيانات للمشاركة حالياً.');
                    return;
                }

                let text = '';

                // حالة بطاقة البحث والاستعلام (تخصيص الأعمدة المؤشرة فقط بدون حشو)
                if (view === 'dashboard' || isCustomizable) {
                    const activeCols = visiblePreviewColumns || [];
                    const count = previewData.filter(d => d.type === 'data').length;
                    
                    text += `📋 *${previewTitle || 'بيانات المنتسبين'}*\\n`;
                    text += `🏢 شعبة تبريد المركز ومحطة عزل نهر بن عمر\\n`;
                    text += `━━━━━━━━━━━━━━━━━━━━\\n`;

                    let itemIndex = 0;
                    previewData.forEach(row => {
                        if (row.type === 'data') {
                            itemIndex++;
                            const name = row['الاسم الكامل'] || row['الأسم الكامل'] || row['الاسم'] || row['الأسم الثلاثي'] || '';
                            text += count > 1 ? `\\n*${itemIndex}. ${name}*\\n` : `👤 *${name}*\\n`;
                            
                            // إضافة الحقول المؤشرة فقط
                            activeCols.forEach(col => {
                                if (row[col] !== undefined && row[col] !== null && String(row[col]).trim() !== '') {
                                    text += `▫️ ${col}: *${row[col]}*\\n`;
                                }
                            });
                        }
                    });

                    text += `━━━━━━━━━━━━━━━━━━━━\\n`;
                    text += `📊 إجمالي العدد: ${count} منتسب\\n`;
                } else {
                    // حالة الموقف اليومي الموحد للشعبة
                    text += `📋 *${previewTitle || 'تقرير الموقف الموحد'}*\\n`;
                    text += `🏢 شركة نفط البصرة - شعبة تبريد المركز ومحطة عزل نهر بن عمر\\n`;
                    text += `📅 التاريخ: ${dailyReportDate || new Date().toISOString().split('T')[0]}\\n`;
                    text += `━━━━━━━━━━━━━━━━━━━━\\n`;
                    
                    let count = 0;
                    previewData.forEach(row => {
                        if (row.type === 'separator') {
                            text += `\\n📌 *${row.content.replace(/━/g, '').trim()}*\\n`;
                        } else if (row.type === 'data') {
                            count++;
                            const name = row['الاسم الكامل'] || row['الأسم الكامل'] || row['الاسم'] || '';
                            const jobNum = row['الرقم الوظيفي'] || row['الرقم'] || '';
                            const status = row['الموقف اليومي'] || row['طبيعة العمل'] || row['الوظيفة'] || row['العنوان الوظيفي'] || '';
                            const notes = row['الملاحظات'] || '';
                            text += `${count}. *${name}* (${jobNum}) : ${status} ${notes ? `[${notes}]` : ''}\\n`;
                        }
                    });
                    text += `━━━━━━━━━━━━━━━━━━━━\\n`;
                    text += `📊 إجمالي العدد: ${count} منتسب\\n`;
                    text += `✍️ منظم الموقف: ${dataEntryOperator || 'إدارة الشعبة'}\\n`;
                }

                const url = `https://api.whatsapp.com/send?text=${encodeURIComponent(text)}`;
                if (navigator.share && /mobile|android|iphone/i.test(navigator.userAgent)) {
                    navigator.share({ title: previewTitle || 'بيانات الموظف', text: text }).catch(() => window.open(url, '_blank'));
                } else {
                    window.open(url, '_blank');
                }
            };"""

s_idx = code.find(old_whatsapp_fn_start)
e_idx = code.find(old_whatsapp_fn_end)

if s_idx != -1 and e_idx != -1:
    code = code[:s_idx] + new_whatsapp_fn + "\n\n            " + code[e_idx:]
    print("✓ Successfully updated shareViaWhatsApp to send only checked card fields in Search view")

with open('e:/Antigravity projects/HR Admin/index.html', 'w', encoding='utf-8') as f:
    f.write(code)

with open('e:/Antigravity projects/HR Admin/نظام_ادراة_الملاك_v7.5_cloud.html', 'w', encoding='utf-8') as f:
    f.write(code)

print("✓ Completed refine_whatsapp_and_add_work_paper.py")
