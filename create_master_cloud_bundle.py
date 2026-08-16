import urllib.request
import json

def create_master_cloud_store():
    url = "https://api.restful-api.dev/objects"
    master_payload = {
        "name": "HR_ADMIN_BASRA_OIL_COMPANY_MASTER_CLOUD_DB",
        "data": {
            "version": "v7.5 Cloud Edition Beta",
            "lastCloudUpdate": "2026-08-16T11:25:00.000Z",
            "staffData": [],
            "officialHolidaysList": [],
            "hourlyLeaveRecords": [],
            "overtimeHoursRecords": [],
            "dailyStatusOverrides": {},
            "shiftAnchorDate": "2026-01-01",
            "threeShiftAnchorSquad": "أ",
            "twoShiftAnchorSquad": "أ",
            "dataEntryOperator": "م. أسامة خليل هاشم"
        }
    }
    
    req = urllib.request.Request(
        url,
        data=json.dumps(master_payload).encode('utf-8'),
        headers={'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'}
    )
    with urllib.request.urlopen(req) as resp:
        res = json.loads(resp.read().decode('utf-8'))
        master_id = res.get('id')
        print("🎉 MASTER CLOUD STORE CREATED! ID:", master_id)
        return master_id

if __name__ == '__main__':
    create_master_cloud_store()
