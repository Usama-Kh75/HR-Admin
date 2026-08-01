import os
import re

def update_file(file_path):
    if not os.path.exists(file_path):
        print(f"File not found: {file_path}")
        return False

    with open(file_path, 'r', encoding='utf-8') as f:
        code = f.read()

    # 1. Inject RBAC States and handlers
    rbac_states_code = """
            // ===== نظام إدارة الصلاحيات وكلمات المرور (RBAC System) =====
            const [passwordsConfig, setPasswordsConfig] = useState(() => {
                const saved = localStorage.getItem('passwordsConfig');
                return saved ? JSON.parse(saved) : { admin: '1975', operator: '2026', viewer: '1234' };
            });
            React.useEffect(() => {
                localStorage.setItem('passwordsConfig', JSON.stringify(passwordsConfig));
            }, [passwordsConfig]);

            const [currentUserRole, setCurrentUserRole] = useState(() => {
                return localStorage.getItem('currentUserRole') || null;
            });

            const [showChangePasswordModal, setShowChangePasswordModal] = useState(false);
            const [loginInputRole, setLoginInputRole] = useState('operator');
            const [loginInputPin, setLoginInputPin] = useState('');
            const [loginError, setLoginError] = useState('');

            const [newAdminPin, setNewAdminPin] = useState('');
            const [newOperatorPin, setNewOperatorPin] = useState('');
            const [newViewerPin, setNewViewerPin] = useState('');

            const handleLogin = (e) => {
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
            };

            const handleLogout = () => {
                setCurrentUserRole(null);
                localStorage.removeItem('currentUserRole');
            };

            const handleSaveNewPasswords = (e) => {
                if (e) e.preventDefault();
                const updated = {
                    admin: newAdminPin.trim() || passwordsConfig.admin,
                    operator: newOperatorPin.trim() || passwordsConfig.operator,
                    viewer: newViewerPin.trim() || passwordsConfig.viewer
                };
                setPasswordsConfig(updated);
                localStorage.setItem('passwordsConfig', JSON.stringify(updated));
                alert('✅ تم تحديث وتأمين كلمات المرور بنجاح!');
                setShowChangePasswordModal(false);
                setNewAdminPin('');
                setNewOperatorPin('');
                setNewViewerPin('');
            };

            const isViewer = currentUserRole === 'viewer';
    """

    state_anchor = "const [passwordsConfig, setPasswordsConfig]"
    if state_anchor not in code:
        code = code.replace("const [syncStatus, setSyncStatus] = useState({", rbac_states_code + "\n            const [syncStatus, setSyncStatus] = useState({")
        print(f"✓ Injected RBAC states into {file_path}")

    # 2. Update deleteEmployee pin validation to use passwordsConfig.admin
    code = code.replace("if (adminPin !== '1975') {", "if (adminPin !== passwordsConfig.admin) {")

    # 3. Inject Role Badges & Logout Button into Header
    header_badge_target = """                                <span className="text-xs font-bold">
                                    {syncStatus.connected ? `🟢 السيرفر المحلي نشط (${syncStatus.ip || 'Local'})` : '🟡 أوفلاين محلي'}
                                </span>
                            </div>"""

    new_header_controls = """                                <span className="text-xs font-bold">
                                    {syncStatus.connected ? `🟢 السيرفر المحلي نشط (${syncStatus.ip || 'Local'})` : '🟡 أوفلاين محلي'}
                                </span>
                            </div>

                            {/* شريط التحكم بالصفة وكلمات المرور */}
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

    if header_badge_target in code and "شريط التحكم بالصفة" not in code:
        code = code.replace(header_badge_target, new_header_controls)
        print(f"✓ Injected header role controls into {file_path}")

    # 4. Inject Login Modal & Change Password Modal
    modals_code = """
            {/* نافذة تسجيل الدخول للنظام (Login Modal) */}
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
            )}

            {/* نافذة تغيير كلمات المرور (Change Passwords Modal) */}
            {showChangePasswordModal && (
                <div className="fixed inset-0 bg-slate-950/70 backdrop-blur-sm z-50 flex items-center justify-center p-4">
                    <div className="bg-white rounded-3xl shadow-2xl border border-slate-100 max-w-md w-full overflow-hidden animate-fadeInUp">
                        <div className="bg-gradient-to-r from-amber-600 to-orange-700 p-5 text-white relative flex justify-between items-center">
                            <div className="flex items-center gap-2">
                                <span className="text-2xl">🔑</span>
                                <div>
                                    <h3 className="text-lg font-black">إدارة كلمات المرور بالنظام</h3>
                                    <p className="text-xs text-amber-100">خاص بمدير النظام (م. أسامة خليل)</p>
                                </div>
                            </div>
                            <button
                                onClick={() => setShowChangePasswordModal(false)}
                                className="w-8 h-8 rounded-full bg-white/10 hover:bg-white/20 flex items-center justify-center text-white font-bold transition"
                            >
                                ✕
                            </button>
                        </div>

                        <form onSubmit={handleSaveNewPasswords} className="p-6 space-y-4">
                            <div className="space-y-1">
                                <label className="block text-xs font-bold text-slate-700">👑 كلمة سر مدير النظام (الماستر الحالية: {passwordsConfig.admin}):</label>
                                <input
                                    type="text"
                                    placeholder={passwordsConfig.admin}
                                    value={newAdminPin}
                                    onChange={(e) => setNewAdminPin(e.target.value)}
                                    className="w-full bg-slate-50 border border-slate-300 rounded-xl px-3 py-2 text-xs font-mono font-bold text-slate-800 outline-none focus:border-amber-500"
                                />
                            </div>

                            <div className="space-y-1">
                                <label className="block text-xs font-bold text-slate-700">✍️ كلمة سر الإداريين ومُدخلي البيانات (الحالية: {passwordsConfig.operator}):</label>
                                <input
                                    type="text"
                                    placeholder={passwordsConfig.operator}
                                    value={newOperatorPin}
                                    onChange={(e) => setNewOperatorPin(e.target.value)}
                                    className="w-full bg-slate-50 border border-slate-300 rounded-xl px-3 py-2 text-xs font-mono font-bold text-slate-800 outline-none focus:border-amber-500"
                                />
                            </div>

                            <div className="space-y-1">
                                <label className="block text-xs font-bold text-slate-700">👁️ كلمة سر المستعرضين (الحالية: {passwordsConfig.viewer}):</label>
                                <input
                                    type="text"
                                    placeholder={passwordsConfig.viewer}
                                    value={newViewerPin}
                                    onChange={(e) => setNewViewerPin(e.target.value)}
                                    className="w-full bg-slate-50 border border-slate-300 rounded-xl px-3 py-2 text-xs font-mono font-bold text-slate-800 outline-none focus:border-amber-500"
                                />
                            </div>

                            <div className="flex justify-end gap-2 pt-2">
                                <button
                                    type="button"
                                    onClick={() => setShowChangePasswordModal(false)}
                                    className="px-4 py-2 bg-slate-100 hover:bg-slate-200 text-slate-700 font-bold rounded-xl text-xs transition"
                                >
                                    إلغاء
                                </button>
                                <button
                                    type="submit"
                                    className="px-5 py-2 bg-amber-600 hover:bg-amber-700 text-white font-bold rounded-xl text-xs shadow transition"
                                >
                                    💾 حفظ كلمات المرور الجديدة
                                </button>
                            </div>
                        </form>
                    </div>
                </div>
            )}"""

    modal_target = "{/* تنبيه النسخ الاحتياطي التلقائي */}"
    if modal_target in code and "نافذة تسجيل الدخول للنظام" not in code:
        code = code.replace(modal_target, modals_code + "\n\n                                " + modal_target)
        print(f"✓ Injected RBAC & Passwords Modals into {file_path}")

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(code)
    return True

if __name__ == '__main__':
    update_file('e:/Antigravity projects/HR Admin/index.html')
    update_file('e:/Antigravity projects/HR Admin/نظام_ادراة_الملاك_v6.9_online.html')
    update_file('e:/Antigravity projects/HR Admin/نظام_ادراة_الملاك_v6.9.html')
