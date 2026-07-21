# app.py
# -----------------------------------------------------------------------------
# Main Flask application. Defines all URL routes.
# This file NEVER writes raw SQL - it only calls methods on StudentTracker
# (from models.py), which handles all database work.
# -----------------------------------------------------------------------------

from flask import Flask, render_template, request, redirect, url_for, flash

import database
from models import (
    StudentTracker,
    SUBJECTS,
    DuplicateRollNumberError,
    StudentNotFoundError,
    GradeNotFoundError,
    InvalidMarksError,
)

app = Flask(__name__)

# Needed for flash() messages to work (Flask encrypts the message using this key).
# In a real production app this should be a long random secret, not readable text.
app.secret_key = "student-performance-tracker-secret-key"

# Create the database tables (if they don't exist yet) the moment the app starts.
database.init_db()

# One shared StudentTracker instance used by every route.
tracker = StudentTracker()


# ---------------- Dashboard ----------------

@app.route("/")
def index():
    """Homepage: shows dashboard cards (total students, subjects, average, top performer)."""
    stats = tracker.get_dashboard_stats()
    return render_template("index.html", stats=stats)


# ---------------- Student Management ----------------

@app.route("/students")
def students():
    """Lists all students in a table."""
    all_students = tracker.get_all_students()
    return render_template("students.html", students=all_students)


@app.route("/student/add", methods=["GET", "POST"])
def add_student():
    """GET: show the add-student form. POST: process the form submission."""
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        roll_number = request.form.get("roll_number", "").strip()
        try:
            tracker.add_student(name, roll_number)
            flash("Student added successfully!", "success")
            return redirect(url_for("students"))
        except DuplicateRollNumberError as e:
            flash(str(e), "danger")
    return render_template("add_student.html")


@app.route("/student/edit/<int:student_id>", methods=["GET", "POST"])
def edit_student(student_id):
    """GET: show the edit form pre-filled. POST: save changes."""
    try:
        student, grades = tracker.view_student(student_id)
    except StudentNotFoundError as e:
        flash(str(e), "danger")
        return redirect(url_for("students"))

    if request.method == "POST":
        name = request.form.get("name", "").strip()
        roll_number = request.form.get("roll_number", "").strip()
        try:
            tracker.edit_student(student_id, name, roll_number)
            flash("Student updated successfully!", "success")
            return redirect(url_for("students"))
        except DuplicateRollNumberError as e:
            flash(str(e), "danger")

    return render_template("edit_student.html", student=student)


@app.route("/student/delete/<int:student_id>", methods=["POST"])
def delete_student(student_id):
    """Deletes a student (their grades are removed automatically via ON DELETE CASCADE)."""
    try:
        tracker.delete_student(student_id)
        flash("Student deleted successfully!", "success")
    except StudentNotFoundError as e:
        flash(str(e), "danger")
    return redirect(url_for("students"))


@app.route("/student/<int:student_id>")
def student_details(student_id):
    """Shows one student's full profile: their info + all grades + their average."""
    try:
        student, grades = tracker.view_student(student_id)
    except StudentNotFoundError as e:
        flash(str(e), "danger")
        return redirect(url_for("students"))
    average = tracker.calculate_average(student_id)
    return render_template("student_details.html", student=student, grades=grades, average=average)


@app.route("/search")
def search_student():
    """Search a student by roll number (used by the search box)."""
    roll_number = request.args.get("roll_number", "").strip()
    student = tracker.search_student(roll_number)
    if student is None:
        flash(f"No student found with roll number '{roll_number}'.", "danger")
        return redirect(url_for("students"))
    return redirect(url_for("student_details", student_id=student["id"]))


# ---------------- Grade Management ----------------

@app.route("/grades/add/<int:student_id>", methods=["GET", "POST"])
def add_grade(student_id):
    """Adds a grade for one student. Subjects list comes from models.SUBJECTS."""
    try:
        student, grades = tracker.view_student(student_id)
    except StudentNotFoundError as e:
        flash(str(e), "danger")
        return redirect(url_for("students"))

    if request.method == "POST":
        subject = request.form.get("subject")
        marks = request.form.get("marks")
        try:
            tracker.add_grade(student_id, subject, marks)
            flash("Grade added successfully!", "success")
            return redirect(url_for("student_details", student_id=student_id))
        except InvalidMarksError as e:
            flash(str(e), "danger")

    return render_template("add_grade.html", student=student, subjects=SUBJECTS)


@app.route("/grades/delete/<int:grade_id>/<int:student_id>", methods=["POST"])
def delete_grade(grade_id, student_id):
    """Deletes one grade entry, then returns to that student's profile page."""
    try:
        tracker.delete_grade(grade_id)
        flash("Grade deleted successfully!", "success")
    except GradeNotFoundError as e:
        flash(str(e), "danger")
    return redirect(url_for("student_details", student_id=student_id))


# ---------------- Reports ----------------

@app.route("/reports")
def reports():
    """Shows every student's average, plus each subject's class average, plus overall average."""
    all_students = tracker.get_all_students()
    report_data = [
        {"student": s, "average": tracker.calculate_average(s["id"])}
        for s in all_students
    ]
    subject_averages = {subject: tracker.subject_average(subject) for subject in SUBJECTS}
    overall_avg = tracker.class_average()
    return render_template(
        "reports.html",
        report_data=report_data,
        subject_averages=subject_averages,
        overall_avg=overall_avg,
    )


@app.route("/topper")
def topper():
    """Shows the top scorer in each subject, plus the overall topper."""
    toppers = tracker.all_subject_toppers()
    overall = tracker.overall_topper()
    return render_template("topper.html", toppers=toppers, overall=overall)


# ---------------- Error Handling ----------------

@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404


if __name__ == "__main__":
    # debug=True auto-reloads on save and shows detailed error pages while developing.
    app.run(debug=True)