import json
import os


class Student:

    def __init__(self, name, roll):
        self.name = name
        self.roll = roll
        self.grades = {}

    def add_grades(self, subject, marks):
        self.grades[subject] = marks

    def show_details(self):
        print("Name:", self.name)
        print("Roll:", self.roll)
        print("Grades:")

        if len(self.grades) == 0:
            print("No subjects added yet.")
        else:
            for subject, marks in self.grades.items():
                print(subject, ":", marks)

    def average(self):
        if len(self.grades) == 0:
            return 0
        return sum(self.grades.values()) / len(self.grades)

    def save_data(self):
        data = {
            "name": self.name,
            "roll": self.roll,
            "grades": self.grades
        }

        with open("student.json", "w") as file:
            json.dump(data, file, indent=4)

    def load_data(self):
        try:
            with open("student.json", "r") as file:
                data = json.load(file)

            self.name = data["name"]
            self.roll = data["roll"]
            self.grades = data["grades"]

        except FileNotFoundError:
            print("No Previous Data Found!")


if os.path.exists("student.json"):
    student = Student("", 0)
    student.load_data()
    print("Previous data loaded successfully!")

else:
    name = input("Enter Name: ")
    roll = int(input("Enter Roll: "))

    student = Student(name, roll)
    student.save_data()


while True:

    print("\n===== Student Performance Tracker =====")
    print("1. Add Marks")
    print("2. Show Details")
    print("3. Show Average")
    print("4. Exit")
    print("5. Edit Marks")
    print("6. Delete Subject")
    print("7. Reset All Data")

    choice = input("Enter Choice: ")

    if choice == "1":
        subject = input("Enter Subject: ")

        try:
            marks = int(input("Enter Marks: "))
            student.add_grades(subject, marks)
            student.save_data()
            print("Marks Added Successfully!")

        except ValueError:
            print("Invalid Input! Please enter a number.")

    elif choice == "2":
        student.show_details()

    elif choice == "3":
        print("Average =", round(student.average(), 2))

    elif choice == "5":
        subject = input("Enter Subject to Edit: ")

        if subject in student.grades:

            try:
                marks = int(input("Enter New Marks: "))
                student.add_grades(subject, marks)
                student.save_data()
                print("Marks Updated Successfully!")

            except ValueError:
                print("Invalid Input! Please enter a number.")

        else:
            print("Subject Not Found!")

    elif choice == "6":
        subject = input("Enter Subject to Delete: ")

        if subject in student.grades:
            del student.grades[subject]
            student.save_data()
            print("Subject Deleted Successfully!")

        else:
            print("Subject Not Found!")

    elif choice == "7":
        student.grades.clear()
        student.save_data()
        print("All Data Reset Successfully!")

    elif choice == "4":
        print("Thank You!")
        break

    else:
        print("Invalid Choice! Please Try Again.")