from flask import Flask, render_template, request, redirect, session, flash
import sqlite3
from datetime import date
import smtplib
from email.mime.text import MIMEText
from apscheduler.schedulers.background import BackgroundScheduler
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = "secret123"

# ---------------- SQLITE CONNECTION ----------------
def get_db():
    conn = sqlite3.connect("tasks.db")
    conn.row_factory = sqlite3.Row
    return conn


# ---------------- CREATE TABLES ----------------
def init_db():
    conn = get_db()
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE,
        password TEXT,
        email TEXT
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS tasks (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        title TEXT,
        deadline TEXT,
        priority TEXT,
        status TEXT,
        notified INTEGER DEFAULT 0
    )
    """)

    conn.commit()
    conn.close()


# ---------------- EMAIL FUNCTION ----------------
def send_email(to_email, subject, body):
    sender_email = "lovesh8125@gmail.com"
    sender_password = "uahavmxwcibkutrm"

    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = sender_email
    msg["To"] = to_email

    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(sender_email, sender_password)
    server.send_message(msg)
    server.quit()


# ---------------- DEADLINE CHECKER ----------------
def check_deadlines():
    conn = get_db()
    cur = conn.cursor()

    cur.execute("""
    SELECT tasks.id, tasks.title, tasks.deadline,
           tasks.notified, users.email
    FROM tasks
    JOIN users ON tasks.user_id = users.id
    WHERE tasks.status='Pending'
    """)

    rows = cur.fetchall()
    today = str(date.today())

    for row in rows:
        task_id = row[0]
        title = row[1]
        deadline = row[2]
        notified = row[3]
        user_email = row[4]

        if not user_email:
            continue

        if notified == 0:

            if deadline == today:
                send_email(
                    user_email,
                    "Task Due Today",
                    f"Reminder: Your task '{title}' is due today."
                )

                cur.execute(
                    "UPDATE tasks SET notified=1 WHERE id=?",
                    (task_id,)
                )
                conn.commit()

            elif deadline < today:
                send_email(
                    user_email,
                    "Task Overdue",
                    f"Alert: Your task '{title}' is overdue."
                )

                cur.execute(
                    "UPDATE tasks SET notified=1 WHERE id=?",
                    (task_id,)
                )
                conn.commit()

    conn.close()


# ---------------- REGISTER ----------------
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':

        username = request.form['username']
        password = request.form['password']
        email = request.form['email']

        hashed_password = generate_password_hash(password)

        conn = get_db()
        cur = conn.cursor()

        try:
            cur.execute(
                "INSERT INTO users (username,password,email) VALUES (?,?,?)",
                (username, hashed_password, email)
            )
            conn.commit()

            flash("Registered successfully! Please login.")
            return redirect('/login')

        except:
            flash("Username already exists!")

        conn.close()

    return render_template('register.html')


# ---------------- LOGIN ----------------
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':

        username = request.form['username']
        password = request.form['password']

        conn = get_db()
        cur = conn.cursor()

        cur.execute(
            "SELECT * FROM users WHERE username=?",
            (username,)
        )

        user = cur.fetchone()
        conn.close()

        if user and check_password_hash(user["password"], password):
            session['user_id'] = user["id"]
            flash("Login successful!")
            return redirect('/')

        flash("Invalid credentials!")

    return render_template('login.html')


# ---------------- LOGOUT ----------------
@app.route('/logout')
def logout():
    session.pop('user_id', None)
    flash("Logged out successfully!")
    return redirect('/login')


# ---------------- DASHBOARD ----------------
@app.route('/')
def home():
    if 'user_id' not in session:
        return redirect('/login')

    priority = request.args.get('priority')
    status = request.args.get('status')

    query = "SELECT * FROM tasks WHERE user_id=?"
    values = [session['user_id']]

    if priority:
        query += " AND priority=?"
        values.append(priority)

    if status:
        query += " AND status=?"
        values.append(status)

    conn = get_db()
    cur = conn.cursor()

    cur.execute(query, tuple(values))
    tasks = cur.fetchall()

    conn.close()

    return render_template(
        "dashboard.html",
        tasks=tasks,
        today=str(date.today())
    )


# ---------------- ADD TASK ----------------
@app.route('/add', methods=['POST'])
def add_task():
    if 'user_id' not in session:
        return redirect('/login')

    title = request.form['title']
    deadline = request.form['deadline']
    priority = request.form['priority']
    user_id = session['user_id']

    conn = get_db()
    cur = conn.cursor()

    cur.execute("""
    INSERT INTO tasks
    (user_id,title,deadline,priority,status,notified)
    VALUES (?,?,?,?,?,?)
    """, (user_id, title, deadline, priority, "Pending", 0))

    conn.commit()
    conn.close()

    flash("Task added successfully!")
    return redirect('/')


# ---------------- COMPLETE TASK ----------------
@app.route('/complete/<int:id>')
def complete_task(id):
    conn = get_db()
    cur = conn.cursor()

    cur.execute(
        "UPDATE tasks SET status='Completed' WHERE id=?",
        (id,)
    )

    conn.commit()
    conn.close()

    flash("Task marked as completed!")
    return redirect('/')


# ---------------- DELETE TASK ----------------
@app.route('/delete/<int:id>')
def delete_task(id):
    conn = get_db()
    cur = conn.cursor()

    cur.execute(
        "DELETE FROM tasks WHERE id=?",
        (id,)
    )

    conn.commit()
    conn.close()

    flash("Task deleted!")
    return redirect('/')


# ---------------- TEST EMAIL ----------------
@app.route('/test-email')
def test_email():
    send_email(
        "lovesh8125@gmail.com",
        "Test Email",
        "Your Flask email system is working!"
    )
    return "Email Sent"


# ---------------- RUN APP ----------------
import os

if __name__ == '__main__':
    init_db()

    scheduler = BackgroundScheduler()
    scheduler.add_job(check_deadlines, 'interval', minutes=1)
    scheduler.start()

    app.run(
        host="0.0.0.0",
        port=int(os.environ.get("PORT", 5000))
    )