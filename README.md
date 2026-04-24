# TaskFlow 🚀

### Smart Task Manager Web App

TaskFlow is a full-stack productivity web application built using Flask that helps users organize tasks, track deadlines, and receive automatic reminders through email notifications.

🔗 **Live Demo:** https://taskflow-6k9q.onrender.com

---

## ✨ Features

* 👤 User Registration & Login
* 🔐 Secure Password Hashing
* 📝 Add / Complete / Delete Tasks
* 🎯 Priority Levels (High / Medium / Low)
* 📌 Task Status Tracking
* ⏰ Due Today & Overdue Alerts
* 📧 Automatic Email Reminders
* 🌙 Responsive Dark Theme UI
* ☁️ Public Deployment on Render

---

## 🛠 Tech Stack

### Frontend

* HTML5
* CSS3
* Bootstrap 5
* Jinja2

### Backend

* Python
* Flask

### Database

* SQLite

### Automation

* APScheduler

### Security

* Werkzeug Password Hashing
* Environment Variables

---

## 📂 Project Structure

```text id="a4m5oc"
Task_manager/
│── app.py
│── requirements.txt
│── Procfile
│── tasks.db
│── templates/
│   ├── login.html
│   ├── register.html
│   └── dashboard.html
```

---

## ⚙️ Installation & Run Locally

```bash id="oq2n7z"
git clone https://github.com/Lovesh-afk/taskflow.git
cd taskflow
pip install -r requirements.txt
python app.py
```

---

## 🔑 Environment Variables

Create the following variables:

```text id="0k6ysd"
EMAIL_USER=your_email@gmail.com
EMAIL_PASS=your_google_app_password
SECRET_KEY=your_secret_key
```

---

## 🚀 Deployment

Hosted on **Render** using GitHub integration.

---

## 📈 Future Enhancements

* Password Reset
* Push Notifications
* PostgreSQL Migration
* Calendar View

---

## 👨‍💻 Author

**Lovesh**
