import os

def update_file(file_path):
    if not os.path.exists(file_path):
        print(f"File not found: {file_path}")
        return False

    with open(file_path, 'r', encoding='utf-8') as f:
        code = f.read()

    # 1. Do NOT persist currentUserRole in localStorage so every fresh page load requires password
    old_role_state = """            const [currentUserRole, setCurrentUserRole] = useState(() => {
                return localStorage.getItem('currentUserRole') || null;
            });"""

    new_role_state = """            const [currentUserRole, setCurrentUserRole] = useState(null);"""

    if old_role_state in code:
        code = code.replace(old_role_state, new_role_state)
        print(f"✓ Reset currentUserRole to null on initial load in {file_path}")

    # Remove localStorage.setItem('currentUserRole', ...) calls if any
    code = code.replace("localStorage.setItem('currentUserRole', 'admin');", "")
    code = code.replace("localStorage.setItem('currentUserRole', 'operator');", "")
    code = code.replace("localStorage.setItem('currentUserRole', 'viewer');", "")
    code = code.replace("localStorage.removeItem('currentUserRole');", "")

    # 2. Strict PIN checking in handleLogin (do NOT allow empty string as valid PIN unless viewer button clicked)
    old_handle_login = """            const handleLogin = (e) => {
                if (e) e.preventDefault();
                setLoginError('');
                const inputPin = loginInputPin.trim();

                if (inputPin === passwordsConfig.admin) {
                    setCurrentUserRole('admin');
                    localStorage.setItem('currentUserRole', 'admin');
                    setShowWelcome(false);
                    setLoginInputPin('');
                    setShowLoginModal(false);
                } else if (inputPin === passwordsConfig.operator) {
                    setCurrentUserRole('operator');
                    localStorage.setItem('currentUserRole', 'operator');
                    setShowWelcome(false);
                    setLoginInputPin('');
                    setShowLoginModal(false);
                } else if (inputPin === passwordsConfig.viewer || inputPin === '') {
                    setCurrentUserRole('viewer');
                    localStorage.setItem('currentUserRole', 'viewer');
                    setShowWelcome(false);
                    setLoginInputPin('');
                    setShowLoginModal(false);
                } else {
                    setLoginError('❌ كلمة المرور غير صحيحة!');
                }
            };"""

    new_handle_login = """            const handleLogin = (e) => {
                if (e) e.preventDefault();
                setLoginError('');
                const inputPin = loginInputPin.trim();

                if (!inputPin) {
                    setLoginError('⚠️ يرجى إدخال كلمة المرور للدخول للنظام!');
                    return;
                }

                if (inputPin === passwordsConfig.admin) {
                    setCurrentUserRole('admin');
                    setShowWelcome(false);
                    setLoginInputPin('');
                    setShowLoginModal(false);
                } else if (inputPin === passwordsConfig.operator) {
                    setCurrentUserRole('operator');
                    setShowWelcome(false);
                    setLoginInputPin('');
                    setShowLoginModal(false);
                } else if (inputPin === passwordsConfig.viewer) {
                    setCurrentUserRole('viewer');
                    setShowWelcome(false);
                    setLoginInputPin('');
                    setShowLoginModal(false);
                } else {
                    setLoginError('❌ كلمة المرور غير صحيحة!');
                }
            };"""

    if old_handle_login in code:
        code = code.replace(old_handle_login, new_handle_login)
        print(f"✓ Made handleLogin PIN check strict in {file_path}")

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(code)
    return True

if __name__ == '__main__':
    update_file('e:/Antigravity projects/HR Admin/index.html')
    update_file('e:/Antigravity projects/HR Admin/نظام_ادراة_الملاك_v6.9_online.html')
    update_file('e:/Antigravity projects/HR Admin/نظام_ادراة_الملاك_v6.9.html')
