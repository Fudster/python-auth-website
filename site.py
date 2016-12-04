from flask import Flask, request, session, g, redirect, url_for, abort, \
     render_template, flash, send_from_directory, Response
from flask_login import LoginManager, UserMixin, \
                                login_required, login_user, logout_user 
import sqlite3
import werkzeug.security

app = Flask(__name__, static_url_path='')
# config
app.config.update(
    DEBUG = True,
    SECRET_KEY = 'GMRKMGKRMG'
)

def app_start(host,port):
    app.run(host=host, port=port)



# flask-login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)

##A simple way to access the DB
def query(sql, params=None):
    conn = sqlite3.connect('site.db')
    cursor = conn.cursor()
    cursor.execute(sql, params)
    data = cursor.fetchall()
    cursor.close()
    return data

def check_email(emailx):
    conn = sqlite3.connect('site.db')
    cursor = conn.cursor()
    sql = "Select email from users where email=?"
    cursor.execute(sql, [emailx])
    data = cursor.fetchone()
    cursor.close()
    if data and data[0]:
        return True
    else:
        return False 

def check_username(usernamex):
    data =  query("Select username from users where username=?",[usernamex])
    return data

def check_password(emailx, passwordx):
    data =  query("Select password from users where email=?",[emailx])
    result = werkzeug.security.check_password_hash(data[0],passwordx)
    return result
        
def get_id(emailx):
    conn = sqlite3.connect('site.db')
    cursor = conn.cursor()
    sql = "Select id from users where email=?"
    cursor.execute(sql, [emailx])
    data = cursor.fetchone()
    cursor.close()
    return data[0]

def create_account(userx,passwordx,emailx):
    if not check_email(emailx) and not check_username(userx):
        hashpw = werkzeug.security.generate_password_hash(passwordx)
        conn = sqlite3.connect('site.db')
        cursor = conn.cursor()
        cursor.execute("INSERT INTO users (username, password, email) VALUES(?, ?, ?)",
        (userx, hashpw, emailx))
        conn.commit()
        cursor.close()
        return "Account created!"
    else:
        return "User or email already exists!"
 

@app.route("/register")
def show_register_form():
    return app.send_static_file('register.html') 

@app.route("/login/")
def show_login():
    return app.send_static_file('login.html') 


@app.route("/account/register/process/", methods=["POST"])
def register_account():
        username = request.form.get("username")
        email = request.form.get("email")
        password = request.form.get("password")
        confrim_password = request.form.get("confirm-password")
        if password == confrim_password:
           create_account(username,password,email)
           return "account created!"
        else: 
            return "Password does not match!"
@app.route("/account/login/process/", methods=["POST"])            
def login_account():
    email = request.form.get("email")
    password = request.form.get("password")
    if check_password(email,password) == True:
        username = get_username(email)
        return "Welcome " + username
    else:
        return "Email or password Incorrect!"
@app.route('/dashboard/')
@login_required
def home():
    return Response("Hello World!")

@app.route('/check/<slug>')
def test_function(slug):
    return get_id(slug)

app_start('0.0.0.0',6060)
