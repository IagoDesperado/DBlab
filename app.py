import pymysql
import os 
from flask import Flask,render_template, request, url_for, flash, redirect,session
from flask_mysqldb import MySQL
from werkzeug.exceptions import abort
#from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your secret key'

def get_db_connection():
 db = pymysql.connect(db = "testdb",user = "iago_desperado", password = "Yq9ZkNMkd7!3yNx", host = "localhost")
 return db

def get_book(name):
  conn = pymysql.connect(db = "testdb",user = "iago_desperado", password = "Yq9ZkNMkd7!3yNx", host = "localhost")
  cursor = conn.cursor()
  sql = "SELECT title,num_of_copies FROM copies_avail WHERE copies_avail.sch_name = '%s' "%name
  cursor.execute(sql)
  book = cursor.fetchall()
  conn.close()
  return book

@app.route('/home')
def index():
 
 conn = pymysql.connect(db = "testdb",user = "iago_desperado", password = "Yq9ZkNMkd7!3yNx", host = "localhost")
 cursor = conn.cursor()
 sql = "SELECT * FROM school"
 cursor.execute(sql)
 school = cursor.fetchall()
 sql2 = " SELECT f_name,l_name FROM principle"# WHERE principle.sch_name = '%s' " %name
 cursor.execute(sql2)
 principle = cursor.fetchall()
 print(principle)
 conn.close()
 user_check = session['loggedin']
 return render_template("index.html",post = school,principle = principle,user_check = user_check)

@app.route('/<name>')
def sch(name):
 if (session['loggedin'] == False):
   flash("You must log in to see this school's library.")
   return redirect(url_for('index'))
 conn = pymysql.connect(db = "testdb",user = "iago_desperado", password = "Yq9ZkNMkd7!3yNx", host = "localhost")
 cursor = conn.cursor()
 sql2 = " SELECT f_name,l_name FROM principle WHERE principle.sch_name = '%s' " %name
 cursor.execute(sql2)
 principal = cursor.fetchone()
 sql3 = " SELECT f_name,l_name FROM lib_admin WHERE lib_admin.sch_name = '%s' " %name
 cursor.execute(sql3)
 lib_admin = cursor.fetchone()
 conn.close()
 sch_name = name
 book = get_book(name)
 return render_template('school.html',book = book,principal = principal, lib_admin = lib_admin,sch_name = sch_name)

@app.route('/<name>/<book_title>')
def get_book_info(name,book_title):
 if (session['loggedin'] == False):
   flash("You must log in to see this school's library.")
   return redirect(url_for('index'))
 conn = pymysql.connect(db = "testdb",user = "iago_desperado", password = "Yq9ZkNMkd7!3yNx", host = "localhost")
 cursor = conn.cursor()
 sql = "SELECT* FROM book WHERE book.title = '%s'"% book_title
 cursor.execute(sql)
 book_info = cursor.fetchone()
 sql2 = "SELECT ISBN,language FROM book_ISBN WHERE book_ISBN.title = '%s'"% book_title
 cursor.execute(sql2)
 book_ISBN = cursor.fetchall()
 sql3 = "SELECT f_name, l_name FROM writer WHERE writer.title = '%s'"% book_title
 cursor.execute(sql3)
 writer = cursor.fetchone()
 sql4 ="SELECT * FROM belong_to_genre WHERE belong_to_genre.title = '%s'"% book_title
 cursor.execute(sql4)
 genre = cursor.fetchall()
 conn.close()
 return render_template('book_info.html',book_info = book_info,book_ISBN = book_ISBN,writer = writer,genre = genre)
  
@app.route('/review',methods = ['GET', 'POST'])
def write_review():
  if (request.method == 'POST'):
    review = request.form['review']
    if (review == ''):
     flash("You didn't write anything.") 
    else:
     conn = pymysql.connect(db = "testdb",user = "iago_desperado", password = "Yq9ZkNMkd7!3yNx", host = "localhost")
     cursor = conn.cursor()
     sql = "INSERT INTO review( content ) VALUES('%s');"%review
     try:
      cursor.execute(sql)
      conn.commit()
     except:
       conn.rollback() 
     conn.close() 
  return render_template('review.html')

@app.route('/sign up',methods = ['GET', 'POST'])
def sign_up():
  conn = pymysql.connect(db = "testdb",user = "iago_desperado", password = "Yq9ZkNMkd7!3yNx", host = "localhost")
  cursor = conn.cursor()
  if request.method == 'POST':
    username = request.form.get('username')
    password1 = request.form.get('password1')
    password2 = request.form.get('password2')
    flag = request.form.get('dropdown')
    email = request.form.get('email')    
    first_name = request.form.get('first_name')
    last_name = request.form.get('last_name')
    age = request.form.get('age') 
     
    #sql = "SELECT username FROM user where user.username = %s"% username
    #cursor.execute(sql)
    #username_check = cursor.fetchone()
 
    if (len(username) < 1):
      flash("Your username must be at least 1 character long",category = 'error')
    elif(password1 != password2):
      flash("Passwords don't match.",category = 'error')
    elif(len(email) < 3):
      flash("Your email must be at least 3 characters long.",category = 'error')
    elif((len(first_name) < 1) or (len(last_name) < 1)):
      flash("Your name must be at least 1 character long.",category = 'error')
    else:
     sql2 = "INSERT INTO user(username,password,flag,email,first_name,last_name,age)\
            VALUES('%s','%s','%s','%s','%s','%s','%s');"%(username,password1,flag,email,first_name,last_name,age)
     cursor.execute(sql2)
     test = cursor.fetchall()
     print(test)
     try:
      conn.commit()
     except:
       conn.rollback()
     conn.close()  
     flash('Account created!', category='success')
     return redirect(url_for('index'))            
  
  return render_template("sign_up.html")

@app.route("/", methods = ['GET','POST'])
def login():
  if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
    username = request.form['username']
    password = request.form['password']
    print(username,password)
    conn = pymysql.connect(db = "testdb",user = "iago_desperado", password = "Yq9ZkNMkd7!3yNx", host = "localhost")
    cursor = conn.cursor()
    sql = "SELECT * FROM user WHERE username ='%s' AND password = '%s';"%(username,password)
    cursor.execute(sql)
    account = cursor.fetchone()
    if account:
      session['loggedin'] = True
      session['username'] = account[0]
      session['flag'] = account[2]
      print(session['loggedin'],session['username'])
      flash("log in succesful.", category = 'success')
      return redirect(url_for('index'))  
    else:
      session['loggedin'] = False
      flash("Invalid credentials.", category = "error")
  return render_template("login.html")    

@app.route("/logout")
def log_out():
  if session['loggedin']:
   session['loggedin'] = False
   session['flag'] = None
   session['username'] = None
   #session.pop('loggein',None)
   #session.pop('username',None)
   flash("Logged out", category = 'succesess')
   return redirect(url_for('index'))
  else:
    flash("You are not logged in.")
    return redirect(url_for('index'))

@app.route('/user info',methods = ['GET', 'POST'])
def user_info():
 if not session['loggedin']:
   flash("You're not currently logged in")
   return redirect(url_for('index'))
 else:
   conn = pymysql.connect(db = "testdb",user = "iago_desperado", password = "Yq9ZkNMkd7!3yNx", host = "localhost")
   cursor = conn.cursor()
   sql = "SELECT* FROM user WHERE username = '%s'"% session['username']
   cursor.execute(sql)
   user_info = cursor.fetchone()
   if(request.form.get('new username')):
    new_username = request.form.get('new username')
    sql = "UPDATE user \
    SET username = '%s' WHERE username = '%s'"%(new_username,session['username'])
    cursor.execute(sql)
    try:
     conn.commit()
     session['username'] = new_username
    except:
     conn.rollback()     
   return render_template('user_info.html', user_info = user_info)

@app.route('/edit profile', methods = ['GET','POST'])
def edit_profile():
  conn = pymysql.connect(db = "testdb",user = "iago_desperado", password = "Yq9ZkNMkd7!3yNx", host = "localhost")
  cursor = conn.cursor()
  if(request.form.get('new username')):
   new_username = request.form.get('new username')
   if(len(new_username) < 1):
     flash("New username must be at least 1 character long.",category = 'error')
     return redirect(url_for("edit_username"))
   sql = "UPDATE user \
    SET username = '%s' WHERE username = '%s'"%(new_username,session['username'])
   cursor.execute(sql)
   try:
    conn.commit()
    session['username'] = new_username
    flash("Username changed succesfully.",category = 'success')
   except:
    conn.rollback()
  if(request.form.get('new password')):
    new_password = request.form.get('new password')
    if(len(new_password) < 5):
      flash("Your password must be at least 5 characters long.", category = 'error')
      return redirect(url_for('edit_profile'))
    sql = "UPDATE user \
    SET password = '%s' WHERE username = '%s'"%(new_password,session['username'])
    cursor.execute(sql)
    try:
     conn.commit()
     flash("Password changed succesfully.",category = 'success')
    except:
     conn.rollback()  
  if(request.form.get('new email')):
    new_email = request.form.get('new email')
    if(len(new_email) < 3):
      flash("Your email must be at least 3 characters long.", category = 'error')
      return redirect(url_for('edit_profile'))
    sql = "UPDATE user \
    SET email = '%s' WHERE username = '%s'"%(new_email,session['username'])
    cursor.execute(sql)
    try:
     conn.commit()
     flash("Email changed succesfully.",category = 'success')
    except:
     conn.rollback()
  if(request.form.get('new first name')):
    new_first_name = request.form.get('new first name')
    sql = "UPDATE user \
    SET first_name = '%s' WHERE username = '%s'"%(new_first_name,session['username'])
    cursor.execute(sql)
    try:
     conn.commit()
     flash("Name changed succesfully.",category = 'success')
    except:
     conn.rollback()   
  if(request.form.get('new last name')):
    new_last_name = request.form.get('new last name')
    sql = "UPDATE user \
    SET last_name = '%s' WHERE username = '%s'"%(new_last_name,session['username'])
    cursor.execute(sql)
    try:
     conn.commit()
     flash("Surname changed succesfully.",category = 'success')
    except:
     conn.rollback()
  if(request.form.get('new age')):
    new_age = request.form.get('new age')
    sql = "UPDATE user \
    SET age = '%s' WHERE username = '%s'"%(new_age,session['username'])
    cursor.execute(sql)
    try:
     conn.commit()
     flash("Email changed succesfully.",category = 'success')
    except:
     conn.rollback()   
  conn.close      
  conn.close
  return render_template('edit_username.html')

@app.route('/see users')   
def see_users():
  if (session['loggedin'] == True and session['flag'] == 'library admin'):
        conn = pymysql.connect(db = "testdb",user = "iago_desperado", password = "Yq9ZkNMkd7!3yNx", host = "localhost")
        cursor = conn.cursor()
        sql = "SELECT username FROM user WHERE flag = 'student' OR flag = 'teacher'"
        cursor.execute(sql)
        users = cursor.fetchall()
        conn.close()
  else:
    flash("You must be a library administrator in order to see the users list")
    return redirect(url_for('index'))
  return render_template('see_users.html',users = users)

@app.route('/see users/edit <user>')
def edit_user(user):
  conn = pymysql.connect(db = "testdb",user = "iago_desperado", password = "Yq9ZkNMkd7!3yNx", host = "localhost")
  cursor = conn.cursor()
  sql = "SELECT * FROM user WHERE username = '%s'"% user
  cursor.execute(sql)
  info = cursor.fetchone()
  return render_template('edit_user.html',info = info)
  
  
  

      
          



