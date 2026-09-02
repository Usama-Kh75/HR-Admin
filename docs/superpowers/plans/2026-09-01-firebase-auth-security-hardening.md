# Firebase Auth Security Hardening Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Remove the client-exposed PIN system and open Firebase write access from the HR Admin system, replacing them with real Firebase Authentication, server-enforced write rules, and an audit log — without changing the app's existing open-read philosophy.

**Architecture:** Add a small set of REST-based Firebase Auth helper functions (no SDK) to `index.html`, wire them into the existing login flow and every Firebase write call site via a single `cloudFetch` wrapper that attaches the current ID token, then mirror the same edits into `نظام_ادارة_الملاك_v8.5_cloud.html`. The offline file gets a narrower fix: replace the shared hardcoded `'1975'` PIN with a locally-generated PIN that never leaves the browser.

**Tech Stack:** Vanilla JS + React (in-browser Babel, no build step), Firebase Realtime Database REST API, Firebase Identity Toolkit REST API (Email/Password auth).

**Spec:** `docs/superpowers/specs/2026-09-01-firebase-auth-security-hardening-design.md`

## Global Constraints

- No new npm packages, build step, or SDK — stay consistent with the existing plain-`fetch()` REST style used throughout the file.
- `system_bundle` read stays open (`.read: true`) — do not gate reads behind auth.
- Every write to `system_bundle`, `backups_history`, or `active_sessions` must carry the caller's current Firebase ID token.
- `نظام_ادارة_الملاك_v8.5_offline.html` must never call any Firebase URL and must remain fully isolated (existing invariant #7 in `HR_Admin_Handoff.md`).
- No automated test suite exists in this project — every task's verification is manual (browser + curl), matching the project's existing practice.

There is no test runner in this repository. Wherever the task-template below says "write the failing test," substitute the manual verification step given in that task (grep confirmation, browser console check, or curl call) — do the same verification before and after the change to confirm it moved from failing to passing.

---

## Task 1: Add Firebase Auth REST helpers to `index.html`

**Files:**
- Modify: `index.html` (near existing constants at line ~1020)

**Interfaces:**
- Produces: `FIREBASE_WEB_API_KEY` (const, placeholder string), `FIREBASE_ROLES_URL`, `FIREBASE_AUDIT_LOG_URL` (consts), `getStoredAuth()`, `setStoredAuth(session|null)`, `signInWithEmail(email, password)` (returns `{idToken, refreshToken, uid, expiresAt}`, throws on failure), `refreshIdTokenIfNeeded()` (returns session or `null`), `signOutFirebase()`, `cloudFetch(url, options)` (returns a `fetch` Promise with `auth=<idToken>` appended when a session exists), `logAuditEvent(action)`.

- [x] **Step 1: Confirm current state**

Run: `grep -n "FIREBASE_SESSIONS_URL = " "index.html"`
Expected output: one line, `const FIREBASE_SESSIONS_URL = "https://hr-cooling-default-rtdb.firebaseio.com/active_sessions";` — this is the anchor line for the next edit.

- [x] **Step 2: Add the new constants and helper functions**

Insert immediately after the `FIREBASE_SESSIONS_URL` line (index.html:1022):

```js
            const FIREBASE_ROLES_URL = "https://hr-cooling-default-rtdb.firebaseio.com/roles";
            const FIREBASE_AUDIT_LOG_URL = "https://hr-cooling-default-rtdb.firebaseio.com/audit_log";
            const FIREBASE_WEB_API_KEY = "REPLACE_WITH_FIREBASE_WEB_API_KEY";
            const FIREBASE_AUTH_BASE = "https://identitytoolkit.googleapis.com/v1";
            const FIREBASE_TOKEN_URL = "https://securetoken.googleapis.com/v1/token";

            const getStoredAuth = () => {
                try {
                    const raw = safeStorage.getItem('firebaseAuthSession');
                    return raw ? JSON.parse(raw) : null;
                } catch (e) { return null; }
            };

            const setStoredAuth = (session) => {
                if (session) {
                    safeStorage.setItem('firebaseAuthSession', JSON.stringify(session));
                } else {
                    safeStorage.removeItem('firebaseAuthSession');
                }
            };

            const signInWithEmail = async (email, password) => {
                const res = await fetch(`${FIREBASE_AUTH_BASE}/accounts:signInWithPassword?key=${FIREBASE_WEB_API_KEY}`, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ email, password, returnSecureToken: true })
                });
                const data = await res.json();
                if (!res.ok) {
                    const msg = (data.error && data.error.message) || 'AUTH_FAILED';
                    throw new Error(msg);
                }
                const session = {
                    idToken: data.idToken,
                    refreshToken: data.refreshToken,
                    uid: data.localId,
                    expiresAt: Date.now() + (parseInt(data.expiresIn, 10) * 1000)
                };
                setStoredAuth(session);
                return session;
            };

            const refreshIdTokenIfNeeded = async () => {
                const session = getStoredAuth();
                if (!session) return null;
                if (Date.now() < session.expiresAt - 5 * 60 * 1000) {
                    return session;
                }
                try {
                    const res = await fetch(`${FIREBASE_TOKEN_URL}?key=${FIREBASE_WEB_API_KEY}`, {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
                        body: `grant_type=refresh_token&refresh_token=${session.refreshToken}`
                    });
                    const data = await res.json();
                    if (!res.ok) {
                        setStoredAuth(null);
                        return null;
                    }
                    const refreshed = {
                        idToken: data.id_token,
                        refreshToken: data.refresh_token,
                        uid: data.user_id,
                        expiresAt: Date.now() + (parseInt(data.expires_in, 10) * 1000)
                    };
                    setStoredAuth(refreshed);
                    return refreshed;
                } catch (e) {
                    return session;
                }
            };

            const signOutFirebase = () => {
                setStoredAuth(null);
            };

            const cloudFetch = async (url, options = {}) => {
                const session = await refreshIdTokenIfNeeded();
                const separator = url.includes('?') ? '&' : '?';
                const authedUrl = session ? `${url}${separator}auth=${session.idToken}` : url;
                return fetch(authedUrl, options);
            };

            const logAuditEvent = async (action, displayName) => {
                try {
                    const session = getStoredAuth();
                    if (!session) return;
                    await cloudFetch(`${FIREBASE_AUDIT_LOG_URL}.json`, {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify({
                            uid: session.uid,
                            displayName: displayName || '',
                            action,
                            timestamp: new Date().toISOString()
                        })
                    });
                } catch (e) {}
            };
```

- [x] **Step 3: Verify it loads without errors**

Open `index.html` directly in a browser (double-click or `start index.html` on Windows). Open DevTools Console. Confirm there are no red syntax errors on load (the app should render the normal welcome/login screen). This confirms the new code parses correctly under Babel's in-browser JSX/JS transform.

- [x] **Step 4: Commit**

```bash
git add index.html
git commit -m "Add Firebase Auth REST helpers (signIn, token refresh, cloudFetch, audit log)"
```

---

## Task 2: Replace PIN login with email/password Firebase Auth login

**Files:**
- Modify: `index.html:1036-1136` (login state + `handleLogin`), `index.html:5769-5820` (login modal JSX)

**Interfaces:**
- Consumes: `signInWithEmail`, `cloudFetch`, `FIREBASE_ROLES_URL` from Task 1.
- Produces: `loginEmail`/`setLoginEmail`, `loginPassword`/`setLoginPassword` state (replacing `loginInputPin`); `handleLogin` now authenticates via Firebase and reads the user's role from `roles/{uid}`.

- [x] **Step 1: Confirm current state**

Run: `grep -n "loginInputPin" "index.html"`
Expected: matches at the state declaration (~1036), inside `handleLogin` (~1042, 1070), and in the JSX input (~5791). These are all the sites this task touches.

- [x] **Step 2: Replace login state**

Find (index.html:1036-1037):
```js
            const [loginInputPin, setLoginInputPin] = useState('');
            const [loginError, setLoginError] = useState('');
```
Replace with:
```js
            const [loginEmail, setLoginEmail] = useState('');
            const [loginPassword, setLoginPassword] = useState('');
            const [loginError, setLoginError] = useState('');
```

- [x] **Step 3: Rewrite `handleLogin`**

Replace the entire `handleLogin` function body (index.html:1039-1136) with:

```js
            const handleLogin = async (e) => {
                if (e) e.preventDefault();
                setLoginError('');
                const email = loginEmail.trim();
                const password = loginPassword;
                if (!email || !password) return;

                setIsCheckingLogin(true);

                let session;
                try {
                    session = await signInWithEmail(email, password);
                } catch (err) {
                    setIsCheckingLogin(false);
                    setLoginError('❌ البريد الإلكتروني أو كلمة المرور غير صحيحة!');
                    return;
                }

                let roleData = null;
                try {
                    const roleRes = await cloudFetch(`${FIREBASE_ROLES_URL}/${session.uid}.json`);
                    if (roleRes.ok) {
                        roleData = await roleRes.json();
                    }
                } catch (err) {
                    console.warn("Role fetch error during login:", err);
                }

                if (!roleData || !roleData.role) {
                    setIsCheckingLogin(false);
                    signOutFirebase();
                    setLoginError('❌ هذا الحساب غير مخوّل للدخول (لا يوجد دور مسند له). راجع مدير النظام.');
                    return;
                }

                const targetUser = { id: session.uid, name: roleData.name || email, role: roleData.role, permissions: roleData.permissions || {} };

                // فحص هل الحساب مستخدم حالياً من جهاز آخر (قفل الجلسة الفردية لمنع التزامن)
                try {
                    const sessRes = await fetch(`${FIREBASE_SESSIONS_URL}/${targetUser.id}.json?t=${Date.now()}`);
                    if (sessRes.ok) {
                        const sessData = await sessRes.json();
                        if (sessData && sessData.sessionId && sessData.lastSeen) {
                            const elapsed = Date.now() - sessData.lastSeen;
                            if (elapsed < 15000 && sessData.sessionId !== currentSessionIdRef.current) {
                                setIsCheckingLogin(false);
                                signOutFirebase();
                                setLoginError(`⛔ هذا الحساب (${targetUser.name}) قيد الاستخدام حالياً من جهاز آخر!\nلا يمكن لشخصين تسجيل الدخول بنفس الحساب في آن واحد.\n(يرجى تسجيل الخروج من الجهاز الآخر أولاً، أو الانتظار 15 ثانية في حال إغلاق المتصفح).`);
                                return;
                            }
                        }
                    }
                } catch (err) {
                    console.warn("Session check error:", err);
                }

                // حجز الجلسة الفردية للجهاز الحالي
                const newSessionId = 'sess_' + Date.now() + '_' + Math.random().toString(36).substr(2, 7);
                currentSessionIdRef.current = newSessionId;
                currentUserIdRef.current = targetUser.id;

                try {
                    await cloudFetch(`${FIREBASE_SESSIONS_URL}/${targetUser.id}.json`, {
                        method: 'PUT',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify({
                            sessionId: newSessionId,
                            userId: targetUser.id,
                            name: targetUser.name,
                            role: targetUser.role,
                            lastSeen: Date.now()
                        })
                    });
                } catch (e) {}

                setCurrentUserRole(targetUser.role);
                setCurrentUserName(targetUser.name);
                setCurrentUserPermissions(targetUser.permissions);
                if (targetUser.role === 'operator' || targetUser.role === 'admin') {
                    setDataEntryOperator(targetUser.name.split('(')[0].trim());
                }
                logAuditEvent('login', targetUser.name);
                setIsCheckingLogin(false);
                setShowWelcome(false);
                setLoginEmail('');
                setLoginPassword('');
                setShowLoginModal(false);
            };

            const handleLogout = () => {
                if (currentUserIdRef.current) {
                    const uid = currentUserIdRef.current;
                    cloudFetch(`${FIREBASE_SESSIONS_URL}/${uid}.json`, { method: 'DELETE' }).catch(() => {});
                }
                signOutFirebase();
                currentUserIdRef.current = null;
                currentSessionIdRef.current = null;
                setCurrentUserRole(null);
                setCurrentUserName('');
                setCurrentUserPermissions({});
            };
```

Note: this introduces `currentUserPermissions` state — add it in Task 4 alongside the RBAC changes (declare it now as a plain `useState({})` next to `currentUserRole` so Task 2's code compiles standalone):

Find (index.html, the `currentUserRole` declaration, originally at line 998):
```js
            const [currentUserRole, setCurrentUserRole] = useState(null);
```
Replace with:
```js
            const [currentUserRole, setCurrentUserRole] = useState(null);
            const [currentUserPermissions, setCurrentUserPermissions] = useState({});
```

- [x] **Step 4: Update the heartbeat effect to use `cloudFetch` for writes**

Find (index.html, inside the heartbeat `useEffect`, originally ~1168):
```js
                        await fetch(`${FIREBASE_SESSIONS_URL}/${uid}.json`, {
                            method: 'PUT',
                            headers: { 'Content-Type': 'application/json' },
                            body: JSON.stringify({
                                sessionId: sid,
                                userId: uid,
                                name: currentUserName,
                                role: currentUserRole,
                                lastSeen: Date.now()
                            })
                        });
```
Replace `await fetch(` with `await cloudFetch(` (same arguments) — the read call one line above it (`checkRes = await fetch(...)`) stays a plain `fetch` since reads remain open.

- [x] **Step 5: Update the login modal JSX**

Replace the password input block (index.html:5785-5795):
```jsx
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
```
with:
```jsx
                            <div className="space-y-1.5">
                                <label className="block text-xs font-black text-slate-700">📧 البريد الإلكتروني:</label>
                                <input
                                    type="email"
                                    autoFocus
                                    placeholder="name@example.com"
                                    value={loginEmail}
                                    onChange={(e) => setLoginEmail(e.target.value)}
                                    className="w-full bg-slate-50 border-2 border-slate-300 rounded-xl px-4 py-3 text-center font-bold text-indigo-900 outline-none focus:border-indigo-600 transition shadow-inner"
                                />
                            </div>
                            <div className="space-y-1.5">
                                <label className="block text-xs font-black text-slate-700">🔑 كلمة المرور:</label>
                                <input
                                    type="password"
                                    placeholder="••••••••"
                                    value={loginPassword}
                                    onChange={(e) => setLoginPassword(e.target.value)}
                                    className="w-full bg-slate-50 border-2 border-slate-300 rounded-xl px-4 py-3 text-center font-bold text-indigo-900 outline-none focus:border-indigo-600 transition shadow-inner"
                                />
                            </div>
```

- [x] **Step 6: Verify the login form renders**

Open `index.html` in a browser, click through to the login modal. Confirm it shows email + password fields (not the old single PIN field) and that typing and submitting with a bogus email/password shows the `❌` error message without a JS console error.

- [x] **Step 7: Commit**

```bash
git add index.html
git commit -m "Replace PIN login with Firebase email/password authentication"
```

---

## Task 3: Remove the hardcoded admin PIN and PIN-gated admin checks

**Files:**
- Modify: `index.html` at lines ~970, ~977-998, ~1582, ~4207, ~4413, ~5301, ~8749 (all `isAdminPin` / `'1975'` sites — re-check line numbers with grep first, since Tasks 1-2 shifted them)

**Interfaces:**
- Consumes: `currentUserRole`, `currentUserPermissions` (from Task 2).
- Produces: `isAdminPin` and all literal `'1975'` checks removed; admin-only actions now gate on `currentUserRole === 'admin'` directly (the user is already authenticated by Firebase at this point, so no secondary PIN re-entry is needed).

- [x] **Step 1: Find every remaining site**

Run: `grep -n "isAdminPin\|'1975'" "index.html"`
This must be the authoritative list for this task — line numbers below are illustrative, not to be trusted after Tasks 1-2 shift the file.

- [x] **Step 2: Remove the `isAdminPin` definition**

Delete this block entirely (originally index.html:977-982):
```js
            const isAdminPin = (pin) => {
                const p = String(pin || '').trim();
                const matchedUser = systemUsers.find(u => u.active !== false && String(u.pin).trim() === p && u.role === 'admin');
                return !!matchedUser || p === '1975';
            };
```

- [x] **Step 3: Simplify `handleOpenUserManagement`**

Find (originally index.html:988-1002-ish, the function guarding the user-management modal):
```js
            const handleOpenUserManagement = () => {
                if (currentUserRole === 'admin') {
                    setShowUserManagementModal(true);
                } else {
                    const pin = prompt('🔐 فتح إدارة الحسابات والصلاحيات:\n\nيرجى إدخال كلمة المرور (PIN) الخاصة بمدير النظام:');
                    if (isAdminPin(pin)) {
                        setCurrentUserRole('admin');
                        const adminUser = systemUsers.find(u => u.role === 'admin') || { name: 'أسامة خليل (مدير النظام)' };
                        setCurrentUserName(adminUser.name);
                        setShowUserManagementModal(true);
                    } else if (pin !== null) {
                        alert('❌ كلمة المرور غير صحيحة!');
                    }
                }
            };
```
Replace with:
```js
            const handleOpenUserManagement = () => {
                if (currentUserRole === 'admin') {
                    setShowUserManagementModal(true);
                } else {
                    alert('❌ هذه النافذة متاحة فقط لمن سجّل دخوله كمدير للنظام.');
                }
            };
```
This is safe because the user's role now comes from the server-verified `roles/{uid}` node set at login (Task 2) — there is no longer a client-editable PIN to re-check, so a second local prompt would only be theater.

- [x] **Step 4: Replace every other `isAdminPin(adminPin)` guard**

For each remaining call site found in Step 1 (originally ~1582, ~4207, ~4413, ~8749), these guard a destructive/admin action behind a `prompt()`-collected `adminPin` variable. Replace the pattern:
```js
                if (!isAdminPin(adminPin)) {
```
with:
```js
                if (currentUserRole !== 'admin') {
```
and remove the now-unused `const adminPin = prompt(...)` line directly above each of those `if` statements (search one line up from each match — the prompt text is no longer needed since the check no longer consumes its value).

- [x] **Step 5: Verify no references remain**

Run: `grep -n "isAdminPin\|'1975'" "index.html"`
Expected: no output (0 matches).

- [x] **Step 6: Manual smoke test**

Open `index.html` in a browser. Confirm the app still loads and the login modal still opens/closes without a console error (full login can't be tested yet — Firebase console setup and Task 6 are still pending).

- [x] **Step 7: Commit**

```bash
git add index.html
git commit -m "Remove hardcoded admin PIN and PIN-based admin re-checks"
```

---

## Task 4: Attach auth tokens to remaining Firebase writes and add audit logging

**Files:**
- Modify: `index.html` — `pushDataToCloud` (~1456-1526), the backups snapshot `fetch` inside it, and the two `handleThreeShiftAnchorChange`/`handleTwoShiftAnchorChange` `pushDataToCloud` call sites already shown in the working tree's uncommitted diff.

**Interfaces:**
- Consumes: `cloudFetch`, `logAuditEvent` (Task 1).
- Produces: no new interfaces — closes the last write call sites that were still using plain `fetch`.

- [x] **Step 1: Confirm remaining plain-`fetch` writes**

Run: `grep -n "fetch(FIREBASE_DB_URL\|fetch(\`\${FIREBASE_BACKUPS_URL}" "index.html"`
Expected: the `PUT` to `FIREBASE_DB_URL` inside `pushDataToCloud`, and the `PUT` to `FIREBASE_BACKUPS_URL/${todayKey}.json` inside the same function (GET calls to these URLs elsewhere are reads and stay as plain `fetch`).

- [x] **Step 2: Switch both writes to `cloudFetch`**

In `pushDataToCloud` (index.html:1486 and 1506 in the original numbering), change:
```js
                    const res = await fetch(FIREBASE_DB_URL, {
```
to:
```js
                    const res = await cloudFetch(FIREBASE_DB_URL, {
```
and:
```js
                        fetch(`${FIREBASE_BACKUPS_URL}/${todayKey}.json`, {
```
to:
```js
                        cloudFetch(`${FIREBASE_BACKUPS_URL}/${todayKey}.json`, {
```

- [x] **Step 3: Log an audit event on every successful save**

Immediately after the line `setCloudSyncStatus({ connected: true, syncing: false, lastSync: new Date().toLocaleTimeString('ar-IQ') });` inside `pushDataToCloud`, add:
```js
                        logAuditEvent('save_system_bundle', currentUserName);
```

- [x] **Step 4: Verify no plain-`fetch` writes remain to protected paths**

Run: `grep -n "fetch(FIREBASE_DB_URL, {\|fetch(\`\${FIREBASE_BACKUPS_URL}" "index.html"`
Expected: 0 matches for the write forms (the read forms — with `?t=` and no `method:`, or explicit `method: 'GET'` — are unaffected and should still be plain `fetch`).

- [x] **Step 5: Manual verification**

Open `index.html`, open DevTools → Network tab, trigger any save action (e.g. change the daily report date). Confirm the outgoing request URL to `system_bundle.json` now includes `?auth=...` (it will be the literal string `undefined` until Firebase is fully configured in Task 6 — that's expected at this point; the goal here is confirming the query param is present, not that it's a valid token yet).

- [x] **Step 6: Commit**

```bash
git add index.html
git commit -m "Route remaining Firebase writes through cloudFetch and add save audit logging"
```

---

## Task 5: Rework the User Management modal to assign roles, not PINs

**Files:**
- Modify: `index.html` — the User Management modal JSX and its save/delete/toggle handlers (originally around lines 1245-1400 for handlers, ~5850+ for the modal JSX; re-locate with grep since line numbers shifted).

**Interfaces:**
- Consumes: `FIREBASE_ROLES_URL`, `cloudFetch` (Task 1).
- Produces: the modal now edits `{name, role, permissions}` for a Firebase Auth `uid` the admin pastes in (copied from Firebase Console per the deployment steps), instead of generating a `pin`.

- [x] **Step 1: Locate the current handlers**

Run: `grep -n "existingWithPin\|newUser = {\|updatedUsers = systemUsers.map" "index.html"`
This finds the add/edit-user save handler that currently validates and stores a `pin` field.

- [x] **Step 2: Remove PIN validation and generation from the save handler**

Find the block that checks for PIN collisions:
```js
                const existingWithPin = systemUsers.find(u => String(u.pin).trim() === pin && u.id !== editingUserId);
```
and the surrounding logic that builds `newUser`/`updatedUsers` with a `pin` field. Replace the user object shape so it no longer includes `pin`, and instead requires a `uid` field (text input, admin pastes the Firebase Auth UID from the console) plus `name`, `role`, `permissions` — the same shape already used elsewhere in the file for `permissions` (`{ dailyReport, staffMaster, safety, evaluation }`).

- [x] **Step 3: Write role changes to `roles/{uid}` in Firebase, not just local state**

After `updatedUsers` is computed and saved to `safeStorage`/`systemUsers` state (existing behavior), add a call so the change actually takes effect for that person's next login:
```js
                cloudFetch(`${FIREBASE_ROLES_URL}/${targetUid}.json`, {
                    method: 'PUT',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ name, role: userFormRole, permissions: permsToSave })
                }).catch(() => {});
                logAuditEvent(`update_role:${targetUid}`, currentUserName);
```
(`targetUid` is the `uid` field entered in Step 2; `name`, `userFormRole`, `permsToSave` are the same local variables the existing handler already computes.)

- [x] **Step 4: Update the modal form JSX**

In the add/edit user form, replace the PIN input field (a 4-digit numeric input) with a text input labeled "🆔 معرّف حساب Firebase (UID)" bound to the new `uid` field — the admin copies this from Firebase Console → Authentication → Users after creating the account there (per the deployment steps already shared).

- [x] **Step 5: Verify the modal still opens and saves**

Open `index.html`, log in is not yet fully testable (Task 6 pending), but confirm via DevTools Console that no reference to `pin` remains unresolved: `grep -n "\.pin\b" "index.html"` should return no matches other than incidental unrelated words (double-check any hit manually).

- [x] **Step 6: Commit**

```bash
git add index.html
git commit -m "Rework user management to assign Firebase roles instead of generating PINs"
```

---

## Task 6: Mirror all changes into the cloud standalone file and verify parity

**Files:**
- Modify: `نظام_ادارة_الملاك_v8.5_cloud.html` (apply the same edits as Tasks 1-5)

- [x] **Step 1: Diff against `index.html` before starting**

Run: `diff "index.html" "نظام_ادارة_الملاك_v8.5_cloud.html"`
Per `HR_Admin_Handoff.md` section 2, this file is documented as "متطابقة مع index.html" (identical to index.html). Confirm the diff shows only the changes from Tasks 1-5 still missing (i.e., this file is currently identical to what `index.html` looked like *before* this plan started) — if there are unrelated differences, stop and flag them instead of overwriting.

- [x] **Step 2: Apply the same edits**

Repeat Tasks 1-5's exact edits (same old/new code blocks) against this file.

- [x] **Step 3: Verify parity**

Run: `diff "index.html" "نظام_ادارة_الملاك_v8.5_cloud.html"`
Expected: no output (the two files are byte-identical again, now both with the security hardening applied).

- [x] **Step 4: Commit**

```bash
git add "نظام_ادارة_الملاك_v8.5_cloud.html"
git commit -m "Mirror Firebase Auth security hardening into the cloud standalone file"
```

---

## Task 7: Replace the shared offline PIN with a locally-generated one

**Files:**
- Modify: `نظام_ادارة_الملاك_v8.5_offline.html`

This file must stay fully isolated from Firebase (Global Constraints), so it does not get the Auth changes above. But it likely still contains the same hardcoded `'1975'` string, which is a real (if lower-severity) problem: anyone who reads the publicly-hosted `index.html` source learns the same PIN and can try it against any deployment of the offline file too, since the secret is shared across every install rather than being specific to one machine.

- [x] **Step 1: Confirm the offline file's current PIN handling**

Run: `grep -n "isAdminPin\|'1975'" "نظام_ادارة_الملاك_v8.5_offline.html"`
Note the matching lines — expect a structure similar to `index.html`'s original `isAdminPin`.

- [x] **Step 2: Generate a local-only PIN on first run instead of hardcoding one**

Replace the `isAdminPin` function in this file with a version that checks against a PIN stored only in this browser's local storage, generating one on first use:
```js
            const isAdminPin = (pin) => {
                const p = String(pin || '').trim();
                const matchedUser = systemUsers.find(u => u.active !== false && String(u.pin).trim() === p && u.role === 'admin');
                if (matchedUser) return true;
                let localAdminPin = safeStorage.getItem('localOfflineAdminPin');
                if (!localAdminPin) {
                    localAdminPin = String(Math.floor(1000 + Math.random() * 9000));
                    safeStorage.setItem('localOfflineAdminPin', localAdminPin);
                    alert(`🔐 تم إنشاء رمز مدير محلي جديد لهذا الجهاز لأول مرة:\n\n${localAdminPin}\n\nاحتفظ به في مكان آمن — لن يظهر مرة أخرى تلقائياً.`);
                }
                return p === localAdminPin;
            };
```

- [x] **Step 3: Verify the old shared literal is gone**

Run: `grep -n "'1975'" "نظام_ادارة_الملاك_v8.5_offline.html"`
Expected: no output.

- [x] **Step 4: Manual verification**

Open `نظام_ادارة_الملاك_v8.5_offline.html` directly (double-click, `file://`). Trigger an admin-gated action for the first time — confirm the alert box shows a freshly generated 4-digit PIN, and that entering it succeeds. Reload the page and confirm the *same* PIN (now persisted in that browser's local storage) still works, and a wrong PIN is still rejected.

- [x] **Step 5: Commit**

```bash
git add "نظام_ادارة_الملاك_v8.5_offline.html"
git commit -m "Replace shared hardcoded offline admin PIN with a per-machine generated one"
```

---

## Task 8: Wire in the real Firebase Web API Key and roles, then end-to-end verify

**Files:**
- Modify: `index.html`, `نظام_ادارة_الملاك_v8.5_cloud.html` (the `FIREBASE_WEB_API_KEY` placeholder from Task 1)

This task requires the user to have already completed the manual Firebase Console steps (enable Email/Password auth, create accounts, set `roles/{uid}`, publish the new Security Rules) and provided: the Web API Key, and each account's `uid`/name/role/permissions.

- [ ] **Step 1: Replace the placeholder key in both files**

In both `index.html` and `نظام_ادارة_الملاك_v8.5_cloud.html`, replace:
```js
            const FIREBASE_WEB_API_KEY = "REPLACE_WITH_FIREBASE_WEB_API_KEY";
```
with the real key the user provided, e.g.:
```js
            const FIREBASE_WEB_API_KEY = "AIza...";
```

- [ ] **Step 2: Confirm the rules are live (read-only check, no write needed)**

Run: `curl -s -o /dev/null -w "%{http_code}" "https://hr-cooling-default-rtdb.firebaseio.com/system_bundle.json"`
Expected: `200` (read stays open, per design).

- [ ] **Step 3: Confirm unauthenticated writes are now rejected**

Run: `curl -s -X PUT -d "{\"test\":true}" "https://hr-cooling-default-rtdb.firebaseio.com/system_bundle/__probe.json"`
Expected: a JSON body containing `"error"` (Firebase returns `403`/permission-denied style error) — NOT a success response. This is the concrete proof the catastrophic "anyone can write" hole from the original design doc is closed.

- [ ] **Step 4: Confirm authenticated login works end-to-end**

Open `index.html` in a browser, log in with one real admin account and one real operator account (separately). For each: confirm login succeeds, the correct role/permissions are applied (admin sees the user-management button per Task 3/5; operator does not), and a save action (e.g. editing the daily report date) completes without a console error, with the Network tab showing a `200` response from `system_bundle.json?auth=...`.

- [ ] **Step 5: Confirm the audit log is being written**

After the save from Step 4, run:
`curl -s "https://hr-cooling-default-rtdb.firebaseio.com/audit_log.json?auth=<one of the idTokens from Step 4's Network tab>"`
Expected: a JSON object containing at least one entry with `action: "save_system_bundle"` and the matching `uid`.

- [ ] **Step 6: Commit**

```bash
git add index.html "نظام_ادارة_الملاك_v8.5_cloud.html"
git commit -m "Wire in production Firebase Web API key after console setup"
```
