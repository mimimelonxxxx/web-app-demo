"""
title: Flask Web App for Contacts
author: Michell Jiang
date-created: 2022-12-05
"""

from flask import Flask, render_template, request, redirect
from pathlib import Path
import sqlite3

### GLOBAL ###

DB_NAME = "flask.db"
FIRSTRUN = True
if (Path.cwd()/ DB_NAME).exists():
    FIRSTRUN = False

### FLASK ###

app = Flask(__name__) # makes the flask object 

@app.route("/", methods=["GET", "POST"])
def index():
    ALERT = ""
    if request.form:
        FIRSTNAME = request.form.get("first_name")
        LASTNAME = request.form.get("last_name")
        EMAIL = request.form.get("email")
        if EMAIL != "" and FIRSTNAME != "":
            if getContact(EMAIL) is None: 
                createContact(FIRSTNAME, LASTNAME, EMAIL)
                ALERT = "Successfully added a new contact!"
            else:
                ALERT = "A contact with the given email already exists. "
        else:
            ALERT = "Please fill in the required fields: First Name, Email"

    QUERYCONTACTS = getAll()
    return render_template("index.html", alert=ALERT, contacts=QUERYCONTACTS)

@app.route("/delete/<ID>")
def delete(ID):
    deleteContact(ID)
    return redirect("/")

### SQLITE ### 
def createTable():
    global DB_NAME
    CONNECTION = sqlite3.connect(DB_NAME)
    CURSOR = CONNECTION.cursor()
    CURSOR.execute("""
        CREATE TABLE 
            contacts (
                first_name TEXT NOT NULL,
                last_name TEXT,
                email TEXT PRIMARY KEY
            );
    """)
    CONNECTION.commit()
    CONNECTION.close()

def deleteContact(EMAIL):
    global DB_NAME
    CONNECTION = sqlite3.connect(DB_NAME)
    CURSOR = CONNECTION.cursor()
    CURSOR.execute("""
        DELETE FROM
            contacts
        WHERE
            email = ?;
    """, [EMAIL])
    CONNECTION.commit()
    CONNECTION.close()

def getContact(EMAIL):
    global DB_NAME
    CONNECTION = sqlite3.connect(DB_NAME)
    CURSOR = CONNECTION.cursor()
    CONTACT = CURSOR.execute("""
        SELECT
            *
        FROM
            contacts
        WHERE
            email = ?; 
    """, [EMAIL]).fetchone()
    return CONTACT

def createContact(FIRSTNAME, LASTNAME, EMAIL):
    global DB_NAME
    CONNECTION = sqlite3.connect(DB_NAME)
    CURSOR = CONNECTION.cursor()
    CURSOR.execute("""
        INSERT INTO
            contacts
        VALUES (
            ?,
            ?,
            ?
        );
    """, [FIRSTNAME, LASTNAME, EMAIL])

    CONNECTION.commit()
    CONNECTION.close()

def getAll():
    global DB_NAME
    CONNECTION = sqlite3.connect(DB_NAME)
    CURSOR = CONNECTION.cursor()
    CONTACTS = CURSOR.execute("""
        SELECT
            *
        FROM
            contacts
        ORDER BY 
            first_name;
    """).fetchall()
    CONNECTION.close()
    return CONTACTS

if __name__ == "__main__":
    if FIRSTRUN:
        createTable()
    app.run(debug=True)