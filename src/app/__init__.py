from flask import Flask, render_template, redirect, url_for, request, session, flash, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from flask_login import login_required, current_user, LoginManager, login_user, UserMixin, logout_user
from werkzeug.security import generate_password_hash, check_password_hash

import random
import MySQLdb.cursors
import re
from functools import wraps
import codecs

app = Flask(__name__)

app.config['SECRET_KEY'] = str(random.random()) 
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'

db = SQLAlchemy(app)

class users(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(100), unique = True)
    password = db.Column(db.String(100))  
    email = db.Column(db.String(200), unique = True)

db.create_all()

db.init_app(app)
login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    # since the user_id is just the primary key of our user table, use it in the query for the user
    return users.query.get(int(user_id))

if db.session.query(users).filter_by(username='admin').count() < 1:
    admin = users(username='admin', password=generate_password_hash('admin', method='sha256'), email='admin@admin.nl')
    db.session.add(admin)
    db.session.commit()
# some headers
@app.after_request
def add_header(response):
    response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
    response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '0'
    return response

#Create a login
@app.route('/')
def login():
    return render_template('login.html')

@app.route('/', methods = ['GET', 'POST'])  
def login_auth():
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username = request.form.get('username')
        password = request.form.get('password')
        remember = True
        account = users.query.filter_by(username=username).first()

        if account and check_password_hash(account.password, password):
            login_user(account, remember=remember)
            return redirect(url_for('settings'))
        elif not account:
            flash('Account does not exist!')
            return redirect(url_for('login'))
        else:
            flash('Incorrect credentials!')
            return redirect(url_for('login'))

#Create a register
@app.route('/register')
@login_required
def register():
    if current_user.username == 'admin':
        return render_template('register.html')
    else:
        return redirect(url_for('settings'))

@app.route('/register', methods=['GET', 'POST'])
def register_create():
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form:
        username = request.form.get('username')
        password = request.form.get('password')
        email = request.form.get('email')
        account = users.query.filter_by(username=username).first()
        if account:
            flash('Account already exists!')
            return redirect(url_for('register'))
        elif not re.match(r'[A-Za-z0-9]+', username):
            flash('Username must contain only characters and numbers!')
            return redirect(url_for('register'))
        else:
            new_user = users(email=email, username=username, password=generate_password_hash(password, method='sha256'))
            db.session.add(new_user)
            db.session.commit()
            flash('You have successfully registered!')
            return redirect(url_for('register'))

#Settings page
@app.route('/settings')
@login_required
def settings():
    return render_template('settings.html', username=current_user.username)

@app.route('/settings', methods=['GET','POST'])
def settings_send():
    if request.method == 'POST':
        csvfile=request.form['CSV_file']
        width=request.form['width']
        height=request.form['height']
        T_projection=request.form['T_projection']
        N_samplepoints=request.form['N_samplepoints']
        with codecs.open("settings.conf", "w", "utf-8-sig") as f:
            f.write('DISPLAY=:0\n')
            f.write('GLSL_APP_VERT="/usr/bin/shader/basic.vert"\n')
            f.write('GLSL_APP_FRAG="/usr/bin/shader/basic.frag"\n')
            f.write('WIDTH='+width+'\n')
            f.write('HEIGHT='+height+'\n')
            f.write('T_PROJECTION='+T_projection+'\n')
            f.write('N_SAMPLEPOINTS='+N_samplepoints+'\n')
        f.close()

@app.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    user = current_user.username
    passw = current_user.password
    mail = current_user.email
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        email = request.form.get('email')
        account = users.query.filter_by(username=user).first()
        account.username = username
        account.password = password
        account.email = email
        db.session.commit()
    return render_template('profile.html', username=user, email=mail)
#Allow to logout
@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

# video stream
@app.route('/video')
@login_required
def show_video():
    return render_template('hlsvideo.html')

@app.route('/video/<string:file_name>')
def stream(file_name):
    video_dir = './video'
    return send_from_directory(directory=video_dir, filename=file_name)