from flask import Flask, render_template, redirect, request, url_for
from pathlib import Path
import sqlite3

app = Flask (__name__)

folder = Path(__file__).resolve().parent
db = "form.db"

def get_db():
    conn = sqlite3.connect(folder/db)
    conn.row_factory = sqlite3.Row
    return conn

@app.route("/")
def home():
    return render_template("Home.html")

@app.route("/contact")
def contact():
    return render_template("Contact.html")

@app.route("/info")
def info():
    return render_template("Info.html")

@app.route("/bbgfb")
def bbgfb():
    return render_template("bbgfb.html")

@app.route("/bccfb")
def bccfb():
    return render_template("bccfb.html")

if __name__ == "__main__":
    app.run(debug=True)