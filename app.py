from flask import Flask, request, jsonify, render_template, url_for
from flask_jwt import JWT, jwt_required, current_identity
import hmac, datetime
import sqlite3
from flask import redirect


app = Flask(__name__)
app.debug = True


def create_tables():
    # CREATING A DATABASE
    conn = sqlite3.connect('dbHabituate.db')
    print("Opened database successfully")
    # CREATING TABLES
    conn.execute('CREATE TABLE IF NOT EXISTS tblCustomer (customer_id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, surname TEXT, email TEXT)')
    conn.execute('CREATE TABLE IF NOT EXISTS tblHistory (transaction_id INTEGER AUTO_INCREMENT PRIMARY KEY, customer_id INTEGER, isbn TEXT, book_Title TEXT, quantity TEXT,total_price REAL, order_date DATETIME, FOREIGN KEY (customer_id) REFERENCES tblCustomer (customer_id), FOREIGN KEY (isbn) REFERENCES tblBooks (isbn))')
    conn.execute('CREATE TABLE IF NOT EXISTS tblUser (user_id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, surname TEXT, password TEXT, username TEXT)')
    conn.execute("CREATE TABLE IF NOT EXISTS tblBooks (isbn TEXT PRIMARY KEY, title TEXT, author TEXT, image TEXT, reviews TEXT, price REAL,genre TEXT)")
    print("Table created successfully")
    conn.close()


# create_tables()


# REGISTRATION PAGE FOR NEW BOOKS
@app.route('/enter-new/')
def enter_new_student():
    return render_template('addNewBook.html')


# CREATING API OF BOOK DETAILS
@app.route('/booklist-api/', methods=['GET'])
def add_books_api():
     with sqlite3.connect('dbHabituate.db') as conn:
            cur = conn.cursor()
            # cur.execute('UPDATE tblBooks SET image= "https://images1.penguinrandomhouse.com/cover/9780140280197" WHERE author= "robert greene" ')
            # conn.commit()
            cur.execute('SELECT * FROM tblBooks')
            results = cur.fetchall()
            return jsonify(results)


# HOME PAGE OF THE BOOKSTORE WEBSITE
@app.route('/bookstore/')
def show_books():
    return render_template("bookstore.html")


# SIGN IN PAGE FOR A NEW ADMIN
@app.route('/sign-up/')
def sign_up():
    return render_template("sign_up.html")


# LOG IN PAGE FOR A NEW ADMIN
@app.route('/log-in/')
def log_in():
    return render_template("log_in.html")


# ========================================================================================================================================================================
# =================================================================== BACK END ===============================================================
# ========================================================================================================================================================================


class User(object):
    def __init__(self, id, username, password):
        self.id = id
        self.username = username
        self.password = password


def fetch_users():
    with sqlite3.connect('dbHabituate.db') as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM tblUser")
        users = cursor.fetchall()
        new_data = []
        for data in users:
            new_data.append(User(data[0], data[4], data[3]))
    return new_data


users = fetch_users()
username_table = {u.username: u for u in users}
userid_table = {u.id: u for u in users}


def authenticate(username, password):
    user = username_table.get(username, None)
    if user and hmac.compare_digest(user.password.encode('utf-8'), password.encode('utf-8')):
        return user


def identity(payload):
    id = payload['identity']
    return userid_table.get(id, None)


app = Flask(__name__)
app.debug = True
app.config['SECRET_KEY'] = 'super-secret'

jwt = JWT(app, authenticate, identity)


@app.route('/protected')
@jwt_required()
def protected():
    return '%s' % current_identity


# ADDING THE NEW ADMIN ON THE TABLE
@app.route('/user-registration/', methods=["POST"])
def user_registration():
    response = {}

    if request.method == "POST":

        name = request.form['name']
        surname = request.form['surname']
        username = request.form['username']
        password = request.form['password']

        with sqlite3.connect("dbHabituate.db") as conn:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO tblUser("
                           "name,"
                           "surname,"
                           "username,"
                           "password) VALUES(?, ?, ?, ?)", (name, surname, username, password))
            conn.commit()
            response["message"] = "success"
            response["status_code"] = 201

        return response


# ADDING NEW BOOKS ON THE TABLE
@app.route('/add-new-books/', methods=["POST"])
# @jwt_required()
def add_new_books():
    response = {}

    if request.method == 'POST':
        title = request.form['title']
        reviews = request.form['reviews']
        author = request.form['author']
        image = request.form['image']
        strEncode = title[0:3] + title[-3:-1] + author[1:4]
        hex_string = strEncode.encode('utf-8')
        hex_value = hex_string.hex()
        isbn = hex_value
        price = request.form['price']
        genre = request.form['genre']

        with sqlite3.connect('dbHabituate.db') as conn:
            cur = conn.cursor()
            cur.execute('INSERT INTO tblBooks (isbn , title, author, image, reviews, price,genre) VALUES(?,?,?,?,?,?,?)', (isbn, title, author, image, reviews, price, genre))
            conn.commit()
            response["status_code"] = 201
            response['description'] = "Book added succesfully"
        return response


# DISPLAYING ALL BOOKS
@app.route('/get-books/', methods=["GET"])
def get_books():
    response = {}
    with sqlite3.connect("dbHabituate.db") as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM tblBooks")
        posts = cursor.fetchall()
    response['status_code'] = 200
    response['data'] = posts
    return response


# DELETE A BOOK
@app.route("/delete-post/<id>/")
# @jwt_required()
def delete_post(id):
    response = {}
    with sqlite3.connect("dbHabituate.db") as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM tblBooks WHERE isbn=?", [id])
        conn.commit()
        response['status_code'] = 200
        response['message'] = "blog post deleted successfully."
    return response


# UPDATE A BOOK ROW
@app.route('/edit-book/<isbn>/', methods=["PUT"])
# @jwt_required()
def edit_book(isbn):
    response = {}

    if request.method == "PUT":
        with sqlite3.connect('dbHabituate.db') as conn:
            incoming_data = dict(request.json)
            put_data = {}
            # ===================== UPDATING TITLE =================================
            if incoming_data.get("title") is not None:
                put_data["title"] = incoming_data.get("title")
                with sqlite3.connect('dbHabituate.db') as conn:
                    cursor = conn.cursor()
                    cursor.execute("UPDATE tblBooks SET title =? WHERE id=?", ([put_data["title"]], [isbn]))
                    conn.commit()
                    response['message'] = "Update was successfully"
                    response['status_code'] = 200
            # ===================== UPDATING AUTHOR =================================
            if incoming_data.get("author") is not None:
                put_data['author'] = incoming_data.get('author')

                with sqlite3.connect('dbHabituate.db') as conn:
                    cursor = conn.cursor()
                    cursor.execute("UPDATE tblBooks SET author =? WHERE id=?", (put_data["author"], isbn))
                    conn.commit()

                    response["content"] = "author updated successfully"
                    response["status_code"] = 200
            # ===================== UPDATING IMAGE =================================
            if incoming_data.get("image") is not None:
                put_data["image"] = incoming_data.get("image")
                with sqlite3.connect('dbHabituate.db') as conn:
                    cursor = conn.cursor()
                    cursor.execute("UPDATE tblBooks SET image =? WHERE id=?", (put_data["image"], isbn))
                    conn.commit()
                    response['message'] = "Update was successfully"
                    response['status_code'] = 200
            # ===================== UPDATING REVIEWS =================================
            if incoming_data.get("reviews") is not None:
                put_data['reviews'] = incoming_data.get('reviews')

                with sqlite3.connect('dbHabituate.db') as conn:
                    cursor = conn.cursor()
                    cursor.execute("UPDATE tblBooks SET reviews =? WHERE id=?", (put_data["reviews"], isbn))
                    conn.commit()

                    response["content"] = "Content updated successfully"
                    response["status_code"] = 200
            # ===================== UPDATING PRICE =================================
            if incoming_data.get("price") is not None:
                put_data["price"] = incoming_data.get("price")
                with sqlite3.connect('dbHabituate.db') as conn:
                    cursor = conn.cursor()
                    cursor.execute("UPDATE tblBooks SET price =? WHERE id=?", (put_data["price"], isbn))
                    conn.commit()
                    response['message'] = "Update was successfully"
                    response['status_code'] = 200
            # ===================== UPDATING GENRE =================================
            if incoming_data.get("genre") is not None:
                put_data['genre'] = incoming_data.get('genre')

                with sqlite3.connect('dbHabituate.db') as conn:
                    cursor = conn.cursor()
                    cursor.execute("UPDATE tblBooks SET genre =? WHERE id=?", (put_data["genre"], isbn))
                    conn.commit()

                    response["content"] = "Content updated successfully"
                    response["status_code"] = 200
    return response


# DISPLAYING ALL USERS
@app.route('/get-user/<int:id>/', methods=["GET"])
def get_user(id):
    response = {}

    with sqlite3.connect("dbHabituate.db") as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM tblUser WHERE user_id=" + str(id))

        response["status_code"] = 200
        response["description"] = "Blog post retrieved successfully"
        response["data"] = cursor.fetchone()

    return jsonify(response)


# DISPLAYING ALL USERS
@app.route('/filter-books/<genre>/')
def filter_books(genre):
    response = {}

    with sqlite3.connect("dbHabituate.db") as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM tblBooks WHERE genre=?", [genre])
        response["status_code"] = 200
        response["description"] = "Books filtered successfully"
        response["data"] = cursor.fetchall()

    return jsonify(response)


@app.route('/sort-books/<sort_by>/')
def sort_books(sort_by):
    response = {}

    with sqlite3.connect("dbHabituate.db") as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM tblBooks ORDER BY " + sort_by)
        response["status_code"] = 200
        response["description"] = "Books sorted successfully"
        response["data"] = cursor.fetchall()

    return jsonify(response)


# ========================================================= FOR HISTORY TABLE ==========================================================

# ADDING NEW TRANSACTIONS ON THE TABLE
@app.route('/add-transaction/<int:customer_id>/<isbn>/', methods=["POST"])
# @jwt_required()
def add_transaction(customer_id, isbn):
    response = {}

    if request.method == 'POST':
        with sqlite3.connect('dbHabituate.db') as conn:
            cur = conn.cursor()
            cur.execute('SELECT isbn,title,price FROM tblBooks WHERE isbn=?', [isbn])
            book_details = cur.fetchall()
            quantity = request.form['quantity']
            order_date = datetime.datetime.now()
            cur.execute('INSERT INTO tblHistory (customer_id, isbn , book_Title, quantity, total_price, order_date) VALUES(?,?,?,?,?,?)', (customer_id, book_details[0][0], book_details[0][1], quantity, book_details[0][2], order_date))
            # cur.execute('UPDATE tblHistory SET customer_id = 1 WHERE book_Title = "48 laws of power"')
            # cur.execute('UPDATE tblHistory SET customer_id = 2 WHERE book_Title = "the greatest secret"')
            conn.commit()
            response["status_code"] = 201
            response['description'] = "Book added succesfully"
        return response


# DISPLAYING ALL BOOKS
# @app.route('/get-books/', methods=["GET"])
# def get_books():
#     response = {}
#     with sqlite3.connect("dbHabituate.db") as conn:
#         cursor = conn.cursor()
#         cursor.execute("SELECT * FROM tblBooks")
#         posts = cursor.fetchall()
#     response['status_code'] = 200
#     response['data'] = posts
#     return response


# DELETE A BOOK
@app.route("/delete-post/<id>/")
# @jwt_required()
def delete_books(id):
    response = {}
    with sqlite3.connect("dbHabituate.db") as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM tblBooks WHERE isbn=?", [id])
        conn.commit()
        response['status_code'] = 200
        response['message'] = "blog post deleted successfully."
    return response

# with sqlite3.connect("dbHabituate.db") as conn:
#     cursor = conn.cursor()
#     cursor.execute("SELECT * FROM tblBooks")
#     results = cursor.fetchall()
#     print(results)


# TOTAL PRICE OF A CUSTOMER
@app.route("/price-calculation/<int:customer_id>")
def total_price(customer_id):
        with sqlite3.connect("dbHabituate.db") as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT sum(price) AS total_price FROM tblBooks WHERE customer_id=", str(customer_id))
            total = cursor.fetchone()
        return jsonify(total)


# OVERALL PRICE OF THE BOOKSTORE
@app.route("/bookstore_profit/")
def total_profit():
    with sqlite3.connect("dbHabituate.db") as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT sum(price) AS total_price FROM tblBooks")
        results = cursor.fetchall()
    return jsonify(results)


# ADDING THE NEW customer ON THE TABLE
@app.route('/customer-registration/', methods=["POST"])
def customer_registration():
    response = {}

    if request.method == "POST":

        name = request.form['name']
        surname = request.form['surname']
        email = request.form['email']

        with sqlite3.connect("dbHabituate.db") as conn:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO tblCustomer("
                           "name,"
                           "surname,"
                           "email) VALUES(?, ?, ?)", (name, surname, email))
            conn.commit()
            response["message"] = "success"
            response["status_code"] = 201

        return response


# IMAGE HOSTING
@app.route('/image-hosting/')
def image_hosting():
    with sqlite3.connect("dbHabituate.db") as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT image FROM tblBooks WHERE isbn='34382077656f6265'")
        image = cursor.fetchone()
        for i in image:
            image1 = i
    return redirect(image1)


# with sqlite3.connect("dbHabituate.db") as conn:
#         cursor = conn.cursor()
#         cursor.execute("UPDATE tblHistory SET transaction_id= (SELECT last_insert_id() FROM tblBooks) WHERE isbn='34382077656f6265'")
#         id = cursor.fetchone()
#         print(id)

with sqlite3.connect('dbHabituate.db') as conn:
            cur = conn.cursor()
            cur.execute('SELECT * FROM tblHistory')
            book_details = cur.fetchall()
            print(book_details)
