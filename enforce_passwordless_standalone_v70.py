import os

def fix_standalone(file_path):
    if not os.path.exists(file_path):
        print(f"File not found: {file_path}")
        return False

    with open(file_path, 'r', encoding='utf-8') as f:
        code = f.read()

    # 1. Set default role to 'admin' (passwordless direct entry)
    code = code.replace("const [currentUserRole, setCurrentUserRole] = useState(null);", "const [currentUserRole, setCurrentUserRole] = useState('admin');")

    # 2. Green start button enters app directly (setShowWelcome(false))
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
        print(f"✓ Fixed start button for direct entry in {file_path}")

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(code)
    print(f"✓ Fixed standalone passwordless mode in {file_path}")
    return True

if __name__ == '__main__':
    fix_standalone('e:/Antigravity projects/HR Admin/نظام_ادراة_الملاك_v7.0_online.html')
    fix_standalone('e:/Antigravity projects/HR Admin/نظام_ادراة_الملاك_v7.0.html')
