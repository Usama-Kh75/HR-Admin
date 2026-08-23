import urllib.request
import json

# Test npoint.io, kvdb.io, and jsonstorage.net for instant GET/PUT sync
def test_endpoints():
    print("Testing cloud sync endpoints...")
    
    # Test npoint.io creation
    try:
        req = urllib.request.Request(
            'https://api.npoint.io',
            data=json.dumps({"test": "hello_basra_hr"}).encode('utf-8'),
            headers={'Content-Type': 'application/json'}
        )
        with urllib.request.urlopen(req) as response:
            res_data = json.loads(response.read().decode('utf-8'))
            print("npoint.io creation success:", res_data)
    except Exception as e:
        print("npoint.io error:", e)

if __name__ == '__main__':
    test_endpoints()
