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

def init_db():
    conn = sqlite3.connect(db)
    conn.execute("""CREATE TABLE IF NOT EXISTS forms (
                    form_id INTEGER PRIMARY KEY,
                    email TEXT NOT NULL,
                    name TEXT NOT NULL,
                    message TEXT NOT NULL)""")
    conn.commit()
    conn.close()

init_db()

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

@app.route("/post", methods=["POST"]) 
def new_post(): 
    email = request.form.get("email")
    name = request.form.get("name")
    message = request.form.get("message")
    conn = get_db() 
    conn.execute("INSERT INTO forms (email, name, message) VALUES (?, ?, ?)", 
                 (email, name, message)) 
    conn.commit() 
    conn.close() 
    return redirect(url_for("contact"))

if __name__ == "__main__":
    app.run(debug=True)

    #yoza broza, we should add login page and add admins who can see all forms.