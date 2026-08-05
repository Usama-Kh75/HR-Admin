import os

# 1. Write cloud_server.py for Render deployment
cloud_server_code = """import os
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
"""

with open('e:/Antigravity projects/HR Admin/cloud_server.py', 'w', encoding='utf-8') as f:
    f.write(cloud_server_code)

# 2. Write Procfile for Render
with open('e:/Antigravity projects/HR Admin/Procfile', 'w', encoding='utf-8') as f:
    f.write("web: python cloud_server.py\n")

# 3. Write requirements.txt
with open('e:/Antigravity projects/HR Admin/requirements.txt', 'w', encoding='utf-8') as f:
    f.write("# Standard Python Libraries\n")

print("✓ Created cloud_server.py, Procfile, and requirements.txt for Render deployment")
