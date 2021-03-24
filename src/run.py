from flask import Flask, render_template, redirect, url_for, request, session, flash
from flask_mysqldb import MySQL
import random
import MySQLdb.cursors
import re
from functools import wraps
import codecs

app = Flask(__name__)

app.secret_key = str(random.random()) 

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'pythonlogin'

mysql = MySQL(app)

#Create a login
@app.route('/', methods = ['GET', 'POST'])
def login():
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username = request.form['username']
        password = request.form['password']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM accounts WHERE username = %s AND password = %s', (username, password,))
        account = cursor.fetchone()
        if account:
            session['loggedin'] = True
            session['id'] = account['id']
            session['username'] = account['username']
            return redirect('settings')
        else:
            msg = 'Incorrect credentials!'
    return render_template('login.html', msg=msg)

#Create a register
@app.route('/register', methods=['GET', 'POST'])
def register():
    if 'loggedin' in session:
        if session['username'] == 'admin':
            msg = ''
            if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form:
                username = request.form['username']
                password = request.form['password']
                email = request.form['email']
                cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
                cursor.execute('SELECT * FROM accounts WHERE username = %s', (username,))
                account = cursor.fetchone()
                if account:
                    msg = 'Account already exists!'
                elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
                    msg = 'Invalid E-mail adress!'
                elif not re.match(r'[A-Za-z0-9]+', username):
                    msg = 'Username must contain only characters and numbers!'
                elif not username or not password or not email:
                    msg = 'Please completely fill out the form!'
                else:
                    cursor.execute('INSERT INTO accounts VALUES (NULL, %s, %s, %s)', (username, password, email,))
                    mysql.connection.commit()
                    msg = 'You have successfully registered!'
            elif request.method == 'POST':
                msg = 'Please completely fill out the form!'
            return render_template('register.html', msg=msg)
        else:
            return redirect(url_for('settings'))
    else:
        return redirect(url_for('login'))

#Settings page
@app.route('/settings', methods=['GET','POST'])
def settings():
    if 'loggedin' in session:
        if session['username']=='admin':
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
            return render_template('settingsadmin.html', username=session['username'])
        else:
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
            return render_template('settings.html', username=session['username'])    
    else:
        return redirect(url_for('login'))

#Allow to logout
@app.route('/logout')
def logout():
    session.pop('loggedin', None)
    session.pop('id', None)
    session.pop('username', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)


