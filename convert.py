import markdown
import sciris as sc
text = sc.loadtext('index.md')
html = markdown.markdown(text, extensions=['md_in_html'])
sc.savetext('output.html', html)