import sqlite3
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import smtplib, datetime


# VALIDATION FOR STRINGS
def is_string(*args):
    for arg in args:
        if arg.isdigit() == False:
            flag = True
        else:
            flag = False
    return flag


# VALIDATION FOR INTEGERS
def is_number(*args):
    for arg in args:
        if arg.isdigit() == True:
            flag = True
        else:
            flag = False
    return flag


# VALIDATION FOR LENGTH OF MOBILE
def length(*args):
    for arg in args:
        if len(arg) > 0:
            flag = True
        else:
            flag = False
    return flag


class clsUser:
    def __init__(self, name, surname, username, password):
        self.name = name
        self.surname = surname
        self.username = username
        self.password = password
        # self.email = email


    def user_registration(self):
        response = {}
        if is_string(self.name, self.surname) == True and length(self.name, self.surname, self.username, self.password) == True:

            with sqlite3.connect("dbHabituate.db") as conn:
                cursor = conn.cursor()
                cursor.execute("INSERT INTO tblUser("
                               "name,"
                               "surname,"
                               "username,"
                               "password) VALUES(?, ?, ?, ?)", (self.name, self.surname, self.username, self.password))
                conn.commit()
                response["message"] = "success"
                response["status_code"] = 201
        else:
            response["message"] = "Unsuccessful. Incorrect credentials"
            response["status_code"] = 400
        return response


    def get_transactions(self):
        response = {}
        with sqlite3.connect("dbHabituate.db") as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM tblHistory")
            transactions = cursor.fetchall()
        response['status_code'] = 200
        response['data'] = transactions
        return response


    def get_customers(self):
        response = {}
        with sqlite3.connect("dbHabituate.db") as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM tblCustomer")
            customers = cursor.fetchall()
        response['status_code'] = 200
        response['data'] = customers
        return response


objUser = clsUser("khanya", "gope", "khanya45", "khanyalake")
print(objUser.get_customers())
