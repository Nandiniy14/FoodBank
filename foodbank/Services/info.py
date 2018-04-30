from flask import Flask,render_template,request,redirect,session
import psycopg2
from Services.database import DatabaseConnection

from datetime import datetime
import datetime
import pytz

tz = pytz.timezone('Asia/Kolkata')

class Information():

    #Method for Signup
    def addDetails(self):
        try:
            conn = DatabaseConnection.databaseConnection()
            cur = conn.cursor(cursor_factory = psycopg2.extras.DictCursor)
            name = request.form['username']
            password = request.form['password']
            phone = request.form['phone']
            location = request.form['location']
            user_type = request.form['type']
            query = "insert into userinfo (name, password, phone, location, type)\
            values(%s, %s, %s, %s, %s) RETURNING userid"
            cur.execute(query, (name, password, phone, location, user_type))
            inline_return = cur.fetchone()
            cur.execute('commit')
            a = inline_return[0]
            cur.close()
            conn.close()
            return render_template('login.html', message = "successfull")
        except Exception :
            return render_template('signup.html', message = "User already Exists")
        finally:
            cur.close()
            conn.close()

    #Method for login
    def checkUserDetails(self):
        phone = request.form['phone']
        password = request.form['password']

        conn = DatabaseConnection.databaseConnection()
        cur = conn.cursor(cursor_factory = psycopg2.extras.DictCursor)
        query="select userid, name, type, password from userinfo where phone = %s"
        cur.execute(query, (phone ,))
        res = cur.fetchone()
        if res and (password == res['password']):
            session['userid'] = res[0]
            session['username'] = res[1]
            session['usertype'] = res[2]
            query = "select result.fid, result.foodquantity, result.created_timestamp,\
            result.food_quantity, result.foodquantity, uii.name from \
            (select fi.*, fl.* as hname from foodinfo fi, food_lock fl, userinfo ui \
            where ui.userid = %s and ui.userid = fi.id and fi.foodid = fl.fid) as \
            result, userinfo uii where uii.userid = result.ngo_id ORDER BY \
            result.fid DESC"
            uid = int(session['userid'])
            print(uid)
            cur.execute(query, (uid, ))
            r = cur.fetchall()
            for i in r:
                i['created_timestamp'] = i['created_timestamp'].astimezone(tz)
                i['created_timestamp'] = i['created_timestamp'].strftime("%Y-%d-%m")
                print(i['created_timestamp'])
            session['list'] = r
            cur.close()
            conn.close()
            if res and res['type'] == "hotel":
                return redirect('/donate')
            elif res and res['type'] == "ngo":
                return redirect('/ngo_timeline')
            else:
                return render_template('login.html', message = "Not successfull")

        else:
            cur.close()
            conn.close()
            return render_template('login.html', message = "Not successfull")

    #Method to update the status whether the food is picked or not
    def update_Status(self):
        lock_id = int(request.form['lock_id'])

        conn = DatabaseConnection.databaseConnection()
        cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        query = "update food_lock set status = 'picked' where lock_id = %s"
        cur.execute(query, (lock_id, ))
        cur.execute('commit')
        cur.close()
        conn.close()
        if session['usertype'] == "ngo":
            return redirect('/lock')
        else:
            return redirect('/notification')

    def details(self):

        cur.close()
        conn.close()
        return res
