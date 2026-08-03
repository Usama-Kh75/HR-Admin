import os

def fix_scope_in_file(file_path):
    if not os.path.exists(file_path):
        print(f"File not found: {file_path}")
        return False

    with open(file_path, 'r', encoding='utf-8') as f:
        code = f.read()

    safe_storage_block = """            // آمن لبيئة أندرويد و content:// URI لمنع الشاشة البيضاء عند حظر localStorage
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
            };"""

    # 1. Remove safeStorage from wherever it was inserted previously
    code = code.replace(safe_storage_block, "")

    # 2. Insert safeStorage at the VERY START of the <script type="text/babel"> block
    babel_tag = '<script type="text/babel">'
    if babel_tag in code:
        code = code.replace(babel_tag, babel_tag + "\n" + safe_storage_block + "\n")
        print(f"✓ Positioned safeStorage at the absolute top of Babel script in {file_path}")
    else:
        print(f"Babel script tag not found in {file_path}")

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(code)
    return True

if __name__ == '__main__':
    fix_scope_in_file('e:/Antigravity projects/HR Admin/index.html')
    fix_scope_in_file('e:/Antigravity projects/HR Admin/نظام_ادراة_الملاك_v7.0_online.html')
    fix_scope_in_file('e:/Antigravity projects/HR Admin/نظام_ادراة_الملاك_v7.0.html')
