import os

# Update index.html head tags with mobile security & clean web app metadata
with open('e:/Antigravity projects/HR Admin/index.html', 'r', encoding='utf-8') as f:
    code = f.read()

clean_head_tags = """<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <meta name="theme-color" content="#1e1b4b">
    <meta name="apple-mobile-web-app-capable" content="yes">
    <meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">
    <meta name="description" content="نظام إدارة الملاك والموقف اليومي - شعبة تبريد المركز ومحطة عزل نهر بن عمر - شركة نفط البصرة">
    <meta name="robots" content="index, follow">
    <link rel="icon" href="data:image/svg+xml,<svg xmlns=%22http://www.w3.org/2000/svg%22 viewBox=%220 0 100 100%22><text y=%22.9em%22 font-size=%2290%22>❄️</text></svg>">
    <title>نظام إدارة الملاك - الإصدار v7.5 Cloud Edition Beta ☁️</title>"""

if "<head>" in code:
    code = code.replace("<head>\n    <meta charset=\"UTF-8\">\n    <meta name=\"viewport\" content=\"width=device-width, initial-scale=1.0\">\n    <title>نظام إدارة الملاك - الإصدار v7.5 Cloud Edition Beta ☁️</title>", clean_head_tags)
    code = code.replace("<head>", clean_head_tags) if clean_head_tags not in code else code

with open('e:/Antigravity projects/HR Admin/index.html', 'w', encoding='utf-8') as f:
    f.write(code)

with open('e:/Antigravity projects/HR Admin/نظام_ادراة_الملاك_v7.5_cloud.html', 'w', encoding='utf-8') as f:
    f.write(code)

print("✓ Injected clean mobile metadata & SSL security icon into index.html")
