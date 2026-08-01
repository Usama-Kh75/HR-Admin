@echo off
chcp 65001 > nul
title توليد مجلد المكتبات (libs) للعمل بدون إنترنت
color 0B

echo ==========================================================
echo   أداة توليد وتنزيل مجلد المكتبات (libs) للعمل دون اتصال
echo ==========================================================
echo.
echo سيتم إنشاء مجلد باسم "libs" في نفس الموقع الحالي وتحميل المكتبات اللازمة إليه.
echo يرجى التأكد من اتصال الحاسوب بالإنترنت أثناء تشغيل الأداة لأول مرة.
echo.
echo اضغط على أي مفتاح لبدء التحميل...
pause > nul
echo.

powershell -NoProfile -ExecutionPolicy Bypass -Command "
$libs = @{
    'react.production.min.js' = 'https://unpkg.com/react@18/umd/react.production.min.js';
    'react-dom.production.min.js' = 'https://unpkg.com/react-dom@18/umd/react-dom.production.min.js';
    'babel.min.js' = 'https://unpkg.com/@babel/standalone@7.26.2/babel.min.js';
    'tailwindcss.js' = 'https://cdn.tailwindcss.com';
    'xlsx.full.min.js' = 'https://cdnjs.cloudflare.com/ajax/libs/xlsx/0.18.5/xlsx.full.min.js';
    'exceljs.min.js' = 'https://cdn.jsdelivr.net/npm/exceljs@4.3.0/dist/exceljs.min.js';
    'docx.js' = 'https://unpkg.com/docx@7.8.2/build/index.js';
    'FileSaver.min.js' = 'https://cdnjs.cloudflare.com/ajax/libs/FileSaver.js/2.0.5/FileSaver.min.js'
};

if (!(Test-Path 'libs')) {
    New-Item -ItemType Directory -Path 'libs' | Out-Null
    Write-Host '✓ تم إنشاء مجلد libs جديد.' -ForegroundColor Green
} else {
    Write-Host 'ℹ مجلد libs موجود بالفعل، سيتم تحديث الملفات بداخله.' -ForegroundColor Yellow
}

$headers = @{ 'User-Agent' = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)' };

foreach ($file in $libs.Keys) {
    $url = $libs[$file];
    $dest = Join-Path 'libs' $file;
    Write-Host \"  • جاري تحميل: $file ...\" -ForegroundColor Cyan;
    try {
        [Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12;
        Invoke-WebRequest -Uri $url -OutFile $dest -Headers $headers -TimeoutSec 30;
        Write-Host \"    ✓ تم تحميل الملف بنجاح.\" -ForegroundColor Green;
    } catch {
        Write-Host \"    ❌ فشل تحميل الملف: $_\" -ForegroundColor Red;
    }
}
"

echo.
echo ==========================================================
echo   اكتملت العملية! ستجد مجلد (libs) جاهزاً الآن بجانب الملف.
echo   اضغط أي مفتاح للإغلاق...
echo ==========================================================
pause > nul
