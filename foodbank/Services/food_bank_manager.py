from flask import Flask,render_template,request,redirect,session
from Services.database_manager import DatabaseManager
from Models.user_info import UserInfo
import jsonpickle
import psycopg2
import psycopg2.extras

class FoodBankManager:

    def load_landing_page(self):
        return render_template('landing.html')

    def rendering_signup_page(self):
        return render_template('signup.html')

    def user_signup(self):
        conn = None
        conn = DatabaseManager.database_connection()
        cur=conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        content = request.get_json(silent=True)
        type(content)
        print(content)
        query="insert into userinfo (name,password,phone,email,location,type) \
        values(%s,%s,%s,%s,%s,%s) RETURNING type,email,location, \
        name,phone"
        cur.execute(query,(content['username'],content['password'],content['phone'],content['location'],content['type']))
        inline_return = cur.fetchone()
        cur.execute('commit')
        user_info = UserInfo()
        user_info.name = inline_return[3]
        user_info.type = inline_return[0]
        user_info.location = inline_return[2]
        user_info.phone = inline_return[4]
        user_info.email = inline_return[1]

        return jsonpickle.encode(user_info,unpicklable=False)

    def user_login(self):
        return render_template('home.html')
