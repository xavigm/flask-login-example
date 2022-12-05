from flask import Flask, render_template, request, redirect
from waitress import serve
import database
import os.path
import flask_login
import json



db_exists = os.path.exists('pythonsqlite.db')

if db_exists:
    print ("Database exists, skipping")
else:    
    database.create_new_connection(r"pythonsqlite.db")


app = Flask(__name__, static_folder='')
app.secret_key = 'super secret string'  # Change this!

############
############LOGIN PART
############

login_manager = flask_login.LoginManager()

login_manager.init_app(app)

class User(flask_login.UserMixin):
    pass


@login_manager.user_loader
def user_loader(email):
    users = json.loads(database.selectUser())

    if email not in users:
        return

    user = User()
    user.id = email
    return user


@login_manager.request_loader
def request_loader(request):
    email = request.form.get('email')
    users = json.loads(database.selectUser())

    if email not in users:
        return

    user = User()
    user.id = email
    return user

@app.route('/login', methods=['GET', 'POST'])
def login():
    users = json.loads(database.selectUser())

    if request.method == 'GET':
        templateData = {
        }

        return render_template('login.html', **templateData)
        

    email = request.form['email']
    if email in users and request.form['password'] == users[email]['password']:
        user = User()
        user.id = email
        flask_login.login_user(user)
        return redirect("/")

    templateData = {
        'msg' : '<p style="color:red">Bad login</p>'
        }

    return render_template('login.html', **templateData)

@app.route('/logout')
def logout():
    flask_login.logout_user()
    return redirect("/login")

@login_manager.unauthorized_handler
def unauthorized_handler():
    return redirect("/login")

############
############END OF LOGIN PART
############

@app.route('/')
@flask_login.login_required
def index():

    templateData = {
        'msg': 'Login Succeded',
    }

    return render_template('index.html', **templateData)

app.run() ##Replaced with below code to run it using waitress
#serve(app, host='127.0.0.1', port=5000)  
    