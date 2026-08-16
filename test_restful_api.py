import urllib.request
import json

def test_restful_api():
    url = "https://api.restful-api.dev/objects"
    payload = {
        "name": "HR Admin Basra Oil Company",
        "data": {
            "version": "v7.5 Cloud Edition Beta",
            "staffData": [{"id": 1, "name": "أحمد"}]
        }
    }
    
    # 1. Create Object
    req = urllib.request.Request(
        url,
        data=json.dumps(payload).encode('utf-8'),
        headers={'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'}
    )
    try:
        with urllib.request.urlopen(req) as resp:
            res = json.loads(resp.read().decode('utf-8'))
            obj_id = res.get('id')
            print("✓ Created Cloud Object ID:", obj_id)

            # 2. Update Object (PUT)
            update_url = f"https://api.restful-api.dev/objects/{obj_id}"
            update_payload = {
                "name": "HR Admin Basra Oil Company",
                "data": {
                    "version": "v7.5 Cloud Edition Beta",
                    "staffData": [{"id": 1, "name": "أحمد علي"}]
                }
            }
            req_put = urllib.request.Request(
                update_url,
                data=json.dumps(update_payload).encode('utf-8'),
                headers={'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
                method='PUT'
            )
            with urllib.request.urlopen(req_put) as resp_put:
                res_put = json.loads(resp_put.read().decode('utf-8'))
                print("✓ Successfully Updated Cloud Object via PUT:", res_put)

            # 3. Read Object (GET)
            req_get = urllib.request.Request(update_url, headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req_get) as resp_get:
                res_get = json.loads(resp_get.read().decode('utf-8'))
                print("✓ Successfully Retrieved Cloud Object via GET:", res_get['data']['staffData'])
    except Exception as e:
        print("Restful API error:", e)

if __name__ == '__main__':
    test_restful_api()
