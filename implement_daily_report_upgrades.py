import os

with open('e:/Antigravity projects/HR Admin/index.html', 'r', encoding='utf-8') as f:
    code = f.read()

# 1. Add "تعذر وصول (قطع طرق / ظرف طارئ)" and "توقف موقع (قوة قاهرة)" to status dropdowns and stats
old_status_options = """                                                                                         <option value="استراحة ذوي الاحتياجات الخاصة" className="bg-white text-teal-800 font-bold">♿ استراحة ذوي الاحتياجات الخاصة</option>
                                                                                         <option value="غياب" className="bg-white text-red-700 font-bold">❌ غياب</option>"""

new_status_options = """                                                                                         <option value="استراحة ذوي الاحتياجات الخاصة" className="bg-white text-teal-800 font-bold">♿ استراحة ذوي الاحتياجات الخاصة</option>
                                                                                         <option value="تعذر وصول (قطع طرق / ظرف طارئ)" className="bg-white text-amber-800 font-bold">🚧 تعذر وصول (قطع طرق / ظرف طارئ)</option>
                                                                                         <option value="توقف موقع (قوة قاهرة)" className="bg-white text-orange-900 font-bold">🛑 توقف موقع (قوة قاهرة)</option>
                                                                                         <option value="غياب" className="bg-white text-red-700 font-bold">❌ غياب</option>"""

if old_status_options in code:
    code = code.replace(old_status_options, new_status_options)
    print("✓ Added 'تعذر وصول' and 'توقف موقع' options to daily status dropdown")

# 2. Add shareViaWhatsApp function
share_whatsapp_fn = """            // مشاركة تقرير الموقف أو نتائج الاستعلام عبر تطبيق الواتساب مباشرة
            const shareViaWhatsApp = () => {
                if (!previewData || previewData.length === 0) {
                    alert('⚠️ لا توجد بيانات للمشاركة حالياً.');
                    return;
                }
                let text = `📋 *${previewTitle || 'تقرير الموقف الموحد'}*\\n`;
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
                
                const url = `https://api.whatsapp.com/send?text=${encodeURIComponent(text)}`;
                if (navigator.share && /mobile|android|iphone/i.test(navigator.userAgent)) {
                    navigator.share({ title: previewTitle || 'موقف الشعبة', text: text }).catch(() => window.open(url, '_blank'));
                } else {
                    window.open(url, '_blank');
                }
            };"""

# Insert shareViaWhatsApp before printPreview
print_preview_tag = "const printPreview = () => {"
if print_preview_tag in code:
    code = code.replace(print_preview_tag, share_whatsapp_fn + "\n\n            " + print_preview_tag, 1)
    print("✓ Added shareViaWhatsApp function")

# 3. Add WhatsApp button in preview footer
old_preview_footer = """                                    <button onClick={printPreview}
                                        className="px-6 py-3 bg-purple-500 text-white rounded-lg hover:bg-purple-600 font-bold transition shadow-lg">
                                        🖨️ طباعة
                                    </button>"""

new_preview_footer = """                                    <button onClick={shareViaWhatsApp}
                                        className="px-5 py-3 bg-emerald-600 text-white rounded-lg hover:bg-emerald-700 font-bold transition shadow-lg flex items-center gap-1.5">
                                        <span>📲</span>
                                        <span>إرسال عبر واتساب</span>
                                    </button>

                                    <button onClick={printPreview}
                                        className="px-6 py-3 bg-purple-500 text-white rounded-lg hover:bg-purple-600 font-bold transition shadow-lg">
                                        🖨️ طباعة
                                    </button>"""

if old_preview_footer in code:
    code = code.replace(old_preview_footer, new_preview_footer)
    print("✓ Injected WhatsApp button into preview footer")

# 4. Super-Compact Print CSS (Reduce 6 pages down to 2-3 pages!)
old_print_css_start = "/* تنسيق الطباعة */\n        @media print {"
old_print_css_end = "/* تنسيق طباعة بطاقة الموظف A4 */"

compact_print_css = """/* تنسيق الطباعة عالي الكثافة (توفير الورق وتقليص الصفحات من 6 إلى 2-3 صفحات) */
        @media print {
            @page {
                size: A4 portrait;
                margin: 6mm 5mm 6mm 5mm;
            }
            body { background: white !important; margin: 0 !important; padding: 0 !important; font-size: 7.5pt !important; }
            
            /* إخفاء كل شيء ما عدا المعاينة */
            header, nav, main, footer, .no-print, button { display: none !important; }
            
            /* إظهار المعاينة فقط */
            .preview-overlay { 
                background: white !important; 
                position: static !important; 
                display: block !important; 
                padding: 0 !important;
                margin: 0 !important;
            }
            
            .preview-container { 
                box-shadow: none !important; 
                max-width: 100% !important; 
                max-height: none !important;
                border-radius: 0 !important;
                border: none !important;
            }
            
            /* العنوان المصغر والأنيق */
            .preview-header { 
                background: white !important; 
                color: black !important; 
                border-bottom: 1.5px solid #000 !important; 
                page-break-after: avoid;
                padding: 2px 5px !important;
                margin-bottom: 3px !important;
            }
            .preview-header * { display: none !important; }
            .preview-header h2 { 
                display: block !important; 
                color: black !important; 
                font-size: 11pt !important; 
                font-weight: 900 !important; 
                margin: 0 !important; 
                padding: 1px 0 !important; 
                text-align: center !important; 
            }
            
            .preview-footer { display: none !important; }
            
            /* محتوى الجدول فائق التكثيف */
            .preview-body { 
                max-height: none !important; 
                overflow: visible !important; 
                padding: 0 !important; 
            }
            
            .preview-table { 
                font-size: 7.5pt !important; 
                page-break-inside: auto;
                width: 100% !important;
                border-collapse: collapse !important;
                line-height: 1.15 !important;
            }
            
            .preview-table thead { 
                display: table-header-group;
                background: #e2e8f0 !important;
            }
            
            .preview-table tr { 
                page-break-inside: avoid; 
                page-break-after: auto; 
                height: 18px !important;
            }
            
            .preview-table th { 
                background: #f1f5f9 !important; 
                color: black !important; 
                border: 1px solid #1e293b !important; 
                padding: 2.5px 3px !important; 
                font-weight: 900 !important;
                font-size: 7.5pt !important;
            }
            
            .preview-table td { 
                border: 1px solid #64748b !important; 
                padding: 1.5px 3px !important; 
                color: black !important; 
                background: white !important;
                font-size: 7.5pt !important;
            }
            
            .preview-table tbody tr:nth-child(even) td {
                background: #f8fafc !important;
            }
            
            /* فواصل المواقع المدمجة */
            .location-separator { 
                background: #cbd5e1 !important; 
                color: black !important; 
                font-weight: 900 !important; 
                font-size: 8pt !important;
                padding: 2px 4px !important;
                page-break-after: avoid !important;
            }
            
            .merged-cell {
                background: #fffbeb !important;
                vertical-align: top !important;
            }
            
            .editable-cell { 
                border: none !important; 
                padding: 0 !important; 
                font-size: 7.5pt !important;
                background: transparent !important;
            }
            
            input { border: none !important; background: transparent !important; }
            
            /* تذييل وتوقيعات مكثفة لا تستهلك صفحات إضافية */
            .preview-signatures-row {
                margin-top: 10px !important;
                margin-bottom: 6px !important;
                padding: 0 15px !important;
                page-break-inside: avoid !important;
            }
            .preview-signatures-row p {
                font-size: 8.5pt !important;
                font-weight: 900 !important;
            }
            .preview-page-footer {
                margin-top: 4px !important;
                padding-top: 2px !important;
                font-size: 6.5pt !important;
                page-break-inside: avoid !important;
            }
        }
        
        """

s_pos = code.find("/* تنسيق الطباعة */\n        @media print {")
e_pos = code.find("/* تنسيق طباعة بطاقة الموظف A4 */")

if s_pos != -1 and e_pos != -1:
    code = code[:s_pos] + compact_print_css + code[e_pos:]
    print("✓ Injected ultra-compact print CSS (saving up to 60% of print pages)")

with open('e:/Antigravity projects/HR Admin/index.html', 'w', encoding='utf-8') as f:
    f.write(code)

with open('e:/Antigravity projects/HR Admin/نظام_ادراة_الملاك_v7.5_cloud.html', 'w', encoding='utf-8') as f:
    f.write(code)

print("✓ Completed Daily Report upgrades script!")
