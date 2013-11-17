import json

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

    while data:
        mp = data.pop()
        if mp['twfy_id'] == twfy_id:
            break

    if mp:
        return render_template('mp.html', mp=mp)

    return None

if __name__ == "__main__":
    app.run()
