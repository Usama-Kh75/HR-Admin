import os
import re

def update_file(file_path):
    if not os.path.exists(file_path):
        print(f"File not found: {file_path}")
        return False

    with open(file_path, 'r', encoding='utf-8') as f:
        code = f.read()

    # 1. Update handleLogin function for smart auto-detection by PIN alone
    old_handle_login = """            const handleLogin = (e) => {
                if (e) e.preventDefault();
                setLoginError('');
                const inputPin = loginInputPin.trim();

                if (loginInputRole === 'admin') {
                    if (inputPin === passwordsConfig.admin) {
                        setCurrentUserRole('admin');
                        localStorage.setItem('currentUserRole', 'admin');
                        setLoginInputPin('');
                    } else {
                        setLoginError('❌ كلمة المرور غير صحيحة لمدير النظام!');
                    }
                } else if (loginInputRole === 'operator') {
                    if (inputPin === passwordsConfig.operator || inputPin === passwordsConfig.admin) {
                        const role = inputPin === passwordsConfig.admin ? 'admin' : 'operator';
                        setCurrentUserRole(role);
                        localStorage.setItem('currentUserRole', role);
                        setLoginInputPin('');
                    } else {
                        setLoginError('❌ كلمة المرور غير صحيحة للإداري مدخل البيانات!');
                    }
                } else if (loginInputRole === 'viewer') {
                    if (inputPin === passwordsConfig.viewer || inputPin === passwordsConfig.operator || inputPin === passwordsConfig.admin || inputPin === '') {
                        const role = inputPin === passwordsConfig.admin ? 'admin' : (inputPin === passwordsConfig.operator ? 'operator' : 'viewer');
                        setCurrentUserRole(role);
                        localStorage.setItem('currentUserRole', role);
                        setLoginInputPin('');
                    } else {
                        setLoginError('❌ كلمة المرور غير صحيحة لمستعرض الملاك!');
                    }
                }
            };"""

    new_handle_login = """            const handleLogin = (e) => {
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

    if old_handle_login in code:
        code = code.replace(old_handle_login, new_handle_login)
        print(f"✓ Updated handleLogin for smart PIN auto-detection in {file_path}")

    # Add showLoginModal state
    old_show_welcome = "const [showWelcome, setShowWelcome] = useState(true);"
    new_show_welcome = "const [showWelcome, setShowWelcome] = useState(true);\n            const [showLoginModal, setShowLoginModal] = useState(false);"
    if old_show_welcome in code and "showLoginModal" not in code:
        code = code.replace(old_show_welcome, new_show_welcome)

    # 2. Update Welcome Modal green button to trigger Login Modal
    old_welcome_btn = """                                        <button 
                                            onClick={() => setShowWelcome(false)}
                                            className="px-8 py-3 bg-gradient-to-r from-green-500 to-emerald-600 hover:from-green-600 hover:to-emerald-700 text-white rounded-lg font-bold text-lg transition-all transform hover:scale-105 shadow-xl border-2 border-white border-opacity-30">
                                            ✓ ابدأ العمل الآن
                                        </button>"""

    new_welcome_btn = """                                        <button 
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

    if old_welcome_btn in code:
        code = code.replace(old_welcome_btn, new_welcome_btn)
        print(f"✓ Updated Start Button to trigger Login Modal in {file_path}")

    # 3. Update Login Modal HTML to single smart PIN input UI
    old_login_modal = """            {/* نافذة تسجيل الدخول للنظام (Login Modal) */}
            {!currentUserRole && (
                <div className="fixed inset-0 bg-slate-950/85 backdrop-blur-md z-50 flex items-center justify-center p-4">
                    <div className="bg-white rounded-3xl shadow-2xl border border-slate-100 max-w-md w-full overflow-hidden animate-fadeInUp">
                        <div className="bg-gradient-to-r from-blue-700 via-indigo-700 to-slate-900 p-6 text-white text-center relative">
                            <div className="text-4xl mb-2">🔐</div>
                            <h2 className="text-2xl font-black">نظام إدارة الملاك المتكامل</h2>
                            <p className="text-xs text-blue-200 mt-1">شركة نفط البصرة · شعبة تبريد المركز ومحطة عزل نهر بن عمر</p>
                            <div className="inline-block mt-3 px-3 py-1 bg-white/10 rounded-full text-[11px] font-bold text-blue-100">
                                الإصدار الرسمي v6.9 Beta
                            </div>
                        </div>

                        <form onSubmit={handleLogin} className="p-6 space-y-4">
                            <div className="space-y-1.5">
                                <label className="block text-xs font-black text-slate-700">اختر صفة الدخول للنظام:</label>
                                <div className="grid grid-cols-3 gap-2">
                                    <button
                                        type="button"
                                        onClick={() => { setLoginInputRole('operator'); setLoginError(''); }}
                                        className={`p-2.5 rounded-xl border text-center transition flex flex-col items-center gap-1 ${
                                            loginInputRole === 'operator' 
                                                ? 'bg-indigo-50 border-indigo-600 text-indigo-900 font-extrabold shadow-sm' 
                                                : 'bg-slate-50 border-slate-200 text-slate-600 font-bold hover:bg-slate-100'
                                        }`}
                                    >
                                        <span className="text-lg">✍️</span>
                                        <span className="text-xs">إداري مُدخل</span>
                                    </button>
                                    <button
                                        type="button"
                                        onClick={() => { setLoginInputRole('admin'); setLoginError(''); }}
                                        className={`p-2.5 rounded-xl border text-center transition flex flex-col items-center gap-1 ${
                                            loginInputRole === 'admin' 
                                                ? 'bg-amber-50 border-amber-600 text-amber-900 font-extrabold shadow-sm' 
                                                : 'bg-slate-50 border-slate-200 text-slate-600 font-bold hover:bg-slate-100'
                                        }`}
                                    >
                                        <span className="text-lg">👑</span>
                                        <span className="text-xs">مدير النظام</span>
                                    </button>
                                    <button
                                        type="button"
                                        onClick={() => { setLoginInputRole('viewer'); setLoginError(''); }}
                                        className={`p-2.5 rounded-xl border text-center transition flex flex-col items-center gap-1 ${
                                            loginInputRole === 'viewer' 
                                                ? 'bg-emerald-50 border-emerald-600 text-emerald-900 font-extrabold shadow-sm' 
                                                : 'bg-slate-50 border-slate-200 text-slate-600 font-bold hover:bg-slate-100'
                                        }`}
                                    >
                                        <span className="text-lg">👁️</span>
                                        <span className="text-xs">مستعرض</span>
                                    </button>
                                </div>
                            </div>

                            <div className="space-y-1.5">
                                <label className="block text-xs font-black text-slate-700">أدخل كلمة المرور:</label>
                                <input
                                    type="password"
                                    required
                                    placeholder="••••"
                                    value={loginInputPin}
                                    onChange={(e) => setLoginInputPin(e.target.value)}
                                    className="w-full bg-slate-50 border-2 border-slate-300 rounded-xl px-4 py-2.5 text-center text-lg font-mono font-bold outline-none focus:border-indigo-600 transition"
                                />
                            </div>

                            {loginError && (
                                <div className="p-2.5 bg-red-50 border border-red-200 text-red-700 text-xs font-bold rounded-xl text-center">
                                    {loginError}
                                </div>
                            )}

                            <button
                                type="submit"
                                className="w-full py-3 bg-gradient-to-r from-blue-600 via-indigo-600 to-indigo-800 hover:from-blue-700 hover:to-indigo-900 text-white font-bold rounded-xl text-sm shadow-lg transition transform active:scale-95 flex items-center justify-center gap-2"
                            >
                                <span>🔓</span>
                                <span>تسجيل الدخول للنظام</span>
                            </button>
                        </form>
                    </div>
                </div>
            )}"""

    new_login_modal = """            {/* نافذة تسجيل الدخول للنظام بالتعرف التلقائي الذكي على كلمة المرور */}
            {(showLoginModal || !currentUserRole) && (
                <div className="fixed inset-0 bg-slate-950/85 backdrop-blur-md z-50 flex items-center justify-center p-4">
                    <div className="bg-white rounded-3xl shadow-2xl border border-slate-100 max-w-md w-full overflow-hidden animate-fadeInUp">
                        <div className="bg-gradient-to-r from-blue-700 via-indigo-700 to-slate-900 p-6 text-white text-center relative">
                            <button 
                                onClick={() => setShowLoginModal(false)}
                                className="absolute top-4 left-4 bg-white/10 hover:bg-white/20 w-8 h-8 rounded-full flex items-center justify-center text-white font-bold transition"
                            >
                                ✕
                            </button>
                            <div className="text-4xl mb-2">🔐</div>
                            <h2 className="text-2xl font-black">تسجيل الدخول للنظام</h2>
                            <p className="text-xs text-blue-200 mt-1">يتعرف النظام آلياً على صفة المستخدم فور إدخال كلمة المرور الخاص به</p>
                        </div>

                        <form onSubmit={handleLogin} className="p-6 space-y-4">
                            <div className="space-y-1.5">
                                <label className="block text-xs font-black text-slate-700">🔑 أدخل كلمة المرور الخاصة بك:</label>
                                <input
                                    type="password"
                                    autoFocus
                                    placeholder="••••"
                                    value={loginInputPin}
                                    onChange={(e) => setLoginInputPin(e.target.value)}
                                    className="w-full bg-slate-50 border-2 border-slate-300 rounded-xl px-4 py-3 text-center text-xl font-mono font-bold text-indigo-900 outline-none focus:border-indigo-600 transition shadow-inner"
                                />
                            </div>

                            {loginError && (
                                <div className="p-2.5 bg-red-50 border border-red-200 text-red-700 text-xs font-bold rounded-xl text-center">
                                    {loginError}
                                </div>
                            )}

                            <button
                                type="submit"
                                className="w-full py-3.5 bg-gradient-to-r from-green-600 via-emerald-600 to-teal-700 hover:from-green-700 hover:to-teal-800 text-white font-bold rounded-xl text-sm shadow-lg transition transform active:scale-95 flex items-center justify-center gap-2"
                            >
                                <span>🔓</span>
                                <span>دخول للنظام</span>
                            </button>

                            <div className="text-center pt-2">
                                <button
                                    type="button"
                                    onClick={() => {
                                        setCurrentUserRole('viewer');
                                        localStorage.setItem('currentUserRole', 'viewer');
                                        setShowWelcome(false);
                                        setShowLoginModal(false);
                                    }}
                                    className="text-xs font-bold text-slate-500 hover:text-indigo-600 hover:underline transition"
                                >
                                    👁️ استمرار كـ (مستعرض فقط) دون كلمة سر
                                </button>
                            </div>
                        </form>
                    </div>
                </div>
            )}"""

    if old_login_modal in code:
        code = code.replace(old_login_modal, new_login_modal)
        print(f"✓ Replaced Login Modal with Single Smart PIN Input in {file_path}")

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(code)
    return True

if __name__ == '__main__':
    update_file('e:/Antigravity projects/HR Admin/index.html')
    update_file('e:/Antigravity projects/HR Admin/نظام_ادراة_الملاك_v6.9_online.html')
    update_file('e:/Antigravity projects/HR Admin/نظام_ادراة_الملاك_v6.9.html')
