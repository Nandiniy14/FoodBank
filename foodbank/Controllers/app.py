from flask import Flask, abort, render_template, request, redirect, session, url_for
from Services.info import Information
from Services.donor import Donor
from Services.distributor import Distributor
# from datetime import datetime
# import datetime
# import psycopg2
# import pytz
#
# tz = pytz.timezone('Asia/Kolkata')
app = Flask(__name__)
print(app)
app.secret_key = 'any random string'

#Authorizing the user and restricting him from entering to the pages directly without logging in.
@app.before_request
def request_authorization():
    if 'username' not in session and request.endpoint not in  ['loadLandingPage', 'landingpage', 'login', 'signup']:
        return redirect('/login')

#The first page user can see
@app.route('/')
def loadLandingPage():
    return render_template('landing.html')

@app.route('/pie', methods = ['GET', 'POST'])
def loadLanding():
    color_vals = [ "#F7464A", "#46BFBD","#FDB45C","#FEDCBA","#ABCDEF", "#DDDDDD",
    "#ABCABC", "#4169E1","#C71585", "#FF4500", "#FEDCBA", "#46BFBD"]
    labels=[]
    values=[]
    foodid=[]
    if request.method == "GET":
        return render_template('chart.html',set=None)
    c = 0
    p = 1
    date = request.form['date']
    print(date)
    print(session['list'])
    for i in session['list']:
        print(date,i[2])
        if date == i[2]:
            labels.append(i[5])
            values.append(i[3])
            p = p + 1
    print(p)
    if p == 1:
        return render_template('chart.html',set="no",date=date)

    colors = color_vals[0:p]
    return render_template('chart.html', date=date, set=zip(values, labels, colors))


#Adding the user details into the database
@app.route('/signup', methods = ['GET', 'POST'])
def signup():
    if request.method == "GET":
        return render_template('signup.html')
    else:
        return Information().addDetails()

#Validate the user while logging in
@app.route('/login', methods = ['GET', 'POST'])
def login():
    if request.method == "GET":
        return render_template('login.html')
    else:
        return Information().checkUserDetails()

#Method for logout
@app.route('/logout', methods=['GET'])
def logout():
    session.pop('username', None)
    session.pop('list', None)
    return render_template('landing.html')

#Method to add food details by donors into the database
@app.route('/donate', methods=['GET', 'POST'])
def donateFood():
    if request.method == "GET":
        return render_template('donate.html')
    else:
        return Donor().addFoodDetails()

#Method to display donated food details
@app.route('/timeline', methods=['GET'])
def getFoodInfo():
    return Donor().getFoodDetails()

#Method to get the currently booked food details
@app.route('/notification', methods=['GET'])
def getNotificationInfo():
    return Donor().getNotificationDetails()

#Method to display all the donated food details by a particular donor.
@app.route('/history', methods=['GET'])
def getHistoryInfo():
    return Donor().getHistory()

#Method to update the status whether the food is picked or not
@app.route('/status', methods=['POST'])
def updateStatus():
    return Information().update_Status()

#Method to display the food details posted by various donors
@app.route('/ngo_timeline', methods=['GET'])
def getFoodUnlockInfo():
    return Distributor().getFoodUnlockDetails()

#Method that provides distributor to lock certain amount of food
@app.route('/lock', methods=['GET', 'POST'])
def lockInfo():
    if request.method == "GET":
        return Distributor().getFoodlockDetails()
    else:
        return Distributor().addFoodlockDetails()

#Method to release the amount of food locked by distributor
@app.route('/unlock', methods=['POST'])
def food_unlock():
    return Distributor().addFoodunlockDetails()

@app.route('/landing', methods=['GET'])
def landingpage():
        return render_template('landing.html')


app.run(port=5003)
