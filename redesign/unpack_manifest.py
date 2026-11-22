import re, json, base64, gzip, os

with open('redesign/notebook-design.html', 'r', encoding='utf-8', errors='ignore') as f:
    content = f.read()

manifest_m = re.search(r'<script[^>]*type=[\'"]__bundler/manifest[\'"][^>]*>(.*?)</script>', content, re.DOTALL)
order_m = re.search(r'<script[^>]*type=[\'"]__bundler/page_order[\'"][^>]*>(.*?)</script>', content, re.DOTALL)

if not manifest_m:
    print("No manifest found!")
    exit(1)

manifest = json.loads(manifest_m.group(1))
order = json.loads(order_m.group(1)) if order_m else list(manifest.keys())

out_dir = 'redesign/unpacked_notebook'
os.makedirs(out_dir, exist_ok=True)

print(f"Total entries in manifest: {len(manifest)}")
print(f"Page order count: {len(order)}")

page_num = 1
for key in order:
    if key not in manifest:
        continue
    item = manifest[key]
    mime = item.get('mime', '')
    data_b64 = item.get('data', '')
    is_compressed = item.get('compressed', False)
    
    raw = base64.b64decode(data_b64)
    if is_compressed:
        raw = gzip.decompress(raw)
        
    ext = '.bin'
    if 'html' in mime:
        ext = '.html'
    elif 'css' in mime:
        ext = '.css'
    elif 'javascript' in mime or 'json' in mime:
        ext = '.js'
    elif 'font' in mime or 'woff2' in mime:
        ext = '.woff2'
    elif 'png' in mime:
        ext = '.png'
    elif 'jpeg' in mime or 'jpg' in mime:
        ext = '.jpg'
    elif 'svg' in mime:
        ext = '.svg'
        
    # check if title is in html
    title = f"page_{page_num:02d}"
    if 'html' in mime:
        try:
            txt = raw.decode('utf-8', errors='ignore')
            tm = re.search(r'<title>(.*?)</title>', txt, re.IGNORECASE)
            if tm:
                safe_title = re.sub(r'[^a-zA-Z0-9_\-]', '_', tm.group(1))[:40]
                title = f"page_{page_num:02d}_{safe_title}"
        except:
            pass
            
    filename = f"{title}_{key[:8]}{ext}"
    filepath = os.path.join(out_dir, filename)
    with open(filepath, 'wb') as out_f:
        out_f.write(raw)
    print(f"Saved [{mime}] -> {filename} ({len(raw)} bytes)")
    if 'html' in mime:
        page_num += 1

# Also check other entries not in order
for key, item in manifest.items():
    if key in order:
        continue
    mime = item.get('mime', '')
    data_b64 = item.get('data', '')
    is_compressed = item.get('compressed', False)
    raw = base64.b64decode(data_b64)
    if is_compressed:
        raw = gzip.decompress(raw)
    if 'html' in mime or 'css' in mime or 'svg' in mime:
        ext = '.html' if 'html' in mime else ('.css' if 'css' in mime else '.svg')
        fn = f"extra_{key[:8]}{ext}"
        with open(os.path.join(out_dir, fn), 'wb') as out_f:
            out_f.write(raw)
        print(f"Saved EXTRA [{mime}] -> {fn} ({len(raw)} bytes)")
