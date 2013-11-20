import json
import urllib

# Short script to generate static MP files.
#
# Start the webserver using the instructions
# in README.md, then run this from a python
# prompt.
def generate_static():
    with open('data.json') as data_file:
        data = json.load(data_file)

    for mp in data:
        r = urllib.urlopen('http://localhost:5000/mp/%s' % mp['twfy_id'])
        with open('static/html/%s.html' % mp['twfy_id'], 'w') as f:
            html = r.read()
            html = html.replace('"/static/', '"../')  # fix paths
            f.write(html)

