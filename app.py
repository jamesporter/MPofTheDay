import json
from random import choice

from flask import Flask
from flask import render_template

app = Flask(__name__)

@app.route("/")
def home():
    with open('data.json') as data_file:    
        data = json.load(data_file)
    return render_template('index.html', data=data)

@app.route('/mp/<twfy_id>.html')
def show_mp(twfy_id):
    with open('data.json') as data_file:
        data = json.load(data_file)

    success = False
    while data:
        mp = data.pop()
        if mp['twfy_id'] == twfy_id:
            success = True
            break

    if success:
        mp['first_name'] = mp['name'].split()[0]
        return render_template('mp.html', mp=mp, hat_choice=choice([0,1,2]))

    return '<h1>That&rsquo;s a 404.</h1>'

if __name__ == "__main__":
    app.run()
