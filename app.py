from flask import Flask, request, jsonify, render_template, url_for
import sqlite3


app = Flask(__name__)
app.debug = True


conn = sqlite3.connect('dbHabituate.db')
print("Opened database successfully")
conn.execute('CREATE TABLE IF NOT EXISTS tblCustomer (customer_id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, surname TEXT, addr TEXT, email TEXT, password TEXT)')
conn.execute('CREATE TABLE IF NOT EXISTS tblProduct (book_id INTEGER PRIMARY KEY AUTOINCREMENT, book_Title TEXT, quantity TEXT, price TEXT, bookstore_address)')
print("Table created successfully")
conn.close()



@app.route('/bookstore/')
def show_books():
    return render_template("bookstore.html")


@app.route('/sign-in/')
def sign_in():
    return render_template("sign_in.html")


@app.route('/user-registration/', methods=["POST"])
def user_registration():
    response = {}

    if request.method == "POST":

        name = request.form['name']
        surname = request.form['surname']
        addr = request.form['addr']
        password = request.form['password']
        email = request.form['email']

        with sqlite3.connect("dbHabituate.db") as conn:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO tblCustomer("
                           "name,"
                           "surname,"
                           "addr,"
                           "password,"
                           "email) VALUES(?, ?, ?, ?, ?)", (name, surname, addr, password, email))
            conn.commit()
            response["message"] = "success"
            response["status_code"] = 201

        return render_template("bookstore.html")


# with sqlite3.connect("dbHabituate.db") as conn:
#     cursor = conn.cursor()
#     cursor.execute("SELECT * FROM tblCustomer")
#     results = cursor.fetchall()
#     print(results)
