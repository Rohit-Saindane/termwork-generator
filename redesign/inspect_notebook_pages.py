import os, re

for fname in ['page_16_Notebook___Light_b8140d78.html', 'page_17_Notebook___Dark_1dc3caad.html', 'page_11_Redesign_K___Notebook_57298bf6.html']:
    fpath = os.path.join('redesign/unpacked_notebook', fname)
    if not os.path.exists(fpath):
        continue
    with open(fpath, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()
    print(f"=== {fname} ({len(content)} bytes) ===")
    styles = re.findall(r'<style[^>]*>(.*?)</style>', content, re.DOTALL)
    print(f"  Styles count: {len(styles)}")
    for i, s in enumerate(styles):
        print(f"    Style {i} length: {len(s)}")
    # Look for key terms
    for term in ['Caveat', 'spiral', 'washi', 'highlighter', 'stamp', 'sun', 'moon', 'paperclip', 'ruled', 'margin', 'drawer']:
        matches = len(re.findall(term, content, re.IGNORECASE))
        print(f"    Term '{term}': {matches} matches")
