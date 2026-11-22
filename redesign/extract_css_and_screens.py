import re

with open('redesign/notebook_light_raw.html', 'r', encoding='utf-8') as f:
    html = f.read()

# save CSS to file
styles = re.findall(r'<style[^>]*>(.*?)</style>', html, re.DOTALL)
if len(styles) > 1:
    with open('redesign/notebook_theme.css', 'w', encoding='utf-8') as cf:
        cf.write(styles[1])
    print(f"Saved notebook_theme.css ({len(styles[1])} chars)")

# inspect the views in the HTML
caps = re.findall(r'<p class="cap">(.*?)</p>', html)
print("Screens found in HTML:")
for c in caps:
    print("  *", c)
