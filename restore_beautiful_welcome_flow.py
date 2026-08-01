import os

def update_file(file_path):
    if not os.path.exists(file_path):
        print(f"File not found: {file_path}")
        return False

    with open(file_path, 'r', encoding='utf-8') as f:
        code = f.read()

    # 1. Update condition for showing Login Modal to only show when showLoginModal is true
    old_modal_cond = "{(showLoginModal || !currentUserRole) && ("
    new_modal_cond = "{showLoginModal && ("

    if old_modal_cond in code:
        code = code.replace(old_modal_cond, new_modal_cond)
        print(f"✓ Updated Login Modal render condition to showLoginModal in {file_path}")

    # 2. Make sure Start Button in Welcome Modal always sets showLoginModal(true)
    old_start_btn = """                                        <button 
                                            onClick={() => {
                                                if (!currentUserRole) {
                                                    setShowLoginModal(true);
                                                } else {
                                                    setShowWelcome(false);
                                                }
                                            }}
                                            className="px-8 py-3 bg-gradient-to-r from-green-500 to-emerald-600 hover:from-green-600 hover:to-emerald-700 text-white rounded-lg font-bold text-lg transition-all transform hover:scale-105 shadow-xl border-2 border-white border-opacity-30">
                                            ✓ ابدأ العمل الآن
                                        </button>"""

    new_start_btn = """                                        <button 
                                            onClick={() => setShowLoginModal(true)}
                                            className="px-8 py-3 bg-gradient-to-r from-green-500 to-emerald-600 hover:from-green-600 hover:to-emerald-700 text-white rounded-lg font-bold text-lg transition-all transform hover:scale-105 shadow-xl border-2 border-white border-opacity-30">
                                            ✓ ابدأ العمل الآن
                                        </button>"""

    if old_start_btn in code:
        code = code.replace(old_start_btn, new_start_btn)
        print(f"✓ Updated Start Button to open Login Modal in {file_path}")

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(code)
    return True

if __name__ == '__main__':
    update_file('e:/Antigravity projects/HR Admin/index.html')
    update_file('e:/Antigravity projects/HR Admin/نظام_ادراة_الملاك_v6.9_online.html')
    update_file('e:/Antigravity projects/HR Admin/نظام_ادراة_الملاك_v6.9.html')
