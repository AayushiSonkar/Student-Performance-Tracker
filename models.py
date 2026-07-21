# models.py
# -----------------------------------------------------------------------------
# OOP layer: custom exceptions + Student class + StudentTracker class.
# app.py will NEVER write raw SQL — it only calls methods on StudentTracker.
# -----------------------------------------------------------------------------

import sqlite3
from database import get_db_connection

SUBJECTS = ["Mathematics", "Science", "English", "Computer", "Social Science"]


# ---------------- Custom Exceptions ----------------

class DuplicateRollNumberError(Exception):
    """Raised when a roll number already exists."""
    pass


class StudentNotFoundError(Exception):
    """Raised when a student ID/roll number doesn't exist."""
    pass


class GradeNotFoundError(Exception):
    """Raised when a grade ID doesn't exist."""
    pass


class InvalidMarksError(Exception):
    """Raised when marks are not a number, or not between 0 and 100."""
    pass


# ---------------- Student class ----------------

class Student:
    def __init__(self, id, name, roll_number):
        self.id = id
        self.name = name
        self.roll_number = roll_number

    def __repr__(self):
        return f"Student(id={self.id}, name='{self.name}', roll_number='{self.roll_number}')"


# ---------------- StudentTracker class ----------------

class StudentTracker:

    @staticmethod
    def _validate_marks(marks):
        try:
            marks = float(marks)
        except (ValueError, TypeError):
            raise InvalidMarksError("Marks must be a valid number.")
        if marks < 0 or marks > 100:
            raise InvalidMarksError("Marks must be between 0 and 100.")
        return marks

    # ---------------- Student Management ----------------

    def add_student(self, name, roll_number):
        conn = get_db_connection()
        try:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO students (name, roll_number) VALUES (?, ?)",
                (name.strip(), roll_number.strip())
            )
            conn.commit()
            return cursor.lastrowid
        except sqlite3.IntegrityError:
            raise DuplicateRollNumberError(f"Roll number '{roll_number}' already exists.")
        finally:
            conn.close()

    def edit_student(self, student_id, name, roll_number):
        conn = get_db_connection()
        try:
            existing = conn.execute("SELECT * FROM students WHERE id = ?", (student_id,)).fetchone()
            if existing is None:
                raise StudentNotFoundError(f"No student found with id {student_id}.")
            conn.execute(
                "UPDATE students SET name = ?, roll_number = ? WHERE id = ?",
                (name.strip(), roll_number.strip(), student_id)
            )
            conn.commit()
        except sqlite3.IntegrityError:
            raise DuplicateRollNumberError(f"Roll number '{roll_number}' already exists.")
        finally:
            conn.close()

    def delete_student(self, student_id):
        conn = get_db_connection()
        try:
            existing = conn.execute("SELECT * FROM students WHERE id = ?", (student_id,)).fetchone()
            if existing is None:
                raise StudentNotFoundError(f"No student found with id {student_id}.")
            conn.execute("DELETE FROM students WHERE id = ?", (student_id,))
            conn.commit()
        finally:
            conn.close()

    def search_student(self, roll_number):
        conn = get_db_connection()
        try:
            return conn.execute(
                "SELECT * FROM students WHERE roll_number = ?", (roll_number.strip(),)
            ).fetchone()
        finally:
            conn.close()

    def get_all_students(self):
        conn = get_db_connection()
        try:
            return conn.execute("SELECT * FROM students ORDER BY name ASC").fetchall()
        finally:
            conn.close()

    def view_student(self, student_id):
        conn = get_db_connection()
        try:
            student = conn.execute("SELECT * FROM students WHERE id = ?", (student_id,)).fetchone()
            if student is None:
                raise StudentNotFoundError(f"No student found with id {student_id}.")
            grades = conn.execute(
                "SELECT * FROM grades WHERE student_id = ? ORDER BY subject", (student_id,)
            ).fetchall()
            return student, grades
        finally:
            conn.close()

    # ---------------- Grade Management ----------------

    def add_grade(self, student_id, subject, marks):
        marks = self._validate_marks(marks)
        conn = get_db_connection()
        try:
            student = conn.execute("SELECT * FROM students WHERE id = ?", (student_id,)).fetchone()
            if student is None:
                raise StudentNotFoundError(f"No student found with id {student_id}.")
            conn.execute(
                "INSERT INTO grades (student_id, subject, marks) VALUES (?, ?, ?)",
                (student_id, subject, marks)
            )
            conn.commit()
        finally:
            conn.close()

    def edit_grade(self, grade_id, subject, marks):
        marks = self._validate_marks(marks)
        conn = get_db_connection()
        try:
            grade = conn.execute("SELECT * FROM grades WHERE id = ?", (grade_id,)).fetchone()
            if grade is None:
                raise GradeNotFoundError(f"No grade found with id {grade_id}.")
            conn.execute(
                "UPDATE grades SET subject = ?, marks = ? WHERE id = ?",
                (subject, marks, grade_id)
            )
            conn.commit()
        finally:
            conn.close()

    def delete_grade(self, grade_id):
        conn = get_db_connection()
        try:
            grade = conn.execute("SELECT * FROM grades WHERE id = ?", (grade_id,)).fetchone()
            if grade is None:
                raise GradeNotFoundError(f"No grade found with id {grade_id}.")
            conn.execute("DELETE FROM grades WHERE id = ?", (grade_id,))
            conn.commit()
        finally:
            conn.close()

    # ---------------- Reports & Averages ----------------

    def calculate_average(self, student_id):
        conn = get_db_connection()
        try:
            result = conn.execute(
                "SELECT AVG(marks) as avg_marks FROM grades WHERE student_id = ?", (student_id,)
            ).fetchone()
            return round(result["avg_marks"], 2) if result["avg_marks"] is not None else 0.0
        finally:
            conn.close()

    def class_average(self):
        conn = get_db_connection()
        try:
            result = conn.execute("SELECT AVG(marks) as avg_marks FROM grades").fetchone()
            return round(result["avg_marks"], 2) if result["avg_marks"] is not None else 0.0
        finally:
            conn.close()

    def subject_average(self, subject):
        conn = get_db_connection()
        try:
            result = conn.execute(
                "SELECT AVG(marks) as avg_marks FROM grades WHERE subject = ?", (subject,)
            ).fetchone()
            return round(result["avg_marks"], 2) if result["avg_marks"] is not None else 0.0
        finally:
            conn.close()

    def subject_topper(self, subject):
        conn = get_db_connection()
        try:
            return conn.execute("""
                SELECT students.name AS name, students.roll_number AS roll_number, grades.marks AS marks
                FROM grades
                JOIN students ON grades.student_id = students.id
                WHERE grades.subject = ?
                ORDER BY grades.marks DESC
                LIMIT 1
            """, (subject,)).fetchone()
        finally:
            conn.close()

    def all_subject_toppers(self):
        return {subject: self.subject_topper(subject) for subject in SUBJECTS}

    def overall_topper(self):
        conn = get_db_connection()
        try:
            return conn.execute("""
                SELECT students.name AS name, students.roll_number AS roll_number,
                       AVG(grades.marks) AS avg_marks
                FROM grades
                JOIN students ON grades.student_id = students.id
                GROUP BY grades.student_id
                ORDER BY avg_marks DESC
                LIMIT 1
            """).fetchone()
        finally:
            conn.close()

    def get_dashboard_stats(self):
        conn = get_db_connection()
        try:
            total_students = conn.execute("SELECT COUNT(*) AS c FROM students").fetchone()["c"]
        finally:
            conn.close()

        top = self.overall_topper()
        return {
            "total_students": total_students,
            "total_subjects": len(SUBJECTS),
            "overall_average": self.class_average(),
            "top_performer": top["name"] if top else "N/A"
        }