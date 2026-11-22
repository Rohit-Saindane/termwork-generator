import re, json, base64, gzip, os

def unpack_file(fpath, out_sub):
    with open(fpath, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()
    manifest_m = re.search(r'<script[^>]*type=[\'"]__bundler/manifest[\'"][^>]*>(.*?)</script>', content, re.DOTALL)
    if not manifest_m:
        print(f"No manifest in {fpath}")
        return
    manifest = json.loads(manifest_m.group(1))
    os.makedirs(out_sub, exist_ok=True)
    print(f"\nUnpacking {fpath} ({len(manifest)} entries) into {out_sub}")
    for k, item in manifest.items():
        mime = item.get('mime', '')
        raw = base64.b64decode(item.get('data', ''))
        if item.get('compressed'):
            raw = gzip.decompress(raw)
        ext = '.html' if 'html' in mime else ('.js' if 'javascript' in mime else ('.css' if 'css' in mime else '.bin'))
        fn = f"{k[:12]}{ext}"
        target = os.path.join(out_sub, fn)
        with open(target, 'wb') as out_f:
            out_f.write(raw)
        print(f"  [{mime}] {fn} ({len(raw)} bytes)")

unpack_file('redesign/unpacked_notebook/page_16_Notebook___Light_b8140d78.html', 'redesign/unpacked_p16')
unpack_file('redesign/unpacked_notebook/page_17_Notebook___Dark_1dc3caad.html', 'redesign/unpacked_p17')
unpack_file('redesign/unpacked_notebook/page_11_Redesign_K___Notebook_57298bf6.html', 'redesign/unpacked_p11')
