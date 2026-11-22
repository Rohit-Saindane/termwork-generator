with open('redesign/screens/02_1___FILES___DESKTOP___880.html', 'r', encoding='utf-8') as f:
    text = f.read()

# Let's find '<div class="frame">'
pos = text.find('class="frame"')
if pos != -1:
    print(text[pos-10:pos+2500])
else:
    print(text[:2500])
