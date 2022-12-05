"""
title: Flask Web App for Contacts
author: Michell Jiang
date-created: 2022-12-05
"""

from flask import Flask, render_template, request
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
    if request.form:
        FIRSTNAME = request.form.get("first_name")
        LASTNAME = request.form.get("last_name")
        EMAIL = request.form.get("email")
        print(FIRSTNAME, LASTNAME, EMAIL)
    return render_template("index.html")

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

if __name__ == "__main__":
    if FIRSTRUN:
        createTable()
    app.run(debug=True)