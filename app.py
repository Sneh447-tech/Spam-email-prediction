from flask import Flask, render_template, request, redirect, session
import sqlite3
import pickle
import os

app = Flask(__name__)
app.secret_key = "spam_secret_key"


# =====================================================
# LOAD ML MODEL
# =====================================================
model = pickle.load(open("spam_model.pkl", "rb"))
vectorizer = pickle.load(open("vectorizer.pkl", "rb"))


# =====================================================
# DATABASE CREATE
# =====================================================
def init_db():
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    # USERS TABLE
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE,
        password TEXT,
        is_premium INTEGER DEFAULT 0,
        trial_count INTEGER DEFAULT 3
    )
    """)

    # HISTORY TABLE
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS history(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user TEXT,
        text TEXT,
        spam_score REAL,
        prediction TEXT
    )
    """)

    conn.commit()
    conn.close()


init_db()


# =====================================================
# HOME
# =====================================================
@app.route("/")
def home():
    return redirect("/register")


# =====================================================
# REGISTER
# =====================================================
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()

        try:
            cursor.execute(
                "INSERT INTO users(username,password) VALUES (?,?)",
                (username, password)
            )
            conn.commit()
            conn.close()
            return redirect("/login")
        except:
            conn.close()
            return render_template("register.html", msg="Username already exists")

    return render_template("register.html")


# =====================================================
# LOGIN
# =====================================================
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()

        cursor.execute(
            "SELECT * FROM users WHERE username=? AND password=?",
            (username, password)
        )

        user = cursor.fetchone()
        conn.close()

        if user:
            session["user"] = username
            return redirect("/dashboard")
        else:
            return render_template("login.html", msg="Invalid Login")

    return render_template("login.html")


# =====================================================
# DASHBOARD
# =====================================================
@app.route("/dashboard")
def dashboard():
    if "user" not in session:
        return redirect("/login")

    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    cursor.execute(
        "SELECT is_premium, trial_count FROM users WHERE username=?",
        (session["user"],)
    )

    data = cursor.fetchone()
    conn.close()

    premium = data[0]
    trials = data[1]

    return render_template(
        "dashboard.html",
        user=session["user"],
        premium=premium,
        trials=trials
    )


# =====================================================
# PREDICT EMAIL
# =====================================================
@app.route("/predict", methods=["GET", "POST"])
def predict():
    if "user" not in session:
        return redirect("/login")

    result = None
    score = None

    if request.method == "POST":

        text = request.form["email"]

        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()

        cursor.execute(
            "SELECT is_premium, trial_count FROM users WHERE username=?",
            (session["user"],)
        )

        user_data = cursor.fetchone()
        premium = user_data[0]
        trials = user_data[1]

        # if free trial ended
        if premium == 0 and trials <= 0:
            conn.close()
            return redirect("/payment")

        # ML Prediction
        vec = vectorizer.transform([text])
        pred = model.predict(vec)[0]
        prob = model.predict_proba(vec)[0]

        if pred == 1:
            result = "SPAM 🚫"
            score = round(prob[1] * 100, 2)
        else:
            result = "NOT SPAM ✅"
            score = round(prob[0] * 100, 2)

        # reduce free trial
        if premium == 0:
            cursor.execute(
                "UPDATE users SET trial_count = trial_count - 1 WHERE username=?",
                (session["user"],)
            )

        # save history
        cursor.execute("""
        INSERT INTO history(user,text,spam_score,prediction)
        VALUES (?,?,?,?)
        """, (session["user"], text, score, result))

        conn.commit()
        conn.close()

    return render_template(
        "predict.html",
        result=result,
        score=score
    )


# =====================================================
# HISTORY
# =====================================================
@app.route("/history")
def history():
    if "user" not in session:
        return redirect("/login")

    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    cursor.execute("""
    SELECT text, spam_score, prediction
    FROM history
    WHERE user=?
    ORDER BY id DESC
    """, (session["user"],))

    rows = cursor.fetchall()
    conn.close()

    return render_template("history.html", rows=rows)


# =====================================================
# SAFE DEMO PAYMENT PAGE
# =====================================================
@app.route("/payment")
def payment():
    if "user" not in session:
        return redirect("/login")

    return render_template("payment.html")


# =====================================================
# PAYMENT SUCCESS (NO REAL MONEY)
# =====================================================
@app.route("/payment_success", methods=["POST"])
def payment_success():
    if "user" not in session:
        return redirect("/login")

    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    cursor.execute("""
    UPDATE users
    SET is_premium = 1
    WHERE username = ?
    """, (session["user"],))

    conn.commit()
    conn.close()

    return redirect("/dashboard")


# =====================================================
# LOGOUT
# =====================================================
@app.route("/logout")
def logout():
    session.clear()
    return redirect("/register")


# =====================================================
# RUN
# =====================================================
if __name__ == "__main__":
    app.run(debug=True)