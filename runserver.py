from flask import Flask,render_template, redirect, url_for, request,json,session
from os import environ
from flask_sqlalchemy import SQLAlchemy
import bcrypt
from flaskext.mysql import MySQL
from werkzeug.security import generate_password_hash, check_password_hash

mysql = MySQL()

app = Flask(__name__)

app.config['MYSQL_DATABASE_HOST'] = 'localhost'
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = ''
app.config['MYSQL_DATABASE_DB'] = 'mcaproject'
mysql.init_app(app)
conn = mysql.connect()
cur = conn.cursor()

class ServerError(Exception):pass


@app.route('/', methods=['GET', 'POST'])
def index(): 
    return render_template('index.html')   

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == "POST":
        details = request.form
        username = details['username']
        cur.execute("SELECT COUNT(1) FROM signup WHERE name = (%s)",(username))                  
        if not cur.fetchone()[0]:
                raise ServerError('Invalid username')
        pwd = details['password']
        pd = 'gsb'
        has = generate_password_hash(pd)
        print(pwd)
        cur.execute("SELECT pwd FROM signup WHERE name = (%s)",(username))     
        data = cur.fetchall()   
        print(data[0])              
        if check_password_hash(pd,data[0]):
                return render_template('signup.html')
        raise ServerError('Invalid password')        
        # cur.execute("insert into mcaproject.login_credentials(id,username,pwd) VALUES (%s, %s, %s)",(3,username,_hashed_password))
        # conn.commit()       
    return render_template('login.html')


@app.route('/signup', methods=['GET', 'POST'])  
def sign_up() : 
    if request.method == "POST": 
        signup = request.form
        name = signup['name']                        
        number = signup['number']
        pwd = signup['pwd']
        _hashed_password = generate_password_hash(pwd,bcrypt)
        confirmpwd = signup['confirmpwd'].encode('utf-8')
        # confirm_hashed_password = generate_password_hash(confirmpwd)
        if pwd == confirmpwd:
            conn = mysql.connect()
            cur = conn.cursor()
            cur.execute("insert into mcaproject.signup(name,number,pwd) VALUES (%s, %s, %s)",(name,number,_hashed_password))
            cur.fetchall()
            conn.commit()
        else:
            return "password and confirm password didn't matched!"   
    else:
        return render_template('signup.html')        
    return render_template('login.html')

if __name__ == '__main__':    
    app.run(debug = True)
