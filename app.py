from flask import Flask, render_template, request, redirect
import mysql.connector
import os
from urllib.parse import urlparse

app = Flask(__name__)

# 🔥 GET DATABASE URL
db_url = os.getenv("mysql://root:uRzqvyjJetRKUSxkDvYANqfopxrtjaKp@caboose.proxy.rlwy.net:54119/railway")

# 👉 fallback for local testing (IMPORTANT)
if not db_url:
    db_url = "mmysql://root:uRzqvyjJetRKUSxkDvYANqfopxrtjaKp@caboose.proxy.rlwy.net:54119/railway"

url = urlparse(db_url)

# 🔥 DATABASE CONNECTION
db = mysql.connector.connect( 
    host=url.hostname,
    user=url.username,
    password=url.password,
    database=url.path[1:],   # ✅ correct way (remove "/")
    port=url.port
)
cursor = db.cursor()

# Home Page
@app.route  ('/')
def home():
    return render_template("home.html")

# ADD PAGE
@app.route('/add')
def add():
    return render_template("add.html")

@app.route('/insert', methods=['POST'])
def insert():
    name = request.form['name']
    mobile = request.form['mobile']
    amount = request.form['amount']
    location = request.form['location']

    cursor.execute(
        "INSERT INTO customer VALUES (%s,%s,%s,%s)",
        (name, mobile, amount, location)
    )
    db.commit()
    return redirect('/')

# DISPLAY PAGE
@app.route('/display')
def display():
    cursor.execute("SELECT * FROM customer")
    data = cursor.fetchall()
    return render_template("display.html", customers=data)

# MANAGE PAGE (Update/Delete list)
@app.route('/manage')
def manage():
    cursor.execute("SELECT * FROM customer")
    data = cursor.fetchall()
    return render_template("manage.html", customers=data)

# EDIT PAGE
@app.route('/edit/<mobile>')
def edit(mobile):
    cursor.execute("SELECT * FROM customer WHERE mobile=%s", (mobile,))
    data = cursor.fetchone()
    return render_template("edit.html", customer=data)

# UPDATE
@app.route('/update', methods=['POST'])
def update():
    name = request.form['name']
    mobile = request.form['mobile']
    amount = request.form['amount']
    location = request.form['location']

    cursor.execute(
        "UPDATE customer SET name=%s, amount=%s, location=%s WHERE mobile=%s",
        (name, amount, location, mobile)
    )
    db.commit()
    return redirect('/manage')

# DELETE
@app.route('/delete/<mobile>')
def delete(mobile):
    cursor.execute("DELETE FROM customer WHERE mobile=%s", (mobile,))
    db.commit()
    return redirect('/manage')

if __name__ == "__main__":
    app.run(debug=True,port=5001)