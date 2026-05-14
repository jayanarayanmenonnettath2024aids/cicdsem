"""
Student Manager Module
Handles CRUD operations for students
"""

import json
import os
from datetime import datetime
import logging

# Configure logging
logger = logging.getLogger(__name__)

# ================================
# DATABASE CONFIGURATION
# ================================

# Get absolute project root directory
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

# Database file path
DATABASE_FILE = os.path.join(BASE_DIR, "students_db.json")

# Automatically create database file if missing
if not os.path.exists(DATABASE_FILE):

    initial_data = {
        "students": [],
        "next_id": 1,
        "created_at": datetime.now().isoformat()
    }

    with open(DATABASE_FILE, "w") as f:
        json.dump(initial_data, f, indent=2)

    logger.info(f"Database created at: {DATABASE_FILE}")


class StudentManager:
    """
    Student Manager Class
    Handles all CRUD operations
    """

    def __init__(self):
        self.db_file = DATABASE_FILE

    # ================================
    # LOAD DATABASE
    # ================================
    def _load_database(self):

        try:
            with open(self.db_file, "r") as f:
                return json.load(f)

        except Exception as e:
            logger.error(f"Error loading database: {str(e)}")
            raise

    # ================================
    # SAVE DATABASE
    # ================================
    def _save_database(self, data):

        try:
            with open(self.db_file, "w") as f:
                json.dump(data, f, indent=2)

            logger.info("Database saved successfully")

        except Exception as e:
            logger.error(f"Error saving database: {str(e)}")
            raise

    # ================================
    # ADD STUDENT
    # ================================
    def add_student(self, student_data):

        try:

            if not student_data.get("name"):
                raise ValueError("Student name is required")

            if not student_data.get("email"):
                raise ValueError("Student email is required")

            db = self._load_database()

            new_student = {
                "id": db["next_id"],
                "name": student_data["name"],
                "email": student_data["email"],
                "phone": student_data.get("phone", ""),
                "grade": student_data.get("grade", ""),
                "major": student_data.get("major", ""),
                "created_at": datetime.now().isoformat(),
                "updated_at": datetime.now().isoformat()
            }

            db["students"].append(new_student)

            db["next_id"] += 1

            self._save_database(db)

            logger.info(f"Student added: {new_student['name']}")

            return new_student

        except Exception as e:
            logger.error(f"Error adding student: {str(e)}")
            raise

    # ================================
    # GET ALL STUDENTS
    # ================================
    def get_all_students(self):

        try:
            db = self._load_database()
            return db.get("students", [])

        except Exception as e:
            logger.error(f"Error getting students: {str(e)}")
            raise

    # ================================
    # GET STUDENT BY ID
    # ================================
    def get_student_by_id(self, student_id):

        try:

            db = self._load_database()

            for student in db.get("students", []):

                if student["id"] == int(student_id):
                    return student

            return None

        except Exception as e:
            logger.error(f"Error getting student: {str(e)}")
            raise

    # ================================
    # UPDATE STUDENT
    # ================================
    def update_student(self, student_id, updated_data):

        try:

            db = self._load_database()

            for student in db.get("students", []):

                if student["id"] == int(student_id):

                    student["name"] = updated_data.get(
                        "name",
                        student["name"]
                    )

                    student["email"] = updated_data.get(
                        "email",
                        student["email"]
                    )

                    student["phone"] = updated_data.get(
                        "phone",
                        student["phone"]
                    )

                    student["grade"] = updated_data.get(
                        "grade",
                        student["grade"]
                    )

                    student["major"] = updated_data.get(
                        "major",
                        student["major"]
                    )

                    student["updated_at"] = datetime.now().isoformat()

                    self._save_database(db)

                    logger.info(f"Student updated: {student_id}")

                    return student

            return None

        except Exception as e:
            logger.error(f"Error updating student: {str(e)}")
            raise

    # ================================
    # DELETE STUDENT
    # ================================
    def delete_student(self, student_id):

        try:

            db = self._load_database()

            for i, student in enumerate(db.get("students", [])):

                if student["id"] == int(student_id):

                    db["students"].pop(i)

                    self._save_database(db)

                    logger.info(f"Student deleted: {student_id}")

                    return True

            return False

        except Exception as e:
            logger.error(f"Error deleting student: {str(e)}")
            raise

    # ================================
    # GET STUDENT COUNT
    # ================================
    def get_student_count(self):

        try:

            db = self._load_database()

            return len(db.get("students", []))

        except Exception as e:
            logger.error(f"Error getting count: {str(e)}")
            return 0

    # ================================
    # SEARCH STUDENTS
    # ================================
    def search_students(self, query):

        try:

            db = self._load_database()

            query_lower = query.lower()

            results = [
                student for student in db.get("students", [])
                if query_lower in student["name"].lower()
                or query_lower in student["email"].lower()
            ]

            return results

        except Exception as e:
            logger.error(f"Error searching students: {str(e)}")
            return []

    # ================================
    # CLEAR DATABASE
    # ================================
    def clear_all_students(self):

        try:

            db = self._load_database()

            db["students"] = []
            db["next_id"] = 1

            self._save_database(db)

            logger.warning("All students cleared")

            return True

        except Exception as e:
            logger.error(f"Error clearing database: {str(e)}")
            raise
