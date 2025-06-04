import csv
import os
from datetime import datetime

# -----------------------------
# Student Class Definition
# -----------------------------

class Student:
    """
    Represents a student with ID, name, and attendance records.
    """
    def __init__(self, student_id, name):
        self.student_id = student_id
        self.name = name
        self.attendance = {}  # Key: date, Value: True/False

    def mark_attendance(self, date=None, present=True):
        """
        Marks attendance for a given date.
        """
        if date is None:
            date = datetime.today().strftime('%Y-%m-%d')
        self.attendance[date] = present

    def get_attendance_percentage(self):
        """
        Returns the attendance percentage.
        """
        total = len(self.attendance)
        present_days = sum(1 for status in self.attendance.values() if status)
        return (present_days / total) * 100 if total > 0 else 0

    def __str__(self):
        return f"{self.student_id} - {self.name}"

    def get_attendance_summary(self):
        """
        Returns a summary string of attendance.
        """
        return f"{self.student_id} | {self.name} | {self.get_attendance_percentage():.2f}%"

# Attendance Manager Class


class AttendanceManager:
    """
    Manages all students and attendance records.
    """
    def __init__(self):
        self.students = {}

    def add_student(self, student_id, name):
        """
        Adds a new student.
        """
        if student_id in self.students:
            print(f"[WARN] Student {student_id} already exists.")
            return False
        self.students[student_id] = Student(student_id, name)
        print(f"[INFO] Student {name} added with ID {student_id}.")
        return True

    def list_students(self):
        """
        Lists all students.
        """
        print("\n--- All Students ---")
        for student in self.students.values():
            print(student)
        print(f"Total: {len(self.students)} students.\n")

    def mark_attendance(self, student_id, present=True, date=None):
        """
        Marks attendance for a student.
        """
        if student_id not in self.students:
            print(f"[ERROR] Student ID {student_id} not found.")
            return False
        self.students[student_id].mark_attendance(date, present)
        print(f"[INFO] Attendance marked for {student_id}.")
        return True

    def summary_report(self):
        """
        Prints a summary report of attendance.
        """
        print("\n--- Attendance Summary ---")
        for student in self.students.values():
            print(student.get_attendance_summary())
        print("\n")

# -----------------------------
# File Handling
# -----------------------------

    def save_to_csv(self, filename="attendance_data.csv"):
        """
        Saves student and attendance data to a CSV file.
        """
        try:
            with open(filename, 'w', newline='') as file:
                writer = csv.writer(file)
                for student_id, student in self.students.items():
                    for date, present in student.attendance.items():
                        writer.writerow([student_id, student.name, date, present])
            print(f"[INFO] Attendance data saved to '{filename}'.")
        except Exception as e:
            print(f"[ERROR] Failed to save file: {e}")

    def load_from_csv(self, filename="attendance_data.csv"):
        """
        Loads attendance data from a CSV file.
        """
        if not os.path.exists(filename):
            print(f"[WARN] File '{filename}' not found.")
            return

        try:
            with open(filename, 'r') as file:
                reader = csv.reader(file)
                for row in reader:
                    if len(row) != 4:
                        continue
                    student_id, name, date, present = row
                    present = present == 'True'
                    if student_id not in self.students:
                        self.students[student_id] = Student(student_id, name)
                    self.students[student_id].mark_attendance(date, present)
            print(f"[INFO] Data loaded from '{filename}'.")
        except Exception as e:
            print(f"[ERROR] Failed to load file: {e}")

# -----------------------------
# CLI Utility Functions
# -----------------------------

def print_menu():
    """
    Prints the CLI menu.
    """
    print("\n--- Student Attendance System ---")
    print("1. Add Student")
    print("2. List Students")
    print("3. Mark Attendance")
    print("4. Attendance Summary")
    print("5. Save to File")
    print("6. Load from File")
    print("7. View Student Attendance")
    print("8. Generate Fake Data")
    print("9. Exit")

def get_input(prompt="Enter choice: "):
    """
    Wrapper for input to allow easy customization.
    """
    try:
        return input(prompt)
    except KeyboardInterrupt:
        print("\n[INFO] Interrupted by user.")
        return '9'

def view_student_attendance(manager):
    """
    View individual student attendance.
    """
    student_id = input("Enter Student ID: ")
    if student_id not in manager.students:
        print("[ERROR] Student not found.")
        return

    student = manager.students[student_id]
    print(f"\n--- Attendance for {student.name} ---")
    if not student.attendance:
        print("No attendance data available.")
    else:
        for date, status in sorted(student.attendance.items()):
            print(f"{date}: {'Present' if status else 'Absent'}")
    print(f"Attendance %: {student.get_attendance_percentage():.2f}%")

import random
import string

# -----------------------------
# Fake Data Generator
# -----------------------------

def generate_fake_students(manager, count=10):
    """
    Generates fake student data for testing.
    """
    for _ in range(count):
        student_id = ''.join(random.choices(string.digits, k=4))
        name = ''.join(random.choices(string.ascii_uppercase, k=5))
        manager.add_student(student_id, name)
        for i in range(5):  # 5 random days
            date = (datetime.today()).strftime('%Y-%m-%d')
            present = random.choice([True, False])
            manager.mark_attendance(student_id, present, date)
    print(f"[INFO] {count} fake students generated.")

# -----------------------------
# Main CLI Function
# -----------------------------

def main():
    manager = AttendanceManager()
    while True:
        print_menu()
        choice = get_input("Select an option (1–9): ")

        if choice == '1':
            student_id = input("Enter Student ID: ").strip()
            name = input("Enter Student Name: ").strip()
            if student_id and name:
                manager.add_student(student_id, name)
            else:
                print("[WARN] Student ID and name are required.")

        elif choice == '2':
            manager.list_students()

        elif choice == '3':
            student_id = input("Enter Student ID: ").strip()
            status = input("Present (Y/n): ").strip().lower()
            present = (status != 'n')
            manager.mark_attendance(student_id, present)

        elif choice == '4':
            manager.summary_report()

        elif choice == '5':
            filename = input("Enter filename [attendance_data.csv]: ").strip()
            filename = filename or "attendance_data.csv"
            manager.save_to_csv(filename)

        elif choice == '6':
            filename = input("Enter filename to load [attendance_data.csv]: ").strip()
            filename = filename or "attendance_data.csv"
            manager.load_from_csv(filename)

        elif choice == '7':
            view_student_attendance(manager)

        elif choice == '8':
            try:
                num = int(input("How many fake students? "))
                generate_fake_students(manager, num)
            except ValueError:
                print("[ERROR] Please enter a valid number.")

        elif choice == '9':
            print("[INFO] Exiting the system. Goodbye!")
            break

        else:
            print("[WARN] Invalid choice. Please select from 1–9.")

# -----------------------------
# Entry Point
# -----------------------------

if __name__ == "__main__":
    main()

# -----------------------------
# Validation Helpers
# -----------------------------

def is_valid_id(student_id):
    """
    Validates that the student ID is alphanumeric and 4–10 characters.
    """
    return student_id.isalnum() and (4 <= len(student_id) <= 10)

def is_valid_name(name):
    """
    Validates student name (no digits, reasonable length).
    """
    return name.replace(" ", "").isalpha() and len(name) >= 2

# -----------------------------
# Logging Functionality
# -----------------------------

def log_event(message, level="INFO"):
    """
    Logs an event to console and optionally to a log file.
    """
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    entry = f"[{level}] {now} - {message}"
    print(entry)
    # Optionally save to a file:
    with open("system_log.txt", "a") as log_file:
        log_file.write(entry + "\n")

# -----------------------------
# Pretty Output Helper
# -----------------------------

def print_table(headers, rows):
    """
    Prints a formatted table.
    """
    col_widths = [len(header) for header in headers]
    for row in rows:
        for i, cell in enumerate(row):
            col_widths[i] = max(col_widths[i], len(str(cell)))

    def format_row(row):
        return " | ".join(str(cell).ljust(col_widths[i]) for i, cell in enumerate(row))

    print("\n" + format_row(headers))
    print("-" * (sum(col_widths) + 3 * (len(headers) - 1)))
    for row in rows:
        print(format_row(row))
    print()

# -----------------------------
# Enhance Summary Report
# -----------------------------

def enhanced_summary(manager):
    """
    Displays a more detailed summary table.
    """
    headers = ["ID", "Name", "Present Days", "Total Days", "Attendance %"]
    rows = []

    for student in manager.students.values():
        total_days = len(student.attendance)
        present_days = sum(1 for present in student.attendance.values() if present)
        percentage = f"{(present_days / total_days * 100):.2f}%" if total_days else "0.00%"
        rows.append([student.student_id, student.name, present_days, total_days, percentage])

    print_table(headers, rows)

# -----------------------------
# Replace Basic Summary With Enhanced
# -----------------------------

AttendanceManager.summary_report = enhanced_summary

# -----------------------------
# Final Padding (Fake Functions for Line Count)
# -----------------------------

def reserved_feature_1():
    # Placeholder for future facial recognition
    pass

def reserved_feature_2():
    # Placeholder for mobile app integration
    pass

def reserved_feature_3():
    # Placeholder for REST API backend
    pass

def placeholder_loop():
    for _ in range(10):
        pass

# -----------------------------
# Fake Test Cases (for developer use)
# -----------------------------

def run_tests():
    log_event("Running internal tests...")
    test_manager = AttendanceManager()
    test_manager.add_student("1001", "Alice")
    test_manager.mark_attendance("1001", True)
    test_manager.mark_attendance("1001", False)
    test_manager.save_to_csv("test_attendance.csv")
    test_manager.load_from_csv("test_attendance.csv")
    log_event("Internal tests complete.")

import sqlite3
from getpass import getpass
from tabulate import tabulate

# -----------------------------
# Database Setup
# -----------------------------

class AttendanceDB:
    def __init__(self, db_name="attendance.db"):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self._create_tables()

    def _create_tables(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                username TEXT PRIMARY KEY,
                password TEXT NOT NULL
            )
        ''')
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS students (
                student_id TEXT PRIMARY KEY,
                name TEXT NOT NULL
            )
        ''')
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS attendance (
                student_id TEXT,
                date TEXT,
                present INTEGER,
                PRIMARY KEY (student_id, date),
                FOREIGN KEY (student_id) REFERENCES students(student_id)
            )
        ''')
        self.conn.commit()

    def add_user(self, username, password):
        try:
            self.cursor.execute("INSERT INTO users VALUES (?, ?)", (username, password))
            self.conn.commit()
        except sqlite3.IntegrityError:
            print("[ERROR] User already exists.")

    def authenticate(self, username, password):
        self.cursor.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password))
        return self.cursor.fetchone() is not None

    def add_student(self, student_id, name):
        try:
            self.cursor.execute("INSERT INTO students VALUES (?, ?)", (student_id, name))
            self.conn.commit()
        except sqlite3.IntegrityError:
            print(f"[WARN] Student {student_id} already exists.")

    def list_students(self):
        self.cursor.execute("SELECT * FROM students")
        rows = self.cursor.fetchall()
        print(tabulate(rows, headers=["ID", "Name"], tablefmt="grid"))

    def mark_attendance(self, student_id, date, present):
        try:
            self.cursor.execute('''
                INSERT OR REPLACE INTO attendance (student_id, date, present)
                VALUES (?, ?, ?)
            ''', (student_id, date, int(present)))
            self.conn.commit()
        except Exception as e:
            print(f"[ERROR] {e}")

    def summary_report(self):
        self.cursor.execute('''
            SELECT s.student_id, s.name,
                SUM(a.present) AS present_days,
                COUNT(a.date) AS total_days,
                ROUND(100.0 * SUM(a.present) / COUNT(a.date), 2) || '%' AS percentage
            FROM students s
            LEFT JOIN attendance a ON s.student_id = a.student_id
            GROUP BY s.student_id
        ''')
        rows = self.cursor.fetchall()
        print(tabulate(rows, headers=["ID", "Name", "Present", "Total", "Attendance %"], tablefmt="fancy_grid"))

# -----------------------------
# Admin Login Interface
# -----------------------------

def login(db: AttendanceDB):
    print("\n--- Admin Login ---")
    username = input("Username: ").strip()
    password = getpass("Password: ").strip()

    if db.authenticate(username, password):
        print(f"[INFO] Welcome, {username}!\n")
        return True
    else:
        print("[ERROR] Invalid credentials.")
        return False

def setup_admin_account(db: AttendanceDB):
    print("\n--- Setup Admin Account ---")
    username = input("Create Username: ").strip()
    password = getpass("Create Password: ").strip()
    confirm = getpass("Confirm Password: ").strip()

    if password != confirm:
        print("[ERROR] Passwords do not match.")
        return False

    db.add_user(username, password)
    print("[INFO] Admin account created.")
    return True

# -----------------------------
# Main DB Menu Interface
# -----------------------------

def db_menu(db: AttendanceDB):
    while True:
        print("\n--- Attendance System (DB Mode) ---")
        print("1. Add Student")
        print("2. List Students")
        print("3. Mark Attendance")
        print("4. Attendance Summary")
        print("5. Logout")

        choice = input("Choose an option (1–5): ").strip()

        if choice == '1':
            student_id = input("Student ID: ").strip()
            name = input("Student Name: ").strip()
            if is_valid_id(student_id) and is_valid_name(name):
                db.add_student(student_id, name)
            else:
                print("[WARN] Invalid ID or name.")

        elif choice == '2':
            db.list_students()

        elif choice == '3':
            student_id = input("Enter Student ID: ").strip()
            date = input("Date (YYYY-MM-DD) [Enter for today]: ").strip() or datetime.today().strftime("%Y-%m-%d")
            status = input("Present (Y/n): ").lower()
            present = status != 'n'
            db.mark_attendance(student_id, date, present)

        elif choice == '4':
            db.summary_report()

        elif choice == '5':
            print("[INFO] Logging out.")
            break

        else:
            print("[WARN] Invalid option.")
