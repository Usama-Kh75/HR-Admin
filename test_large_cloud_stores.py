import urllib.request
import json

# Generate ~150KB test staff payload
test_staff = []
for i in range(150):
    test_staff.append({
        "id": i + 1,
        "name": f"موظف تجريبي رقم {i+1}",
        "jobNumber": str(1000 + i),
        "unit": "تبريد المركز",
        "workType": "صباحي",
        "jobTitle": "مهندس",
        "phone": "07701234567"
    })

bundle_payload = {
    "version": "v7.5 Cloud Edition Beta",
    "lastCloudUpdate": "2026-08-16T19:00:00.000Z",
    "staffData": test_staff,
    "officialHolidaysList": ["2026-08-01", "2026-08-02"],
    "dailyStatusOverrides": {},
    "hourlyLeaveRecords": [],
    "overtimeHoursRecords": []
}

payload_json = json.dumps(bundle_payload)
print(f"Testing with payload size: {len(payload_json)} bytes (~{len(payload_json)//1024} KB)")

# Test 1: JSONStorage.net
try:
    req = urllib.request.Request(
        "https://api.jsonstorage.net/v1/json",
        data=payload_json.encode('utf-8'),
        headers={'Content-Type': 'application/json'}
    )
    with urllib.request.urlopen(req) as resp:
        res = json.loads(resp.read().decode('utf-8'))
        print("✓ JSONStorage Success! URI:", res.get('uri'))
except Exception as e:
    print("JSONStorage error:", e)

# Test 2: JSONBin.io Public
try:
    req2 = urllib.request.Request(
        "https://api.jsonbin.io/v3/b",
        data=payload_json.encode('utf-8'),
        headers={
            'Content-Type': 'application/json',
            'X-Master-Key': '$2a$10$w81c7J9qjV7G7N81f6mHxe01234567890abcdef'
        }
    )
except Exception as e:
    print("JSONBin error:", e)
