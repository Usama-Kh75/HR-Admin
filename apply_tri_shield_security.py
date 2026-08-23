import os

files_to_secure = [
    'e:/Antigravity projects/HR Admin/index.html',
    'e:/Antigravity projects/HR Admin/نظام_ادارة_الملاك_v8.0_cloud.html',
    r'C:\Users\asalz\OneDrive\Desktop\index.html'
]

anti_f12_script = """
    <!-- درع الحماية الشامل ضد التفتيش والـ F12 (Anti-Inspect & Zero Data Leakage Shield) -->
    <script>
        (function() {
            // 1. حظر النقر بزر الفأرة الأيمن
            document.addEventListener('contextmenu', function(e) {
                e.preventDefault();
                return false;
            }, { capture: true });

            // 2. حظر مفتاح F12 وكافة اختصارات أدوات المطورين وكود المصدر
            document.addEventListener('keydown', function(e) {
                // F12
                if (e.key === 'F12' || e.keyCode === 123) {
                    e.preventDefault();
                    e.stopPropagation();
                    return false;
                }
                // Ctrl+Shift+I (Inspect), Ctrl+Shift+J (Console), Ctrl+Shift+C (Element picker)
                if (e.ctrlKey && e.shiftKey && ['I', 'i', 'J', 'j', 'C', 'c', 'K', 'k'].includes(e.key)) {
                    e.preventDefault();
                    e.stopPropagation();
                    return false;
                }
                // Ctrl+U (View Source), Ctrl+S (Save page)
                if (e.ctrlKey && ['u', 'U', 's', 'S', 'p', 'P'].includes(e.key) && e.key.toLowerCase() !== 'p') {
                    e.preventDefault();
                    e.stopPropagation();
                    return false;
                }
            }, { capture: true });

            // 3. فخ المطورين الأمني (DevTools Trap): يمنع التفتيش بالمتصفح
            setInterval(function() {
                const startTime = performance.now();
                // debugger probe
                (function() {})['constructor']('debugger')();
                const endTime = performance.now();
                if (endTime - startTime > 100) {
                    // إذا فُتحت أدوات المطورين، يتم حجب الصفحة
                    document.body.style.filter = 'blur(20px)';
                } else {
                    if (document.body && document.body.style.filter === 'blur(20px)') {
                        document.body.style.filter = 'none';
                    }
                }
            }, 1000);
        })();
    </script>
</head>"""

for file_path in files_to_secure:
    if os.path.exists(file_path):
        with open(file_path, 'r', encoding='utf-8') as f:
            code = f.read()
        
        # Inject anti-f12 script before </head>
        if '</head>' in code and 'Anti-Inspect' not in code:
            code = code.replace('</head>', anti_f12_script, 1)
            print(f"✓ Injected Anti-F12 Client Shield into {os.path.basename(file_path)}")

        # Condition fetchCloudData only when logged in (Zero Data Before PIN)
        old_sync_effect = """            React.useEffect(() => {
                fetchCloudData();
                const interval = setInterval(fetchCloudData, 5000);
                return () => clearInterval(interval);
            }, []);"""

        new_sync_effect = """            React.useEffect(() => {
                // حظر جلب أو استهلاك البيانات السحابية طالما المستخدم في شاشة القفل (حماية من تسريب الذاكرة)
                if (currentUserRole) {
                    fetchCloudData();
                    const interval = setInterval(fetchCloudData, 5000);
                    return () => clearInterval(interval);
                }
            }, [currentUserRole]);"""

        if old_sync_effect in code:
            code = code.replace(old_sync_effect, new_sync_effect, 1)
            print(f"✓ Enabled Zero-Data-Before-PIN guard in {os.path.basename(file_path)}")

        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(code)

print("✓ Completed Tri-Shield Security Implementation!")
