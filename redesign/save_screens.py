import re, os

with open('redesign/notebook_light_raw.html', 'r', encoding='utf-8') as f:
    html = f.read()

out_dir = 'redesign/screens'
os.makedirs(out_dir, exist_ok=True)

parts = html.split('<p class="cap">')
for i, p in enumerate(parts[1:], 1):
    cap_end = p.find('</p>')
    cap = p[:cap_end].strip()
    safe_name = re.sub(r'[^a-zA-Z0-9_\-]', '_', cap)
    content = p[cap_end+4:]
    # find where frame ends (it ends before next <div class="vp" or </section> or <div class="row">)
    # usually ends with </div></div></div> (vp ends)
    clean = re.sub(r'<script.*?</script>', '', content, flags=re.DOTALL)
    with open(os.path.join(out_dir, f"{i:02d}_{safe_name}.html"), 'w', encoding='utf-8') as out_f:
        out_f.write(clean)
    print(f"Saved screen {i}: {safe_name}")
