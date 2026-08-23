import re
import os

def fix_file(file_path):
    if not os.path.exists(file_path):
        return
    with open(file_path, 'r', encoding='utf-8') as f:
        code = f.read()

    # Extract sync engine code block and remove it from line 460 area
    pattern = r"// ----------------------------------------------------\s+// محرك المزامنة حياً مع السيرفر المحلي للشعبة \(Local Live Sync Engine\).*?// بث التغييرات عند تعديل أي بيانات في النظام\s+React\.useEffect\(\(\) => \{\s+if \(!isSyncingRef\.current && syncStatus\.connected\) \{\s+pushDataToServer\(\);\s+\}\s+\}, \[.*?\]\);"
    
    match = re.search(pattern, code, re.DOTALL)
    if not match:
        print(f"Sync engine block not matched in {file_path}")
        return

    sync_block = match.group(0)
    
    # Clean the sync block to ensure anchorDate is used consistently
    sync_block = sync_block.replace("shiftAnchorDate: shiftAnchorDate,", "shiftAnchorDate: anchorDate,")
    sync_block = sync_block.replace("shiftAnchorDate", "anchorDate")

    # Remove sync block from current position
    code = code.replace(sync_block, "")

    # Target insertion point: AFTER anchorDate, threeShiftAnchorSquad, twoShiftAnchorSquad, dailyReportDate state declarations!
    target_anchor = "localStorage.setItem('twoShiftAnchorSquad', twoShiftAnchorSquad);\n            }, [anchorDate, threeShiftAnchorSquad, twoShiftAnchorSquad]);"

    if target_anchor in code:
        code = code.replace(target_anchor, target_anchor + "\n\n" + sync_block)
        print(f"✓ Successfully repositioned sync engine after state declarations in {file_path}")
    else:
        print(f"Target anchor not found in {file_path}")

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(code)

if __name__ == '__main__':
    fix_file('e:/Antigravity projects/HR Admin/index.html')
    fix_file('e:/Antigravity projects/HR Admin/نظام_ادراة_الملاك_v6.8_online.html')
    fix_file('e:/Antigravity projects/HR Admin/نظام_ادراة_الملاك_v6.8.html')
