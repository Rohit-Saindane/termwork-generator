import re, json

with open('redesign/notebook-design.html', 'r', encoding='utf-8', errors='ignore') as f:
    content = f.read()

# find script tags
script_tags = re.findall(r'<script([^>]*)>(.*?)</script>', content, re.DOTALL)
for i, (attrs, body) in enumerate(script_tags):
    print(f"Script {i}: attrs={attrs.strip()}, len={len(body)}")
    print(f"  preview: {body[:150].strip()}")
