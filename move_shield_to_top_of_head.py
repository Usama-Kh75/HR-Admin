import os

with open('e:/Antigravity projects/HR Admin/index.html', 'r', encoding='utf-8') as f:
    code = f.read()

# 1. Remove script from old position
old_script_block = """    <!-- درع الحماية الشامل ضد التفتيش والـ F12 (Anti-Inspect & Zero Data Leakage Shield) -->
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
    </script>"""

if old_script_block in code:
    code = code.replace(old_script_block, "")

# 2. Add ultra-fast top shield right after <head>
top_head_shield = """<head>
    <!-- درع الحماية الفوري الشامل في أول سطر بالصفحة لمنع F12 والتفتيش فورياً -->
    <script>
        (function() {
            function blockAction(e) {
                e = e || window.event;
                if (!e) return true;
                
                // Block F12 (code 123)
                if (e.key === 'F12' || e.keyCode === 123 || e.which === 123) {
                    if (e.preventDefault) e.preventDefault();
                    if (e.stopPropagation) e.stopPropagation();
                    e.returnValue = false;
                    return false;
                }
                // Block Ctrl+Shift+I, Ctrl+Shift+J, Ctrl+Shift+C, Ctrl+Shift+K
                if (e.ctrlKey && e.shiftKey && (e.keyCode === 73 || e.keyCode === 74 || e.keyCode === 67 || e.keyCode === 75 || ['I','i','J','j','C','c','K','k'].includes(e.key))) {
                    if (e.preventDefault) e.preventDefault();
                    if (e.stopPropagation) e.stopPropagation();
                    e.returnValue = false;
                    return false;
                }
                // Block Ctrl+U (View Source)
                if (e.ctrlKey && (e.keyCode === 85 || e.key === 'u' || e.key === 'U')) {
                    if (e.preventDefault) e.preventDefault();
                    if (e.stopPropagation) e.stopPropagation();
                    e.returnValue = false;
                    return false;
                }
            }

            // Bind to all capture stages immediately
            window.addEventListener('keydown', blockAction, true);
            document.addEventListener('keydown', blockAction, true);
            window.onkeydown = blockAction;
            document.onkeydown = blockAction;

            // Block Context Menu (Right Click)
            function blockContext(e) {
                if (e && e.preventDefault) e.preventDefault();
                return false;
            }
            window.addEventListener('contextmenu', blockContext, true);
            document.addEventListener('contextmenu', blockContext, true);
            window.oncontextmenu = blockContext;
            document.oncontextmenu = blockContext;
        })();
    </script>"""

if "<head>" in code:
    code = code.replace("<head>", top_head_shield, 1)
    print("✓ Placed instant Anti-F12 shield in line 1 of <head>")

with open('e:/Antigravity projects/HR Admin/index.html', 'w', encoding='utf-8') as f:
    f.write(code)

with open('e:/Antigravity projects/HR Admin/نظام_ادارة_الملاك_v8.0_cloud.html', 'w', encoding='utf-8') as f:
    f.write(code)

with open(r'C:\Users\asalz\OneDrive\Desktop\index.html', 'w', encoding='utf-8') as f:
    f.write(code)

print("✓ Successfully updated files!")
