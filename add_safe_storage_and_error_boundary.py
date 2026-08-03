import os
import re

def update_file_with_safe_storage(file_path):
    if not os.path.exists(file_path):
        print(f"File not found: {file_path}")
        return False

    with open(file_path, 'r', encoding='utf-8') as f:
        code = f.read()

    # Define safeStorage helper with in-memory fallback for Android content:// URI scheme
    safe_storage_def = """            // آمن لبيئة أندرويد و content:// URI لمنع الشاشة البيضاء عند حظر localStorage
            const memoryStorage = {};
            const safeStorage = {
                getItem: (key) => {
                    try {
                        if (typeof window !== 'undefined' && window.localStorage) {
                            return window.localStorage.getItem(key);
                        }
                    } catch (e) {
                        console.warn('localStorage getItem fallback:', e);
                    }
                    return memoryStorage[key] || null;
                },
                setItem: (key, val) => {
                    try {
                        if (typeof window !== 'undefined' && window.localStorage) {
                            window.localStorage.setItem(key, val);
                            return;
                        }
                    } catch (e) {
                        console.warn('localStorage setItem fallback:', e);
                    }
                    memoryStorage[key] = val;
                }
            };
"""

    if "const safeStorage =" not in code:
        # Insert safeStorage definition right after const App = () => { or inside component
        code = code.replace("const App = () => {", safe_storage_def + "\n            const App = () => {")
        print(f"✓ Added safeStorage in {file_path}")

    # Replace localStorage.getItem with safeStorage.getItem and localStorage.setItem with safeStorage.setItem
    code = code.replace("localStorage.getItem(", "safeStorage.getItem(")
    code = code.replace("localStorage.setItem(", "safeStorage.setItem(")

    # Add ErrorBoundary around ReactDOM.render
    old_render = """ReactDOM.render(<App />, document.getElementById('root'));"""
    new_render = """class ErrorBoundary extends React.Component {
    constructor(props) { super(props); this.state = { hasError: false, error: null }; }
    static getDerivedStateFromError(error) { return { hasError: true, error }; }
    componentDidCatch(error, errorInfo) { console.error("App Crash:", error, errorInfo); }
    render() {
        if (this.state.hasError) {
            return (
                <div style={{ padding: 20, textAlign: 'center', fontFamily: 'sans-serif', direction: 'rtl' }}>
                    <h2 style={{ color: '#e11d48' }}>⚠️ حدث خطأ أثناء تشغيل النافذة على جهازك</h2>
                    <p style={{ color: '#475569' }}>يرجى فتح الملف عبر متصفح Chrome أو كتابة رابط السيرفر المحلي.</p>
                    <pre style={{ background: '#f1f5f9', padding: 10, borderRadius: 8, fontSize: 11, textAlign: 'left', direction: 'ltr' }}>
                        {String(this.state.error)}
                    </pre>
                </div>
            );
        }
        return this.props.children;
    }
}
ReactDOM.render(<ErrorBoundary><App /></ErrorBoundary>, document.getElementById('root'));"""

    if old_render in code:
        code = code.replace(old_render, new_render)
        print(f"✓ Wrapped App with ErrorBoundary in {file_path}")

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(code)
    return True

if __name__ == '__main__':
    update_file_with_safe_storage('e:/Antigravity projects/HR Admin/index.html')
    update_file_with_safe_storage('e:/Antigravity projects/HR Admin/نظام_ادراة_الملاك_v7.0_online.html')
    update_file_with_safe_storage('e:/Antigravity projects/HR Admin/نظام_ادراة_الملاك_v7.0.html')
