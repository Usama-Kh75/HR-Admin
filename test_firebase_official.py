import urllib.request
import json

def test_firebase_realtime_db():
    url = "https://hr-cooling-default-rtdb.firebaseio.com/system_bundle.json"
    payload = {
        "version": "v7.5 Cloud Edition Beta",
        "lastCloudUpdate": "2026-08-16T22:25:00.000Z",
        "staffData": [{"id": 1, "name": "أحمد علي", "jobTitle": "مهندس"}],
        "officialHolidaysList": ["2026-08-01"],
        "dataEntryOperator": "م. أسامة خليل هاشم"
    }

    # 1. Test PUT (Save data to Cloud)
    print("Testing Firebase PUT...")
    req = urllib.request.Request(
        url,
        data=json.dumps(payload).encode('utf-8'),
        headers={'Content-Type': 'application/json'},
        method='PUT'
    )
    with urllib.request.urlopen(req) as resp:
        print("✓ Firebase Realtime DB PUT SUCCESS:", resp.read().decode('utf-8'))

    # 2. Test GET (Fetch data from Cloud)
    print("Testing Firebase GET...")
    with urllib.request.urlopen(url) as resp_get:
        res = json.loads(resp_get.read().decode('utf-8'))
        print("✓ Firebase Realtime DB GET SUCCESS:", res.get('version'), "| Staff Count:", len(res.get('staffData', [])))

if __name__ == '__main__':
    test_firebase_realtime_db()
