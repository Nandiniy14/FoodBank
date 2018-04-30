from flask import Flask,render_template,request,redirect,session
import psycopg2
from Services.database import DatabaseConnection
from Services.way import SendSMS
from datetime import datetime
import datetime
import pytz

tz = pytz.timezone('Asia/Kolkata')

class Donor():

    #Method to add food details by donors into the database
    def addFoodDetails(self):
        des = request.form['des']
        quant = request.form['quant']
        duration = request.form['duration']
        i = session['userid']

        conn = DatabaseConnection.databaseConnection()
        cur = conn.cursor(cursor_factory = psycopg2.extras.DictCursor)

        query="insert into foodinfo(id, description, foodquantity, duration) values(%s, %s, %s, %s) RETURNING foodid"
        cur.execute(query, (i, des, quant, duration))
        inline_return = cur.fetchone()
        cur.execute('commit')

        q="insert into food_unlock(fid,quantity) values(%s, %s)"
        cur.execute(q, (inline_return[0], quant))
        cur.execute('commit')

        q = "select phone,userid from userinfo where type = 'ngo'"
        cur.execute(q)
        phonelist = cur.fetchall()

        for num in phonelist:
            message = str(num['userid']) + str(inline_return[0])
            SendSMS.send(str(num['phone']), message)
        cur.close()
        conn.close()
        return render_template('donate.html')

    #Method to display all the donated food details by a particular donor.
    def getHistory(self):
        conn = DatabaseConnection.databaseConnection()
        cur = conn.cursor(cursor_factory = psycopg2.extras.DictCursor)
        uid = session['userid']
        query = "select fi.*, ui.name from foodinfo fi , userinfo ui\
        where fi.id = ui.userid and id= %s order by foodid desc"
        cur.execute(query, (uid, ))
        res = cur.fetchall()
        for i in res:
            i['created_timestamp'] = i['created_timestamp'].astimezone(tz)
            i['created_timestamp'] = i['created_timestamp'].strftime("%A, %d. %B %Y %I:%M%p")

        cur.close()
        conn.close()
        return render_template('history.html', food=res)

    #Method to display donated food details
    @classmethod
    def getFoodDetails(self):
        conn = DatabaseConnection.databaseConnection()
        cur = conn.cursor(cursor_factory = psycopg2.extras.DictCursor)

        uid = session['userid']

        query="select fi.*, ui.name from foodinfo fi, userinfo ui\
        where fi.id = ui.userid and id = %s order by foodid desc"
        cur.execute(query, (uid, ))
        res = cur.fetchall()

        query="select result.*, uii.name from (select fi.foodid, fl.* from foodinfo \
        fi, food_lock fl, userinfo ui where ui.userid = %s and ui.userid = fi.id \
        and fi.foodid = fl.fid) as result, userinfo uii where uii.userid = result.ngo_id \
        order by result.foodid DESC"
        cur.execute(query, (uid, ))
        lock = cur.fetchall()

        f = []
        j = 0
        x = 1
        count = cur.rowcount
        for i in res:
            i['created_timestamp'] = i['created_timestamp'].astimezone(tz)
            i['created_timestamp'] = i['created_timestamp'].strftime("%A, %d. %B %Y %I:%M%p")
            d = []
            d.append(i['created_timestamp'])
            d.append(i['description'])
            d.append(i['foodquantity'])
            d.append(i['duration'])
            c = 0
            while j < count and i['foodid']== lock[j]['fid']:
                d.append(lock[j])
                j = j + 1
                c = c + 1
            d.append(c)
            f.append(d)
        cur.close()
        conn.close()
        return render_template('timeline.html', lock = f)

    #Method to get the currently booked food details
    def getNotificationDetails(self):
        conn = DatabaseConnection.databaseConnection()
        cur = conn.cursor(cursor_factory = psycopg2.extras.DictCursor)
        uid = session['userid']
        query = "select result.*, uii.name from (select fi.*, fl.* from foodinfo fi, food_lock fl, userinfo ui \
        where ui.userid = %s and ui.userid = fi.id and fi.foodid = fl.fid and fl.status = 'not picked') as result, userinfo uii\
        where uii.userid = result.ngo_id ORDER BY result.created_timestamp DESC"
        cur.execute(query, (uid, ))
        res = cur.fetchall()

        for i in res:
            i['created_timestamp'] = i['created_timestamp'].astimezone(tz)
            i['created_timestamp'] = i['created_timestamp'].strftime("%A, %d. %B %Y %I:%M%p")
        cur.close()
        conn.close()
        return render_template('hotelnotification.html', food = res)
