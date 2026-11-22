import re, json

def save_template(src_html, out_path):
    with open(src_html, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()
    tmpl_m = re.search(r'<script[^>]*type=[\'"]__bundler/template[\'"][^>]*>(.*?)</script>', content, re.DOTALL)
    if not tmpl_m:
        print(f"No template in {src_html}")
        return
    tmpl_raw = tmpl_m.group(1).strip()
    # It is a JSON string literal (starts and ends with quotes)
    tmpl_unescaped = json.loads(tmpl_raw)
    with open(out_path, 'w', encoding='utf-8') as out_f:
        out_f.write(tmpl_unescaped)
    print(f"Saved unescaped template: {out_path} ({len(tmpl_unescaped)} chars)")

save_template('redesign/unpacked_notebook/page_16_Notebook___Light_b8140d78.html', 'redesign/notebook_light_raw.html')
save_template('redesign/unpacked_notebook/page_17_Notebook___Dark_1dc3caad.html', 'redesign/notebook_dark_raw.html')
save_template('redesign/unpacked_notebook/page_11_Redesign_K___Notebook_57298bf6.html', 'redesign/redesign_k_notebook_raw.html')
