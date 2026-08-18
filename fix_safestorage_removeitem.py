import os

with open('e:/Antigravity projects/HR Admin/index.html', 'r', encoding='utf-8') as f:
    code = f.read()

old_safe_storage = """            const safeStorage = {
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

new_safe_storage = """            const safeStorage = {
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
                },
                removeItem: (key) => {
                    try {
                        if (typeof window !== 'undefined' && window.localStorage) {
                            window.localStorage.removeItem(key);
                            return;
                        }
                    } catch (e) {
                        console.warn('localStorage removeItem fallback:', e);
                    }
                    delete memoryStorage[key];
                },
                clear: () => {
                    try {
                        if (typeof window !== 'undefined' && window.localStorage) {
                            window.localStorage.clear();
                            return;
                        }
                    } catch (e) {
                        console.warn('localStorage clear fallback:', e);
                    }
                    for (const k in memoryStorage) delete memoryStorage[k];
                }
            };"""

if old_safe_storage in code:
    code = code.replace(old_safe_storage, new_safe_storage)
    print("✓ Successfully added removeItem and clear to safeStorage in index.html")

with open('e:/Antigravity projects/HR Admin/index.html', 'w', encoding='utf-8') as f:
    f.write(code)

with open('e:/Antigravity projects/HR Admin/نظام_ادراة_الملاك_v7.5_cloud.html', 'w', encoding='utf-8') as f:
    f.write(code)
