import re
import sys

with open('نظام_ادراة_الملاك_v6.6.html', 'r', encoding='utf-8') as f:
    content = f.read()

m = re.search(r'<script type="text/babel">(.*?)</script>', content, re.DOTALL)
if m:
    print(f"✅ JSX Script Block Extracted: {len(m.group(1))} characters")
else:
    print("❌ Failed to find JSX script block!")
    sys.exit(1)

# Check presence of key new features
features = [
    "v6.6 Beta",
    "دوام إضافي",
    "حضور في الاستراحة (عمل إضافي)",
    "periodReport",
    "periodStartDate",
    "periodEndDate",
    "exportPeriodReportExcel",
    "periodReportData"
]

for feat in features:
    if feat in content:
        print(f"  [✔] Feature '{feat}' verified in file.")
    else:
        print(f"  [❌] Feature '{feat}' MISSING!")
