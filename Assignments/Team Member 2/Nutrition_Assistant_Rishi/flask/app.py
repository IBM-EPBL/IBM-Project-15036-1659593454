
from flask import Flask, render_template, request
import sqlite3
import os

app = Flask(__name__)
current_dir = os.path.dirname(os.path.abspath(__file__))

#Home Page
@app.route('/')
def Home():
    return render_template('index.html')


#Signup Page
@app.route('/signup')
def signup():
    return render_template('signup.html')

#Method POST
@app.route('/signup', methods = ['POST'])
def Registration():
    username = request.form['username']
    password = request.form['password']
    phone = request.form['phone']
    id="NULL"
    connection = sqlite3.connect(current_dir + "/NutritionAssistDB.db")
    cursor = connection.cursor()
    query1 = "INSERT INTO users VALUES('{username}', '{password}', {phone}, {id})".format(username=username, password=password, phone=phone, id=id)
    cursor.execute(query1)
    connection.commit()
    return render_template('login.html')


def signup():
    return render_template('signup.html')


#Login Page
@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == "POST" :
        username = request.form['username']
        password = request.form['password']
        connection = sqlite3.connect(current_dir + "/NutritionAssistDB.db")
        cursor = connection.cursor()
        Searchquery = "SELECT * FROM users WHERE username ='{arg1}' and password='{arg2}'".format(arg1=username, arg2=password)
        cursor.execute(Searchquery)
        try:
            x = cursor.fetchall()[0]
            connection.commit()
            return render_template('index.html', user=username)
        except:
            connection.commit()
            return render_template('login.html', error="No account found !")
       
        
    else:
        return render_template('login.html')




if __name__ == '__main__':
    app.run(debug=True)