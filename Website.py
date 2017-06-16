from flask import Flask
from flask import render_template
from flask import request
from flask import abort
from dbsecurity.dbconn import DbConnection
import os
import datetime
instance_db = DbConnection("petfeeder_db")

app = Flask(__name__)

def getDbInfo(sql, name_field_one, name_field_two, params = {}):
    result = instance_db.query(sql, params, dictionary=True)
    time_list = []
    value_list = []

    for item in range(0, len(result)):
        record = result[item]
        time_list.append(record[name_field_one])
        value_list.append(record[name_field_two])

    return [time_list, value_list]


@app.route('/')
def live():
    sql = ('SELECT millilitres_left, timestamp FROM petfeeder_db.tbldrinklog where date(timestamp) = current_date();')
    result = getDbInfo(sql, 'timestamp', 'millilitres_left')
    drink_time_list = result[0]
    drink_value_list = result[1]


    sql2 = (' SELECT grams_left, timestamp FROM petfeeder_db.tblfoodlog where date(timestamp) = current_date();')
    result2 = getDbInfo(sql2, 'timestamp', 'grams_left')
    food_time_list = result2[0]
    food_value_list = result2[1]


    sql3 = ('SELECT percentage_left, timestamp FROM petfeeder_db.tblprovision where date(timestamp) = current_date();')
    result3 = getDbInfo(sql3, 'timestamp', 'percentage_left')
    provision_time_list = result2[0]
    provision_value_list = result2[1]

    return render_template('index.html', drink_time_list=drink_time_list, drink_value_list=drink_value_list ,food_time_list=food_time_list, food_value_list=food_value_list, provision_time_list=provision_time_list, provision_value_list=provision_value_list)


@app.route('/history', methods=['GET'])
def history_get():
    from_date = datetime.datetime.now().date()
    until_date = datetime.datetime.now().date()

    sql = ('SELECT millilitres_left, timestamp FROM petfeeder_db.tbldrinklog where date(timestamp) = current_date();')
    result = getDbInfo(sql, 'timestamp', 'millilitres_left')
    drink_time_list = result[0]
    drink_value_list = result[1]


    sql2 = (' SELECT grams_left, timestamp FROM petfeeder_db.tblfoodlog where date(timestamp) = current_date();')
    result2 = getDbInfo(sql2, 'timestamp', 'grams_left')
    food_time_list = result2[0]
    food_value_list = result2[1]


    sql3 = ('SELECT percentage_left, timestamp FROM petfeeder_db.tblprovision where date(timestamp) = current_date();')
    result3 = getDbInfo(sql3, 'timestamp', 'percentage_left')
    provision_time_list = result2[0]
    provision_value_list = result2[1]

    return render_template('history.html', drink_time_list=drink_time_list, drink_value_list=drink_value_list ,food_time_list=food_time_list, food_value_list=food_value_list, provision_time_list=provision_time_list, provision_value_list=provision_value_list, from_date=from_date, until_date=until_date)


@app.route('/history', methods=['POST'])
def history_post():
    try:
        from_date_string = request.form['from_date']
        until_date_string = request.form['until_date']

        from_date = datetime.datetime.strptime(from_date_string, "%Y-%m-%d")
        until_date = datetime.datetime.strptime(until_date_string, "%Y-%m-%d")

        params = {
            'from_date': from_date,
            'until_date': until_date
        }

        sql = (
        'SELECT millilitres_left, timestamp FROM petfeeder_db.tbldrinklog where date(timestamp) between %(from_date)s and %(until_date)s;')


        result = getDbInfo(sql, 'timestamp', 'millilitres_left', params)
        drink_time_list = result[0]
        drink_value_list = result[1]

        print("stmt 2 bereikt")

        sql2 = (' SELECT grams_left, timestamp FROM petfeeder_db.tblfoodlog where date(timestamp) between %(from_date)s and %(until_date)s;')
        result2 = getDbInfo(sql2, 'timestamp', 'grams_left', params)
        food_time_list = result2[0]
        food_value_list = result2[1]

        sql3 = (
        'SELECT percentage_left, timestamp FROM petfeeder_db.tblprovision where date(timestamp) between %(from_date)s and %(until_date)s;')
        result3 = getDbInfo(sql3, 'timestamp', 'percentage_left', params)
        provision_time_list = result2[0]
        provision_value_list = result2[1]

        return render_template('history.html', drink_time_list=drink_time_list, drink_value_list=drink_value_list,
                               food_time_list=food_time_list, food_value_list=food_value_list,
                               provision_time_list=provision_time_list, provision_value_list=provision_value_list, from_date=from_date_string, until_date=until_date_string)
    except:
        abort(400)


@app.route('/settings', methods=['GET'])
def settings_get():
    try:
        instance_db = DbConnection('petfeeder_db')
        sql = ('select led_alarm_enabeld, sound_alarm_enabled, email_alarm_enabled, sms_alarm_enabled, food_alarm_enabled, drink_alarm_enabled, provision_alarm_enabled, food_alarm_threshold, drink_alarm_threshold, provision_alarm_threshold, alarm_interval_hours, email, phone_number from tblsettings;')
        result = instance_db.query(sql, dictionary=True)
        result = result[0]
        print(result)
        return render_template('settings.html', result=result)
    except:
        abort(400)

@app.route('/settings', methods=['POST'])
def settings_post():
    return render_template('settings.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.errorhandler(400)
def throw_400(error):
    return render_template('error_pages/400.html', error=error)

@app.errorhandler(401)
def throw_401(error):
    return render_template('error_pages/401.html', error=error)


@app.errorhandler(404)
def throw_404(error):
    return render_template('error_pages/404.html', error=error)

if __name__ == '__main__':
    # check omgevingsvariabele voor poort of neem 8080 als standaarc
    port = int(os.environ.get("PORT", 8080))
    host = "169.254.10.111" #luistert naar alle IP's i.p.v. enkel 127.0.0.1
    app.run(host=host, port=port, debug=True)