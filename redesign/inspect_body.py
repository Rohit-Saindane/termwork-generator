import re

with open('redesign/unpacked_notebook/page_16_Notebook___Light_b8140d78.html', 'r', encoding='utf-8', errors='ignore') as f:
    c16 = f.read()

print("Page 16 length:", len(c16))
# Look for non-script HTML or React code
body_m = re.search(r'<body[^>]*>(.*?)</body>', c16, re.DOTALL | re.IGNORECASE)
if body_m:
    print("Body length:", len(body_m.group(1)))
    # print first 1500 chars of body
    clean = re.sub(r'<script.*?</script>', '[SCRIPT]', body_m.group(1), flags=re.DOTALL)
    print("Body content preview:")
    print(clean[:2000])

with open('redesign/unpacked_notebook/page_11_Redesign_K___Notebook_57298bf6.html', 'r', encoding='utf-8', errors='ignore') as f:
    c11 = f.read()

print("\n\nPage 11 length:", len(c11))
body_m11 = re.search(r'<body[^>]*>(.*?)</body>', c11, re.DOTALL | re.IGNORECASE)
if body_m11:
    clean11 = re.sub(r'<script.*?</script>', '[SCRIPT]', body_m11.group(1), flags=re.DOTALL)
    print("Page 11 body preview:")
    print(clean11[:2000])
