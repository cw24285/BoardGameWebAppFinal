from flask import Flask, render_template, redirect, request, url_for, flash, session
from pathlib import Path
import sqlite3
import hashlib

app = Flask (__name__)
app.secret_key = "55370e71b9e52ea8de1bf08597b020b25128e6c4d598228fb9354c588166080f"

folder = Path(__file__).resolve().parent
db = "bayviewboardgame.db"

def get_db():
    conn = sqlite3.connect(folder/db)
    conn.row_factory = sqlite3.Row
    return conn

loggedin = True

def init_db():
    conn = sqlite3.connect(db)
    conn.execute("""CREATE TABLE IF NOT EXISTS forms (
                    form_id INTEGER PRIMARY KEY,
                    email TEXT NOT NULL,
                    name TEXT NOT NULL,
                    message TEXT NOT NULL)""")
    
    conn.execute("""CREATE TABLE IF NOT EXISTS logins (
                    login_id INTEGER PRIMARY KEY,
                    email TEXT NOT NULL,
                    password TEXT NOT NULL,
                    admin INTEGER NOT NULL DEFAULT 0)""")
    conn.commit()
    conn.close()

init_db()

@app.route("/")
def home():
    base = "loggedinbase.html" if "email" in session else\
    "base.html"
    return render_template("Home.html", base=base)

@app.route("/contact")
def contact():
    base = "loggedinbase.html" if "email" in session else\
    "base.html"
    return render_template("Contact.html", base=base)

@app.route("/info")
def info():
    base = "loggedinbase.html" if "email" in session else\
    "base.html"
    return render_template("Info.html", base=base)

@app.route("/bbgfb")
def bbgfb():
    return render_template("bbgfb.html")

@app.route("/bccfb")
def bccfb():
    return render_template("bccfb.html")

@app.route("/login")
def login():
    base = "loggedinbase.html" if "email" in session else\
    "base.html"
    return render_template("login.html", base=base)

@app.route("/adminform")
def adminform():
    base = "loggedinbase.html" if "email" in session else "base.html"

    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT email, name, message FROM forms ORDER BY form_id DESC")
    forms = cursor.fetchall()
    conn.close()

    return render_template("AdminForm.html", base=base, forms=forms)

@app.route("/loginpage", methods=["POST"]) 
def loginpage(): 
    email = request.form.get("loginemail")
    password = request.form.get("loginpassword")
    conn = get_db() 
    cursor = conn.cursor()
    cursor.execute("SELECT password, admin FROM logins WHERE email =?", (email,))
    row = cursor.fetchone()

    hash = hashlib.sha256(password.encode()).hexdigest()

    if row and row[0] == hash:
        session["email"] = email
        session["is_admin"] = bool(row[1])
        return redirect(url_for("home"))

    flash("Incorrect email or password.", "login")
    return redirect(url_for("login"))

@app.route("/signup", methods=["POST"]) 
def signup(): 
    email = request.form.get("signupemail")
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT 1 FROM logins WHERE email = ?", (email,))
    if cursor.fetchone():
        conn.close()
        flash("Email already exists.","signup")
        return redirect(url_for("login"))
    else:
        password = request.form.get("signuppassword")
        data = password.encode()
        hash = hashlib.sha256(data).hexdigest()
        conn.execute("INSERT INTO logins (email, password) VALUES (?, ?)", 
                    (email, hash)) 
        conn.commit() 
        conn.close() 
        return redirect(url_for("home"))

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