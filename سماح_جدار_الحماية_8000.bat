@echo off
chcp 65001 > nul
title HR Admin - Open Firewall Port 8000

echo ==================================================================
echo   🚀 جاري تفعيل السماح للشبكة المحلية والبورت 8000 في جدار الحماية
echo ==================================================================
echo.

netsh advfirewall firewall delete rule name="HR Admin Local Sync Server 8000" >nul 2>&1
netsh advfirewall firewall add rule name="HR Admin Local Sync Server 8000" dir=in action=allow protocol=TCP localport=8000

echo.
echo ==================================================================
echo   ✅ تم تفعيل السماح بنجاح!
echo   يمكن الآن لبقية حواسب وموبايلات الشعبة الاتصال بالرابط:
echo   http://172.16.22.54:8000
echo ==================================================================
echo.
pause
