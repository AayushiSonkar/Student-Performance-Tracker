# 🎓 Student Performance Tracker

A full-stack web application for teachers to manage students, record subject-wise grades, and generate performance reports — including class averages and subject/overall toppers.

## 🚀 Live Demo
🔗 **[https://student-performance-tracker-og73.onrender.com](https://student-performance-tracker-og73.onrender.com)**

## 🛠️ Tech Stack
- **Frontend:** HTML5, CSS3, Bootstrap 5, JavaScript
- **Backend:** Python, Flask
- **Database:** SQLite
- **Deployment:** Render

## ✨ Features
- 📊 Dashboard with live stats (total students, subjects, overall average, top performer)
- 👤 Full student management (Add / Edit / Delete / View / Search by roll number)
- 📝 Grade management for 5 subjects (Mathematics, Science, English, Computer, Social Science)
- 📈 Reports: student-wise average, subject-wise average, overall class average
- 🏆 Subject-wise toppers + overall topper
- ✅ Input validation (unique roll numbers, marks between 0–100)
- ⚠️ Custom exception handling (duplicate roll numbers, invalid marks, student/grade not found)

## 📁 Project Structure
```
Student_Performance_Tracker/
│── app.py              # Flask routes
│── models.py            # OOP: Student, StudentTracker, custom exceptions
│── database.py           # SQLite connection & table creation
│── requirements.txt        # Python dependencies
│── Procfile             # Deployment start command
│── .gitignore
│
├── templates/            # Jinja2 HTML templates (Bootstrap 5)
│   ├── base.html
│   ├── index.html
│   ├── students.html
│   ├── add_student.html
│   ├── edit_student.html
│   ├── add_grade.html
│   ├── student_details.html
│   ├── reports.html
│   ├── topper.html
│   └── 404.html
│
└── static/
    ├── css/style.css
    └── js/script.js
```

## 💻 Run Locally

```bash
# 1. Clone the repository
git clone https://github.com/AayushiSonkar/Student-Performance-Tracker.git
cd Student-Performance-Tracker

# 2. Create and activate a virtual environment
python -m venv venv
venv\Scripts\activate        # Windows
# source venv/bin/activate   # Mac/Linux

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run the app
python app.py
```
Then open `http://127.0.0.1:5000` in your browser.

## 🗄️ Database Schema

**students**
| Column | Type | Notes |
|---|---|---|
| id | INTEGER | Primary Key, Auto-increment |
| name | TEXT | Required |
| roll_number | TEXT | Required, Unique |

**grades**
| Column | Type | Notes |
|---|---|---|
| id | INTEGER | Primary Key, Auto-increment |
| student_id | INTEGER | Foreign Key → students.id (ON DELETE CASCADE) |
| subject | TEXT | Required |
| marks | REAL | Required, 0–100 |

## ☁️ Deployment Guide (Render)

1. Push your code to GitHub (make sure `database.db` and `venv/` are **not** committed — check `.gitignore`).
2. Go to [render.com](https://render.com) and sign up / log in with GitHub.
3. Click **New +** → **Web Service**.
4. Connect your GitHub repository (`Student-Performance-Tracker`).
5. Configure:
   - **Name:** student-performance-tracker (or anything you like)
   - **Runtime:** Python 3
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `gunicorn app:app`
   - **Instance Type:** Free
6. Click **Create Web Service**. Render will install dependencies and start your app.
7. Once deployed, Render gives you a live URL like `https://student-performance-tracker.onrender.com` — this is your submission link.

> ⚠️ **Note on the free tier:** Render's free plan uses an ephemeral filesystem, meaning your SQLite database resets whenever the service restarts or redeploys. This is fine for demoing/grading purposes. For persistent storage in a real production app, you'd attach a Render Disk or switch to a hosted database like PostgreSQL.

## 👩‍💻 Author
Aayushi Sonkar