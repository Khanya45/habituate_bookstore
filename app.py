from flask import Flask, request, jsonify, render_template, url_for
import sqlite3
from tkinter import *

# ==============================================================================================================================================================================
root = Tk()


# FUNCTION FOR ADDING NEW USER TO THE DATABASE
def signup():
    with sqlite3.connect('dbHabituate.db') as conn:
            mycursor = conn.cursor()
            strEncode= edtName.get()[0:3] + edtName.get()[-3:-1] + edtSurname.get()[1:4]
            hex_string = strEncode.encode('utf-8')
            hex_value = hex_string.hex()
            isbn = hex_value
            mycursor.execute('INSERT INTO tblBooks (isbn , title, author, image, reviews, price,genre) VALUES(?,?,?,?,?,?,?)', (isbn, edtName.get(), edtSurname.get(), edtMobile.get(), edtreviews.get(), edtprice.get(), edtID.get()))
            conn.commit()


# ========== VISITOR'S FRAME ===========
lbFrame_visitor = LabelFrame(root, text="VISITOR'S DETAILS", width=330, height=400, bg="#141215", fg="white")
lbFrame_visitor.place(x=20, y=200)

lbName = Label(lbFrame_visitor, text="Book Name", bg="#141215", fg="white")
lbName.place(x=10, y=20)
edtName = Entry(lbFrame_visitor)
edtName.place(x=130, y=20)

lbSurname = Label(lbFrame_visitor, text="Author", bg="#141215", fg="white")
lbSurname.place(x=10, y=60)
edtSurname = Entry(lbFrame_visitor)
edtSurname.place(x=130, y=60)

lbID = Label(lbFrame_visitor, text="category", bg="#141215", fg="white")
lbID.place(x=10, y=100)
edtID = Entry(lbFrame_visitor)
edtID.place(x=130, y=100)

lbreviews = Label(lbFrame_visitor, text="reviews", bg="#141215", fg="white")
lbreviews.place(x=10, y=140)
edtreviews = Entry(lbFrame_visitor)
edtreviews.place(x=130, y=140)

lbprice = Label(lbFrame_visitor, text="price", bg="#141215", fg="white")
lbprice.place(x=10, y=180)
edtprice = Entry(lbFrame_visitor)
edtprice.place(x=130, y=180)

lbMobile = Label(lbFrame_visitor, text="image", bg="#141215", fg="white")
lbMobile.place(x=10, y=220)
edtMobile = Entry(lbFrame_visitor)
edtMobile.place(x=130, y=220)
btnLogin = Button(root, text="SIGN UP", width=10, borderwidth=4, font="Times 15", command=signup, bg="#141215", fg="white")
btnLogin.place(x=190, y=530)
root.mainloop()
# ===========================================================================================================================================================================

app = Flask(__name__)
app.debug = True


def create_tables():
    # CREATING A DATABASE
    conn = sqlite3.connect('dbHabituate.db')
    print("Opened database successfully")
    # CREATING TABLES
    conn.execute('CREATE TABLE IF NOT EXISTS tblCustomer (customer_id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, surname TEXT, email TEXT)')
    conn.execute('CREATE TABLE IF NOT EXISTS tblHistory (customer_id INTEGER, isbn TEXT, book_Title TEXT, quantity TEXT,total_price REAL, order_date DATETIME, FOREIGN KEY (customer_id) REFERENCES tblCustomer (customer_id), FOREIGN KEY (isbn) REFERENCES tblBooks (isbn))')
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


# ADDING NEW BOOKS ON THE TABLE
@app.route('/add-new-books/', methods=["POST"])
def add_new_books():
    if request.method == 'POST':
        try:
            title = request.form['title']
            reviews = request.form['reviews']
            author = request.form['author']
            image = request.form['image']
            hex_string = "rhyrg".encode('utf-8')
            hex_value = hex_string.hex()
            isbn = hex_value
            price = request.form['price']
            genre = request.form['genre']

            with sqlite3.connect('dbHabituate.db') as conn:
                cur = conn.cursor()
                cur.execute('INSERT INTO tblBooks (isbn , title, author, image, reviews, price,genre) VALUES(?,?,?,?)', (isbn, title, author, image, reviews, price, genre))
                conn.commit()
                msg = "Record successfully added"
        except Exception as e:
            conn.rollback()
            msg = "Error occured in insert:" + str(e)
        finally:
            return url_for(add_books_api)


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


# ADDING THE NEW ADMIN ON THE TABLE
@app.route('/user-registration/', methods=["POST"])
def user_registration():
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

        return render_template("bookstore.html")


# FUNCTION FOR DELETING A RECORD FROM BOTH TABLES
def delete():

    try:
        with sqlite3.connect("dbHabituate.db") as conn:
            mycursor = conn.cursor()
            mycursor.execute('DELETE FROM tblNextOfKin WHERE User_id=''')
            mycursor.execute('DELETE FROM tblUser WHERE User_id=''')
            conn.commit()
            # row_id = tblUser.focus()
            # tblUser.delete(row_id)
            message = "successfully deleted"
    except:
        message = "Failed to delete the record"


# FUNCTION FOR ADDING A NEW RECORD OF A USER
def insert_user():
    try:
        with sqlite3.connect("dbHabituate.db") as conn:
            mycursor = conn.cursor()
            mycursor.execute('INSERT INTO tblUser (Name, Surname, ID,Mobile) VALUES ("'+edtNamet1.get()+'","'+edtSurnamet1.get()+'","'+edtIDt1.get()+'","'+edtMobilet1.get()+'")')
            # tblUser.insert("", 'end', values=(edtNamet1.get(), edtSurnamet1.get(), edtIDt1.get(), edtMobilet1.get()))
            conn.commit()
            mycursor.execute('SELECT User_id FROM tblUser WHERE ID="'+""+'"')
            row = mycursor.fetchall()
            # edtUser_idt1.insert(0, row)
            message = "Successfully added"
    except:
        message = "Failed to add the record"


# FUNCTION FOR EDITING A RECORD OF A USER
def update_user():
        try:
            selected = tblUser.focus()
            temp = tblUser.item(selected, 'values')
            tblUser.item(selected, values=(edtNamet1.get(), edtSurnamet1.get(), edtIDt1.get(), edtMobilet1.get(), temp[4], temp[5], temp[6]))
            mycursor.execute('UPDATE tblUser SET Name="'+edtNamet1.get()+'", Surname="'+edtSurnamet1.get()+'", Mobile="'+edtMobilet1.get()+'", ID="'+edtIDt1.get()+'" WHERE User_id='+edtUser_idt1.get())
            mydb.commit()
            messagebox.showinfo("", "Successfully updated")
        except:
            messagebox.showerror("", "Failed to insert")







# with sqlite3.connect("dbHabituate.db") as conn:
#     cursor = conn.cursor()
#     cursor.execute("SELECT * FROM tblBooks")
#     results = cursor.fetchall()
#     print(results)
