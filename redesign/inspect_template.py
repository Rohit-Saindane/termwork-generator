import re

with open('redesign/unpacked_notebook/page_16_Notebook___Light_b8140d78.html', 'r', encoding='utf-8', errors='ignore') as f:
    c16 = f.read()

tmpl_m = re.search(r'<script[^>]*type=[\'"]__bundler/template[\'"][^>]*>(.*?)</script>', c16, re.DOTALL)
if tmpl_m:
    print("=== TEMPLATE IN P16 ===")
    print(tmpl_m.group(1)[:2000])

for fname in ['fb557de9-2a0.js', 'ceabed60-687.js', '55476bf0-bda.js']:
    fpath = f'redesign/unpacked_p16/{fname}'
    with open(fpath, 'r', encoding='utf-8', errors='ignore') as f:
        js_c = f.read()
    print(f"\n=== {fname} ({len(js_c)} bytes) ===")
    print(js_c[:500])
