import os

def clean_standalone(file_path):
    if not os.path.exists(file_path):
        print(f"File not found: {file_path}")
        return False

    with open(file_path, 'r', encoding='utf-8') as f:
        code = f.read()

    # Target block containing role badges, change passwords button, and logout button
    rbac_header_block = """                            {/* شريط التحكم بالصفة وكلمات المرور */}
                            {currentUserRole && (
                                <div className="flex items-center gap-2 flex-shrink-0">
                                    <div className="flex items-center gap-1.5 px-3 py-1 bg-white/15 backdrop-blur-md rounded-full border border-white/20 text-xs font-extrabold text-white shadow-sm">
                                        <span>{currentUserRole === 'admin' ? '👑 مدير النظام' : (currentUserRole === 'operator' ? '✍️ إداري مُدخل' : '👁️ مستعرض')}</span>
                                    </div>
                                    {currentUserRole === 'admin' && (
                                        <button
                                            onClick={() => setShowChangePasswordModal(true)}
                                            className="px-3 py-1 bg-amber-500 hover:bg-amber-600 text-white rounded-full text-xs font-bold shadow transition flex items-center gap-1"
                                            title="تغيير كلمات المرور للنظام"
                                        >
                                            🔑 كلمات المرور
                                        </button>
                                    )}
                                    <button
                                        onClick={handleLogout}
                                        className="px-3 py-1 bg-red-500/80 hover:bg-red-600 text-white rounded-full text-xs font-bold shadow transition flex items-center gap-1"
                                        title="تسجيل الخروج أو تبديل الصفة"
                                    >
                                        🚪 خروج
                                    </button>
                                </div>
                            )}"""

    if rbac_header_block in code:
        code = code.replace(rbac_header_block, "")
        print(f"✓ Removed RBAC role badges & buttons from header in {file_path}")

    # Also make sure showLoginModal & showChangePasswordModal HTML is not rendered in standalone files if needed
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(code)
    return True

if __name__ == '__main__':
    clean_standalone('e:/Antigravity projects/HR Admin/نظام_ادراة_الملاك_v7.0_online.html')
    clean_standalone('e:/Antigravity projects/HR Admin/نظام_ادراة_الملاك_v7.0.html')
