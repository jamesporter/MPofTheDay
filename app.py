from datetime import datetime
import calendar
import time
import json
from random import choice

from flask import Flask
from flask import render_template

app = Flask(__name__)

@app.route("/cal/<month>/<year>")
def show_calendar(month, year):
    with open('data.json') as data_file:    
        data = json.load(data_file)

    month = month.title()

    first = "01 %s %s" % (month, year)
    first_date = datetime.strptime(first, "%d %B %Y")

    total_days = calendar.monthrange(year, first_date.month)[1]
    weekday = first_date.weekday()

    return render_template('calendar.html', data=data, month=month, year=year, render_data=render_data)

@app.route('/mp/<twfy_id>.html')
def show_mp(twfy_id):
    with open('data-latest.json') as data_file:
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
