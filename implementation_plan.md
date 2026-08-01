# 🌐 خطة تفعيل المزامنة المحلية الحية بين أجهزة الشعبة (Local Network Live Sync Plan)

تستهدف هذه الخطة إنشاء وتكامل **نظام مزامنة محلي مستقل وحي (Local Live Sync Engine)** يربط الحاسبة الرئيسية (Master PC) في الشعبة بالأجهزة الطرفية (Client PCs/Mobiles) عبر الراوتر الداخلي بدون الحاجة للإنترنت، مع الحفاظ التام على ذاكرة الجهاز المحلية كنسخة احتياطية.

---

## 🏛️ الآلية المعمارية للمزامنة المحلية (Architecture Overview)

```mermaid
graph TD
    subgraph MasterPC ["🖥️ الحاسبة الرئيسية (Master PC)"]
        Server ["🐍 local_sync_server.py (Port 8000)"]
        DB [("💾 hr_system_database.json")]
        UI1 ["🌐 index.html (Master UI)"]
        Server <--> DB
        UI1 <-->|HTTP / API| Server
    end

    subgraph ClientDevices ["📱💻 الأجهزة الطرفية بالشعبة (Client Devices)"]
        UI2 ["🌐 Client 1 (http://192.168.1.X:8000)"]
        UI3 ["📱 Mobile/Tablet (http://192.168.1.X:8000)"]
    end

    UI2 <-->|Auto-Sync & Live Polling| Server
    UI3 <-->|Auto-Sync & Live Polling| Server
```

---

## 📐 التغييرات المقترحة (Proposed Changes)

### 1. 🐍 إنشاء خادم المزامنة المحلي الخفيف [NEW]
#### [NEW] [local_sync_server.py](file:///e:/Antigravity%20projects/HR%20Admin/local_sync_server.py)
- **الوظيفة:** سيرفر بلغة Python القياسية (بدون مكتبات خارجية):
  - استضافة ملفات الويب الاستاتيكية (`index.html` وإغنائها عبر Port `8000`).
  - حفظ وتحديث قاعدة البيانات المركزية للشعبة في ملف `hr_system_database.json`.
  - توفير واجهة API خفيفة ومستقرة:
    * `GET /api/sync`: لجلب آخر نسخة بيانات من السيرفر.
    * `POST /api/sync`: لإرسال التحديثات الجديدة من أي جهاز للسيرفر وتعميمها.
    * `GET /api/poll?v=N`: للفحص الدوري السريع (Polling كل 3 ثوانٍ) لسرعة تحديث شاشات باقي المستخدمين.

---

### 2. ⚡ موديول المزامنة في الواجهة وشريط التنبيه التفاعلي [MODIFY]
#### [MODIFY] [index.html](file:///e:/Antigravity%20projects/HR%20Admin/index.html)
#### [MODIFY] [نظام_ادراة_الملاك_v6.8_online.html](file:///e:/Antigravity%20projects/HR%20Admin/%D9%86%D8%B8%D8%A7%D9%85_%D8%A7%D8%AF%D8%B1%D8%A7%D8%A9_%D8%A7%D9%84%D9%85%D9%84%D8%A7%D9%83_v6.8_online.html)
- إضافة محرك المزامنة `LocalSyncEngine` داخل التطبيق:
  - **عند الإقلاع:** جلب أحدث نسخة بيانات من السيرفر المحلي. إذا كان السيرفر فارغاً، رفع البيانات المحلية الحالية للسيرفر تلقائياً.
  - **عند التعديل:** (حفظ موظف، تعديل موقف يومي، عطلة رسمية، إجازة زمنية)، يتم الحفظ محلياً أولاً ثم بث التحديث للسيرفر فوراً.
  - **شريط المؤشر الحي (Live Status Badge):**
    * 🟢 **مربوط بالسيرفر المحلي (`http://192.168.1.X:8000`)** — مع إظهار زري "مزامنة الآن" و "عرض رابط الشعبة".
    * 🟡 **مستقل محلياً (Offline Local Mode)** — في حال كانت الحاسبة غير متصلة بالشبكة.

---

### 3. 📜 تحديث سكربت التشغيل التلقائي للشعبة [MODIFY]
#### [MODIFY] [تشغيل_السيرفر_المحلي.bat](file:///e:/Antigravity%20projects/HR%20Admin/%D8%AA%D8%B4%D8%BA%D9%8A%D9%84_%D8%A7%D9%84%D8%B3%D9%8A%D8%B1%D9%81%D8%B1_%D8%A7%D9%84%D9%85%D8%AD%D9%84%D9%8A.bat)
- تشغيل السيرفر المطور `local_sync_server.py` وإظهار عنوان الـ IP المحلي بوضوح ومباشرةً لتسهيل ربط الحواسب والموبايلات بالشبكة.

---

## 🧪 خطة التحقق والاختبار (Verification Plan)

### 1. الفحص الآلي للبناء التركيبي (Automated Babel Check)
- تشغيل سكربت الفحص التركيبي لضمان سلامة كود JSX من الأخطاء:
  ```bash
  python scratch/compile_jsx_with_node.py
  ```

### 2. فحص السيرفر المحلي والـ API
- تشغيل `local_sync_server.py` واختبار استجابة الـ endpoints (`/api/sync` و `/api/status`) عبر طلبات HTTP حية.

### 3. المزامنة مع سطح المكتب
- نسخ ملفات النظام وسكربت التشغيل المحدثة فورياً إلى سطح المكتب:
  `C:\Users\asalz\OneDrive\Desktop`
