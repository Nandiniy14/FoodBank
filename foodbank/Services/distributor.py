from flask import Flask,render_template,request,redirect,session
import psycopg2
from Services.database import DatabaseConnection
from datetime import datetime
import datetime
import pytz

tz = pytz.timezone('Asia/Kolkata')

class Distributor():

    #Method to display the food details posted by various donors
    def getFoodUnlockDetails(self):
        conn = DatabaseConnection.databaseConnection()
        cur=conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        query="select fi.*,fu.quantity,ui.location,ui.name from foodinfo fi, food_unlock fu,\
        userinfo ui where fu.quantity > 0 and fu.fid = fi.foodid and fi.id = ui.userid \
        and now() < (fi.created_timestamp + ( duration * interval '1 hour'))"
        cur.execute(query)
        res = cur.fetchall()
        for i in res:
            i['created_timestamp'] = i['created_timestamp'].astimezone(tz)
            i['created_timestamp'] = i['created_timestamp'].strftime("%A, %d. %B %Y %I:%M%p")
            i['foodid'] = str(i['foodid'])
        return render_template('ngo_timeline.html', food=res)

    #Method that provides distributor to lock certain amount of food
    def addFoodlockDetails(self):
        foodid = int(request.form['foodid'])
        quant = int(request.form['quant'])
        cur_quant = int(request.form['cquant'])
        timelimit = int(request.form['ngodur'])
        ngo_id = session['userid']

        conn = DatabaseConnection.databaseConnection()
        cur=conn.cursor(cursor_factory = psycopg2.extras.DictCursor)

        query="insert into food_lock(fid, food_quantity, timelimit, ngo_id) values(%s, %s, %s, %s)"
        cur.execute(query, (foodid, quant, timelimit, ngo_id))
        cur.execute('commit')

        dif = cur_quant - quant
        q = "update food_unlock set quantity = %s where fid = %s"
        cur.execute(q, (dif, foodid))
        rows = cur.rowcount
        cur.execute('commit')
        cur.close()
        conn.close()
        if rows:
            return redirect('/lock')
        else:
            return redirect('/ngo_timeline')

    #Method to release the amount of food locked by distributor
    def addFoodunlockDetails(self):
        foodid = int(request.form['foodid'])
        quant = int(request.form['quant'])
        cur_quant = int(request.form['cquant'])
        lock_id = int(request.form['lock_id'])

        conn = DatabaseConnection.databaseConnection()
        cur=conn.cursor(cursor_factory = psycopg2.extras.DictCursor)

        query="update food_unlock set quantity = %s where fid = %s"
        dif = cur_quant + quant
        cur.execute(query, (dif, foodid))
        rows = cur.rowcount
        cur.execute('commit')
        query="update food_lock set status='obsolete' where lock_id = %s"
        cur.execute(query, (lock_id, ))
        res = cur.rowcount
        cur.execute('commit')
        cur.close()
        conn.close()
        if res:
            return redirect('/lock')
        else:
            return redirect('/ngo_timeline')

    #Method that provides distributor to get the details of food locked
    def getFoodlockDetails(self):

        conn = DatabaseConnection.databaseConnection()
        cur = conn.cursor(cursor_factory = psycopg2.extras.DictCursor)
        ngo_id = session['userid']
        print(ngo_id)
        query = "select fu.lock_id, fu.timelimit, ui.name, fi.*, fu.food_quantity, \
        ful.quantity, ui.location \
        from foodinfo fi,food_unlock ful, food_lock fu, userinfo ui \
        where fu.fid = fi.foodid and ful.fid = fi.foodid and fi.id = ui.userid and \
        fu.ngo_id = %s \
        and fu.status = 'not picked'"
        cur.execute(query, (ngo_id, ))
        res=cur.fetchall()
        for i in res:
            i['created_timestamp'] = i['created_timestamp'].astimezone(tz)
            i['created_timestamp'] = i['created_timestamp'].strftime("%A, %d. %B %Y %I:%M%p")
        return render_template('handout.html', food = res)
