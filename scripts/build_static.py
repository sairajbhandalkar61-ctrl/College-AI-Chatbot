with open('templates/cortex2.html', 'r', encoding='utf-8') as f:
    c = f.read()

c = c.replace("{{ url_for('static', filename='cortex2.css') }}", 'static/cortex2.css')
c = c.replace("{{ url_for('static', filename='cortex2.js') }}", 'static/cortex2.js')
c = c.replace('href="/chatbot"', 'href="chatbot.html"')

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(c)

print("Generated root index.html successfully for GitHub Pages!")
