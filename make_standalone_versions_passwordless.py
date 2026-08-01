import os

def set_standalone_passwordless(file_path):
    if not os.path.exists(file_path):
        print(f"File not found: {file_path}")
        return False

    with open(file_path, 'r', encoding='utf-8') as f:
        code = f.read()

    # 1. Default role to 'admin' so standalone version opens with 100% full permissions automatically without login
    old_role_init = "const [currentUserRole, setCurrentUserRole] = useState(null);"
    new_role_init = "const [currentUserRole, setCurrentUserRole] = useState('admin');"

    if old_role_init in code:
        code = code.replace(old_role_init, new_role_init)
        print(f"✓ Defaulted currentUserRole to 'admin' (passwordless) in {file_path}")

    # 2. Start button in welcome screen goes directly to main app (setShowWelcome(false))
    old_start_btn = """                                        <button 
                                            onClick={() => setShowLoginModal(true)}
                                            className="px-8 py-3 bg-gradient-to-r from-green-500 to-emerald-600 hover:from-green-600 hover:to-emerald-700 text-white rounded-lg font-bold text-lg transition-all transform hover:scale-105 shadow-xl border-2 border-white border-opacity-30">
                                            ✓ ابدأ العمل الآن
                                        </button>"""

    new_start_btn = """                                        <button 
                                            onClick={() => setShowWelcome(false)}
                                            className="px-8 py-3 bg-gradient-to-r from-green-500 to-emerald-600 hover:from-green-600 hover:to-emerald-700 text-white rounded-lg font-bold text-lg transition-all transform hover:scale-105 shadow-xl border-2 border-white border-opacity-30">
                                            ✓ ابدأ العمل الآن
                                        </button>"""

    if old_start_btn in code:
        code = code.replace(old_start_btn, new_start_btn)
        print(f"✓ Updated Start Button to enter app directly without login modal in {file_path}")

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(code)
    return True

if __name__ == '__main__':
    # Apply passwordless mode to standalone files ONLY
    set_standalone_passwordless('e:/Antigravity projects/HR Admin/نظام_ادراة_الملاك_v6.9_online.html')
    set_standalone_passwordless('e:/Antigravity projects/HR Admin/نظام_ادراة_الملاك_v6.9.html')
