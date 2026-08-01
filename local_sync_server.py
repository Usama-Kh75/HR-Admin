import http.server
import socketserver
import json
import os
import socket
import threading
import time

PORT = 8000
DB_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'hr_system_database.json')

# In-memory lock for atomic file updates
db_lock = threading.Lock()

def get_local_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(('10.255.255.255', 1))
        ip = s.getsockname()[0]
    except Exception:
        ip = '127.0.0.1'
    finally:
        s.close()
    return ip

def load_db():
    with db_lock:
        if not os.path.exists(DB_FILE):
            default_data = {
                "version": 1,
                "last_updated": time.strftime("%Y-%m-%d %H:%M:%S"),
                "data": {}
            }
            with open(DB_FILE, 'w', encoding='utf-8') as f:
                json.dump(default_data, f, ensure_ascii=False, indent=2)
            return default_data
        try:
            with open(DB_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception:
            return {"version": 1, "last_updated": time.strftime("%Y-%m-%d %H:%M:%S"), "data": {}}

def save_db(db_obj):
    with db_lock:
        db_obj["version"] = db_obj.get("version", 1) + 1
        db_obj["last_updated"] = time.strftime("%Y-%m-%d %H:%M:%S")
        with open(DB_FILE, 'w', encoding='utf-8') as f:
            json.dump(db_obj, f, ensure_ascii=False, indent=2)
        return db_obj

class LocalSyncHTTPHandler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        # Enable CORS for local network requests
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.send_header('Cache-Control', 'no-cache, no-store, must-revalidate')
        super().end_headers()

    def do_OPTIONS(self):
        self.send_response(200, "OK")
        self.end_headers()

    def do_GET(self):
        if self.path.startswith('/api/status'):
            db = load_db()
            response = {
                "status": "online",
                "ip": get_local_ip(),
                "port": PORT,
                "version": db.get("version", 1),
                "last_updated": db.get("last_updated", "")
            }
            self.send_response(200)
            self.send_header('Content-Type', 'application/json; charset=utf-8')
            self.end_headers()
            self.wfile.write(json.dumps(response, ensure_ascii=False).encode('utf-8'))
            return

        elif self.path.startswith('/api/sync'):
            db = load_db()
            self.send_response(200)
            self.send_header('Content-Type', 'application/json; charset=utf-8')
            self.end_headers()
            self.wfile.write(json.dumps(db, ensure_ascii=False).encode('utf-8'))
            return

        elif self.path.startswith('/api/poll'):
            db = load_db()
            client_version = 0
            if 'version=' in self.path:
                try:
                    client_version = int(self.path.split('version=')[1].split('&')[0])
                except ValueError:
                    client_version = 0

            server_version = db.get("version", 1)
            has_update = server_version > client_version

            response = {
                "has_update": has_update,
                "version": server_version,
                "last_updated": db.get("last_updated", ""),
                "data": db.get("data") if has_update else None
            }
            self.send_response(200)
            self.send_header('Content-Type', 'application/json; charset=utf-8')
            self.end_headers()
            self.wfile.write(json.dumps(response, ensure_ascii=False).encode('utf-8'))
            return

        # Default static file serving
        return super().do_GET()

    def do_POST(self):
        if self.path.startswith('/api/sync'):
            content_length = int(self.headers.get('Content-Length', 0))
            post_data = self.rfile.read(content_length)
            try:
                payload = json.loads(post_data.decode('utf-8'))
                current_db = load_db()
                
                # Merge or replace payload data
                incoming_data = payload.get("data", payload)
                current_db["data"] = incoming_data
                
                updated_db = save_db(current_db)

                response = {
                    "success": True,
                    "version": updated_db["version"],
                    "last_updated": updated_db["last_updated"]
                }
                self.send_response(200)
                self.send_header('Content-Type', 'application/json; charset=utf-8')
                self.end_headers()
                self.wfile.write(json.dumps(response, ensure_ascii=False).encode('utf-8'))
            except Exception as e:
                response = {"success": False, "error": str(e)}
                self.send_response(500)
                self.send_header('Content-Type', 'application/json; charset=utf-8')
                self.end_headers()
                self.wfile.write(json.dumps(response, ensure_ascii=False).encode('utf-8'))
            return

        self.send_response(404)
        self.end_headers()

def main():
    local_ip = get_local_ip()
    print("==================================================================")
    print("      🚀 سيرفر المزامنة السحابية والمحلية لنظام إدارة الملاك      ")
    print("==================================================================")
    print(f"  • الحاسبة الرئيسية (Master PC):  http://localhost:{PORT}")
    print(f"  • رابط أجهزة الشعبة (Clients):  http://{local_ip}:{PORT}")
    print("------------------------------------------------------------------")
    print(f"  • قاعدة البيانات الحية:         {DB_FILE}")
    print("==================================================================")
    print("  ملاحظة: أبقِ هذه النافذة السوداء مفتوحة أثناء ساعات الدوام بالشعبة.")
    print("  لإيقاف السيرفر: اغلق النافذة مباشرة.")
    print("==================================================================")

    socketserver.TCPServer.allow_reuse_address = True
    with socketserver.TCPServer(('', PORT), LocalSyncHTTPHandler) as httpd:
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nتم إيقاف السيرفر بنجاح.")

if __name__ == '__main__':
    main()
