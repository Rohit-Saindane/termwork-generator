import re

with open('redesign/notebook_light_raw.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Let's find each screen by splitting on `<p class="cap">`
parts = html.split('<p class="cap">')
for i, p in enumerate(parts[1:], 1):
    cap_end = p.find('</p>')
    cap = p[:cap_end]
    content = p[cap_end+4:]
    # find where this frame ends: usually at next </section> or </div></div></div>
    print(f"\n==================================================")
    print(f"SCREEN {i}: {cap}")
    print(f"==================================================")
    # clean out styles or scripts
    clean = re.sub(r'<script.*?</script>', '', content, flags=re.DOTALL)
    print(clean[:1200].strip())
