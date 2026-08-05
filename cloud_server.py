import os
import http.server
import socketserver

PORT = int(os.environ.get('PORT', 8000))

class CloudHandler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Cache-Control', 'no-cache, no-store, must-revalidate')
        super().end_headers()

print(f"🚀 HR Admin System Cloud Server starting on port {PORT}...")
with socketserver.TCPServer(("", PORT), CloudHandler) as httpd:
    print(f"✅ Cloud Server Active & Ready!")
    httpd.serve_forever()
