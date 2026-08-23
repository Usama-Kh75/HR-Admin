import urllib.request
import json

def test_firebase():
    test_url = "https://hr-admin-cooling-default-rtdb.firebaseio.com/bundle.json"
    test_data = {"test": "basra_cooling_online_sync", "timestamp": 123456}
    
    # Try PUT
    req = urllib.request.Request(
        test_url,
        data=json.dumps(test_data).encode('utf-8'),
        headers={'Content-Type': 'application/json'},
        method='PUT'
    )
    try:
        with urllib.request.urlopen(req) as resp:
            print("Firebase PUT success:", resp.read().decode('utf-8'))
    except Exception as e:
        print("Firebase error:", e)

if __name__ == '__main__':
    test_firebase()
