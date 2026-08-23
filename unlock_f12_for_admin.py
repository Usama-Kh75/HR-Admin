import os

with open('e:/Antigravity projects/HR Admin/index.html', 'r', encoding='utf-8') as f:
    code = f.read()

# 1. Update the head shield script to check window.__IS_ADMIN_DEV_UNLOCKED
old_head_script = """    <!-- درع الحماية الفوري الشامل في أول سطر بالصفحة لمنع F12 والتفتيش فورياً -->
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

new_head_script = """    <!-- درع الحماية الذكي: محظور على العامة وشاشة القفل، ومفتوح تلقائياً لمدير النظام (Admin) للتشخيص والتطوير -->
    <script>
        window.__IS_ADMIN_DEV_UNLOCKED = false;
        (function() {
            function blockAction(e) {
                // إذا كان المستخدم مسجلاً كـ مدير نظام (Admin) أو قام بفتح قفل المطورين: يُسمح له بـ F12 والتفتيش فوراً!
                if (window.__IS_ADMIN_DEV_UNLOCKED === true) {
                    return true;
                }

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

            // Block Context Menu (Right Click) for non-admins
            function blockContext(e) {
                if (window.__IS_ADMIN_DEV_UNLOCKED === true) return true;
                if (e && e.preventDefault) e.preventDefault();
                return false;
            }
            window.addEventListener('contextmenu', blockContext, true);
            document.addEventListener('contextmenu', blockContext, true);
            window.oncontextmenu = blockContext;
            document.oncontextmenu = blockContext;
        })();
    </script>"""

if old_head_script in code:
    code = code.replace(old_head_script, new_head_script)
    print("✓ Updated head script with Admin F12 Unlock logic")

# 2. Update React useEffect to set window.__IS_ADMIN_DEV_UNLOCKED = true when currentUserRole === 'admin'
old_guard_effect = """            React.useEffect(() => {
                // حظر جلب أو استهلاك البيانات السحابية طالما المستخدم في شاشة القفل (حماية من تسريب الذاكرة)
                if (currentUserRole) {
                    fetchCloudData();
                    const interval = setInterval(fetchCloudData, 5000);
                    return () => clearInterval(interval);
                }
            }, [currentUserRole]);"""

new_guard_effect = """            React.useEffect(() => {
                // السماح بأدوات المطورين F12 وفحص النظام حصرياً لمدير النظام (Admin)
                if (currentUserRole === 'admin') {
                    window.__IS_ADMIN_DEV_UNLOCKED = true;
                } else {
                    window.__IS_ADMIN_DEV_UNLOCKED = false;
                }

                // حظر جلب أو استهلاك البيانات السحابية طالما المستخدم في شاشة القفل (حماية من تسريب الذاكرة)
                if (currentUserRole) {
                    fetchCloudData();
                    const interval = setInterval(fetchCloudData, 5000);
                    return () => clearInterval(interval);
                }
            }, [currentUserRole]);"""

if old_guard_effect in code:
    code = code.replace(old_guard_effect, new_guard_effect)
    print("✓ Linked currentUserRole === 'admin' to unlock F12 and DevTools")

with open('e:/Antigravity projects/HR Admin/index.html', 'w', encoding='utf-8') as f:
    f.write(code)

with open('e:/Antigravity projects/HR Admin/نظام_ادارة_الملاك_v8.0_cloud.html', 'w', encoding='utf-8') as f:
    f.write(code)

with open(r'C:\Users\asalz\OneDrive\Desktop\index.html', 'w', encoding='utf-8') as f:
    f.write(code)

print("✓ Completed Admin DevTools unlock script!")
