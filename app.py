from flask import Flask, render_template,request, redirect, url_for, session
import sqlite3 as sql
import secrets
app=Flask(__name__)

secret_key = secrets.token_hex(16) 
app.config['SECRET_KEY'] = secret_key

import sqlite3  
  
con = sqlite3.connect("PersonalPortfolio.db")  
print("Database opened successfully")  

con.execute("CREATE TABLE IF NOT EXISTS USER(USERNAME TEXT PRIMARY KEY NOT NULL, PASSWORD VARCHAR(8) NOT NULL)")
print("Table created successfully")
# logincred=["tanvi","admin"]
print("Data inserted successfully")

con.close()


@app.route('/')
def index():
    return render_template("index.html")


@app.route("/contform/")
def contform():
    return render_template("contform.html")


@app.route("/view")  
def view():  
    con = sqlite3.connect("PersonalPortfolio.db")  
    con.row_factory = sqlite3.Row  
    cur = con.cursor()  
    cur.execute("select * from CONTACTS")  
    rows = cur.fetchall()  
    return render_template("dashboard.html",rows = rows)  
    

@app.route('/insertdata', methods=['POST','GET'])
def insertdata():
    msg = "msg"
    if request.method=='POST':
        try:
            name=request.form['name']
            email_id=request.form['email_id']
            message=request.form['message']

            with sql.connect("PersonalPortfolio.db") as con:
                cur=con.cursor()
                cur.execute("INSERT into CONTACTS (name, email_id, message) values (?,?,?)",(name,email_id,message))
                msg="Successfully Added"
                con.commit()
        except:
            con.rollback()
            msg="Error in operation, contact not added"
        finally:
                return render_template("contform.html",msg = msg)
                

  

@app.route('/login', methods =['GET', 'POST'])
def login():
    msg = "msg"
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username = request.form['username']
        password = request.form['password']
        con=sqlite3.connect("PersonalPortfolio.db")
        cur=con.cursor()
        
        cur.execute('SELECT * FROM USER WHERE username = "tanvi"')
        account=cur.fetchall()
        if account:
            session['loggedin'] = True
            session['username'] = account[0]
            msg = 'Logged in successfully !'  
            return redirect(url_for("view"))
        else:
            msg = 'Incorrect username / password !'
    return render_template('login.html', msg = msg)


 
if __name__=="__main__":
    app.run(debug=True)