import datetime
import calendar
import re
import json
from random import choice

from flask import Flask
from flask import render_template
from flask import redirect

app = Flask(__name__)
app.debug = True

def add_months(sourcedate, months):
    month = sourcedate.month - 1 + months
    year = sourcedate.year + month / 12
    month = month % 12 + 1
    day = min(sourcedate.day,calendar.monthrange(year,month)[1])
    return datetime.date(year,month,day)

@app.route("/cal/<month>/<year>")
def show_calendar(month, year):
    def chunks(l, n):
        """ Yield successive n-sized chunks from l.
        """
        for i in xrange(0, len(l), n):
            yield l[i:i+n]

    def get_mp_from_day(daystr, num):
        with open('data-latest.json') as data_file:    
            data = json.load(data_file)
        success = False
        while data:
            mp = data.pop()
            if mp['twfy_dob'] is None:
                continue
            if mp['twfy_dob'][4:] == daystr:
                success = True
                break
        if success:
            return {'hide': False, 'mp': mp, 'num': num}
        return {'hide': False, 'mp': None, 'num': num}

    monthword = month

    first = "01 %s %s" % (monthword, year)
    first_date = datetime.datetime.strptime(first, "%d %B %Y")

    month = int(first_date.month)
    total_days = calendar.monthrange(int(year), month)[1]
    weekday = first_date.weekday()

    block = [{'hide': True, 'mp': None, 'num': None} for x in range(weekday)]

    for x in range(1, int(total_days) + 1):
        daystr = '-%02d-%02d' % (month, x)
        block.append(get_mp_from_day(daystr, x))

    weeks = chunks(block, 7)

    return render_template('calendar.html', month=monthword, year=year, weeks=weeks)

@app.route('/mp/<twfy_id>')
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
        y = mp['twfy_dob'][:4]
        m = mp['twfy_dob'][5:7]
        d = mp['twfy_dob'][9:11]

        dt = datetime.datetime(int(y), int(m), int(d))
        age = 2013 - int(y)
        date = '%s %s' % (dt.day, datetime.datetime.strftime(dt, '%B'))

        mp['first_name'] = mp['name'].split()[0]
        return render_template('mp.html', mp=mp, hat_choice=choice([0,1,2]), date=date, age=age)

    return '<h1>That&rsquo;s a 404.</h1>'

@app.route('/cal/<month>/<year>/next')
def next_month(month, year):
    first = "01 %s %s" % (month, year)
    first_date = datetime.datetime.strptime(first, "%d %B %Y")
    new_date = add_months(first_date, 1)
    return redirect('/cal/' + datetime.datetime.strftime(new_date, '%B') + '/' + str(new_date.year))

@app.route('/cal/<month>/<year>/prev')
def prev_month(month, year):
    first = "01 %s %s" % (month, year)
    first_date = datetime.datetime.strptime(first, "%d %B %Y")
    new_date = add_months(first_date, -1)
    return redirect('/cal/' + datetime.datetime.strftime(new_date, '%B') + '/' + str(new_date.year))

@app.route('/')
def home():
    return redirect('/cal/november/2013')

if __name__ == "__main__":
    app.run()
