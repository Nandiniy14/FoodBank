from flask import Flask,render_template,request,redirect,session
from Services.food_bank_manager import FoodBankManager
app=Flask(__name__)
@app.route('/',methods=['GET'])
def get_load_landing_page():
    return FoodBankManager().load_landing_page()

@app.route('/signup',methods=['GET'])
def get_user_page():
    if request.method == "GET":
        return FoodBankManager().rendering_signup_page()
    else:


@app.route('/signup',methods=['POST'])
def user_register():
    return FoodBankManager().user_signup()


@app.route('/home',methods=['GET'])
def users_login():
    return FoodBankManager().user_login()

if __name__ == '__main__':
    app.run()
