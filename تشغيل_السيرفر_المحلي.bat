@echo off
chcp 65001 > nul
title تشغيل سيرفر الملاك المحلي
color 0A

echo ==========================================================
echo   جاري فحص وتحديد عنوان الشبكة المحلي الخاص بحاسبتك...
echo ==========================================================
echo.

python -c "
import socket, http.server, socketserver, os

PORT = 8000

def get_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(('10.255.255.255', 1))
        IP = s.getsockname()[0]
    except Exception:
        IP = '127.0.0.1'
    finally:
        s.close()
    return IP

ip = get_ip()
print('=========================================================')
print('             سيرفر نظام الملاك المحلي يعمل الآن         ')
print('=========================================================')
print('  لفتح النظام من حاسبتك الحالية، افتح الرابط التالي:')
print(f'  • نسخة الأوفلاين: http://localhost:{PORT}/نظام_ادراة_الملاك_v6.0.html')
print(f'  • نسخة الأونلاين: http://localhost:{PORT}/نظام_ادراة_الملاك_v6.0_online.html')
print('---------------------------------------------------------')
print('  لفتح النظام من أي حاسبة أخرى أو موبايل متصل بنفس الراوتر:')
print(f'  • نسخة الأوفلاين: http://{ip}:{PORT}/نظام_ادراة_الملاك_v6.0.html')
print(f'  • نسخة الأونلاين: http://{ip}:{PORT}/نظام_ادراة_الملاك_v6.0_online.html')
print('=========================================================')
print('  ملاحظة: أبقِ هذه النافذة السوداء مفتوحة أثناء عمل السيرفر.')
print('  لإيقاف السيرفر: أغلق هذه النافذة مباشرة.')
print('=========================================================')

Handler = http.server.SimpleHTTPRequestHandler
socketserver.TCPServer.allow_reuse_address = True
try:
    with socketserver.TCPServer(('', PORT), Handler) as httpd:
        httpd.serve_forever()
except Exception as e:
    print(f'خطأ في تشغيل السيرفر: {e}')
"
pause
