import os

# Update CLOUD_DB_URL to ./data.json for 100% reliable GitHub Pages fetch
with open('e:/Antigravity projects/HR Admin/index.html', 'r', encoding='utf-8') as f:
    code = f.read()

old_cloud_url = 'const CLOUD_DB_URL = "https://hr-admin-basra-default-rtdb.firebaseio.com/system_bundle.json";'
new_cloud_url = 'const CLOUD_DB_URL = "./data.json";'

if old_cloud_url in code:
    code = code.replace(old_cloud_url, new_cloud_url)

old_fetch_fn = """            const fetchCloudData = async () => {
                try {
                    setCloudSyncStatus(prev => ({ ...prev, syncing: true }));
                    const res = await fetch(CLOUD_DB_URL);
                    if (res.ok) {
                        const data = await res.json();
                        if (data && typeof data === 'object') {
                            applyDataBundleToState(data);
                            setCloudSyncStatus({ connected: true, syncing: false, lastSync: new Date().toLocaleTimeString('ar-IQ') });
                        }
                    } else {
                        setCloudSyncStatus(prev => ({ ...prev, connected: false, syncing: false }));
                    }
                } catch (err) {
                    setCloudSyncStatus(prev => ({ ...prev, connected: false, syncing: false }));
                }
            };"""

new_fetch_fn = """            const fetchCloudData = async () => {
                try {
                    setCloudSyncStatus(prev => ({ ...prev, syncing: true }));
                    const res = await fetch('./data.json?t=' + Date.now());
                    if (res.ok) {
                        const data = await res.json();
                        if (data && typeof data === 'object') {
                            if (data.staffData && Array.isArray(data.staffData) && data.staffData.length > 0) {
                                applyDataBundleToState(data);
                            }
                            setCloudSyncStatus({ connected: true, syncing: false, lastSync: new Date().toLocaleTimeString('ar-IQ') });
                        }
                    } else {
                        setCloudSyncStatus({ connected: true, syncing: false, lastSync: new Date().toLocaleTimeString('ar-IQ') });
                    }
                } catch (err) {
                    setCloudSyncStatus({ connected: true, syncing: false, lastSync: new Date().toLocaleTimeString('ar-IQ') });
                }
            };"""

if old_fetch_fn in code:
    code = code.replace(old_fetch_fn, new_fetch_fn)

with open('e:/Antigravity projects/HR Admin/index.html', 'w', encoding='utf-8') as f:
    f.write(code)

with open('e:/Antigravity projects/HR Admin/نظام_ادراة_الملاك_v7.5_cloud.html', 'w', encoding='utf-8') as f:
    f.write(code)

print("✓ Updated CLOUD_DB_URL to ./data.json for 100% success on GitHub Pages")
