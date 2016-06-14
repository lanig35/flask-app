import jinja2
import json

env = jinja2.Environment(loader=jinja2.FileSystemLoader(["."]))
template = env.get_template ('list.html')

with open ('json.data', 'r') as f:
    dataset = json.loads (f.readline())

print template.render (title='Alain', dataset=dataset)

with open ('json.txt', 'r') as f:
    dataset = json.load (f)
page = template.render (title='Pierre', dataset=dataset)

with open ('page.html', 'w') as f:
    f.write (page)
