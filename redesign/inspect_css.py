import re

with open('redesign/notebook_light_raw.html', 'r', encoding='utf-8') as f:
    light = f.read()

# remove font-face definitions to see actual CSS rules
clean_css = re.sub(r'@font-face\s*\{[^}]*\}', '', light)

styles = re.findall(r'<style[^>]*>(.*?)</style>', clean_css, re.DOTALL)
print(f"Total styles in light: {len(styles)}")
for i, s in enumerate(styles):
    print(f"\n--- Style {i} (len: {len(s)}) ---")
    print(s[:1500])

# check the HTML structure inside body
body_m = re.search(r'<body[^>]*>(.*?)</body>', light, re.DOTALL)
if body_m:
    print("\n--- BODY HTML (without scripts) ---")
    body_clean = re.sub(r'<script.*?</script>', '', body_m.group(1), flags=re.DOTALL)
    body_clean = re.sub(r'<style.*?</style>', '', body_clean, flags=re.DOTALL)
    print(body_clean[:2000])
