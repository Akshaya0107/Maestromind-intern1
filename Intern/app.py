from flask import Flask, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL
from werkzeug.security import generate_password_hash, check_password_hash
import os

app = Flask(__name__)
app.secret_key = "your_secret_key"

# ---------------- MYSQL CONFIG ----------------
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'sree@2008'  # your MySQL password
app.config['MYSQL_DB'] = 'flask_app'

mysql = MySQL(app)

# ---------------- HOME ----------------
@app.route("/")
def home():
    return redirect(url_for("login"))

# ---------------- LOGIN ----------------
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM users WHERE username=%s", (username,))
        user = cur.fetchone()

        if user:
            stored_password = user[2]  # column index of password

            if check_password_hash(stored_password, password):
                session["user"] = username
                return redirect(url_for("dashboard"))

        return render_template("login.html", error="Invalid username or password")

    return render_template("login.html")

# ---------------- SIGNUP ----------------
@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        username = request.form["username"]
        password = generate_password_hash(request.form["password"])

        cur = mysql.connection.cursor()
        try:
            cur.execute(
                "INSERT INTO users (username, password) VALUES (%s, %s)",
                (username, password),
            )
            mysql.connection.commit()
        except:
            return render_template("signup.html", error="Username already exists")

        return redirect(url_for("login"))

    return render_template("signup.html")

# ---------------- DASHBOARD ----------------
@app.route("/dashboard")
def dashboard():
    if "user" not in session:
        return redirect(url_for("login"))
    return render_template("dashboard.html", user=session["user"])

# ---------------- LOGOUT ----------------
@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect(url_for("login"))

# -------- QUOTATION / INVOICE / NOTES / VOUCHERS --------
@app.route('/quotation')
def quotation():
    return render_template("quotation.html")

@app.route('/invoice/tax')
def tax_invoice():
    return render_template("tax_invoice.html")

@app.route('/invoice/proforma')
def proforma_invoice():
    return render_template("proforma_invoice.html")

@app.route('/note/credit')
def credit_note():
    return render_template("credit_note.html")

@app.route('/note/debit')
def debit_note():
    return render_template("debit_note.html")

@app.route('/voucher/receipt')
def receipt_voucher():
    return render_template("receipt_voucher.html")

@app.route('/voucher/payment')
def payment_voucher():
    return render_template("payment_voucher.html")

# ---------------- RUN APP ----------------

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
