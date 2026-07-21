# Student Performance Tracker

A Flask-based web application to manage students, record their subject-wise grades, and view class performance reports — built as a step-by-step internship project.

## Features

- **Dashboard** — quick overview: total students, total subjects, overall class average, top performer
- **Student Management** — add, edit, delete, view, and search students (by roll number)
- **Grade Management** — add and delete subject-wise grades for each student, with input validation (marks must be 0–100)
- **Reports** — per-student averages, per-subject class averages, overall class average
- **Toppers** — subject-wise toppers and the overall topper
- **Custom exception handling** — duplicate roll numbers, invalid marks, and missing students/grades are all handled gracefully with user-facing flash messages instead of crashing

## Tech Stack

- **Backend:** Python, Flask
- **Database:** SQLite
- **Templates:** Jinja2
- **Frontend:** Bootstrap, custom CSS/JS
- **Version control:** Git

## Project Structure

```
Student_Performance_Tracker/
├── app.py                  # Flask routes (the only file that talks to Flask)
├── models.py                # StudentTracker class + custom exceptions (business logic)
├── database.py               # Database connection + table setup
├── database.db              # SQLite database file
├── requirements.txt
├── Procfile                # For deployment
├── templates/
│   ├── base.html            # Shared layout (navbar, flash messages)
│   ├── index.html            # Dashboard
│   ├── students.html          # All students list
│   ├── add_student.html        # Add student form
│   ├── edit_student.html        # Edit student form
│   ├── student_details.html      # Single student profile + grades
│   ├── add_grade.html          # Add grade form
│   ├── reports.html           # Class + subject reports
│   ├── topper.html            # Subject and overall toppers
│   └── 404.html              # Custom error page
└── static/
    ├── css/style.css
    └── js/script.js
```

## Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/AayushiSonkar/Student-Performance-Tracker.git
   cd Student-Performance-Tracker
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   venv\Scripts\activate      # Windows
   source venv/bin/activate   # macOS/Linux
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Run the app:
   ```bash
   python app.py
   ```

5. Open your browser at [http://127.0.0.1:5000](http://127.0.0.1:5000)

## Routes

| Route | Method | Description |
|---|---|---|
| `/` | GET | Dashboard |
| `/students` | GET | List all students |
| `/student/add` | GET, POST | Add a new student |
| `/student/edit/<id>` | GET, POST | Edit a student |
| `/student/delete/<id>` | POST | Delete a student |
| `/student/<id>` | GET | View student details + grades |
| `/search` | GET | Search a student by roll number |
| `/grades/add/<student_id>` | GET, POST | Add a grade |
| `/grades/delete/<grade_id>/<student_id>` | POST | Delete a grade |
| `/reports` | GET | Class and subject reports |
| `/topper` | GET | Subject-wise and overall toppers |

## Error Handling

Custom exceptions defined in `models.py` keep the app from crashing on bad input:

- `DuplicateRollNumberError` — roll number already exists
- `StudentNotFoundError` — student ID doesn't exist
- `GradeNotFoundError` — grade ID doesn't exist
- `InvalidMarksError` — marks aren't a number, or aren't between 0–100

All are caught in `app.py` and shown to the user as flash messages instead of a stack trace.

## Author

Built by Ayushi Sonkar as part of an internship project.